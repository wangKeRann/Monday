from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date
import mysql.connector
from mysql.connector import Error

from models import User, get_db
from auth import create_access_token, get_current_user
from github import get_github_access_token, get_github_user_info
from config import settings
from api import router as api_router  # 导入健康历史API路由
from getKeyPoint import router as indicators_router  # 导入指标检索路由
from analysise import router as analysis_router  # 导入趋势分析和详情路由
from countMember import router as comparison_router  # 导入性别统计路由
from last import router as last_router  # 导入 last.py 中的路由

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加健康历史API路由
app.include_router(api_router)

# 添加指标检索路由
app.include_router(indicators_router)

# 添加趋势分析和详情路由
app.include_router(analysis_router)

# 添加性别统计路由
app.include_router(comparison_router)

# 添加 last.py 中的路由
app.include_router(last_router)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'health_exam'
}

# 统计接口的数据模型
class AgeDistribution(BaseModel):
    age_range: str
    total: int
    count: int

class StatisticsResponse(BaseModel):
    total_count: int
    abnormal_count: int
    age_distribution: List[AgeDistribution]

class StatisticsResponseModel(BaseModel):
    code: int
    data: StatisticsResponse

def connect_to_database():
    """连接到数据库"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as err:
        raise HTTPException(status_code=500, detail=f"数据库连接错误: {err}")

@app.get("/api/statistics", response_model=StatisticsResponseModel)
async def get_statistics(current_user: User = Depends(get_current_user)):
    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)

        # 获取总检测人数
        total_sql = "SELECT COUNT(*) as total FROM exam_record"
        cursor.execute(total_sql)
        total_count = cursor.fetchone()['total']

        # 获取异常人数
        abnormal_sql = """
        SELECT COUNT(*) as abnormal 
        FROM exam_record 
        WHERE is_abnormal = 1
        """
        cursor.execute(abnormal_sql)
        abnormal_count = cursor.fetchone()['abnormal']

        # 获取各年龄段分布
        age_distribution_sql = """
        SELECT 
            CASE 
                WHEN age < 19 THEN '0-18'
                WHEN age BETWEEN 19 AND 30 THEN '19-30'
                WHEN age BETWEEN 31 AND 45 THEN '31-45'
                WHEN age BETWEEN 46 AND 60 THEN '46-60'
                ELSE '60+'
            END as age_range,
            COUNT(*) as total,
            SUM(CASE WHEN is_abnormal = 1 THEN 1 ELSE 0 END) as count
        FROM basic_info
        GROUP BY 
            CASE 
                WHEN age < 19 THEN '0-18'
                WHEN age BETWEEN 19 AND 30 THEN '19-30'
                WHEN age BETWEEN 31 AND 45 THEN '31-45'
                WHEN age BETWEEN 46 AND 60 THEN '46-60'
                ELSE '60+'
            END
        ORDER BY 
            CASE age_range
                WHEN '0-18' THEN 1
                WHEN '19-30' THEN 2
                WHEN '31-45' THEN 3
                WHEN '46-60' THEN 4
                ELSE 5
            END
        """
        cursor.execute(age_distribution_sql)
        age_distribution = cursor.fetchall()

        return {
            "code": 200,
            "data": {
                "total_count": total_count,
                "abnormal_count": abnormal_count,
                "age_distribution": age_distribution
            }
        }

    except Error as err:
        raise HTTPException(status_code=500, detail=f"数据库查询错误: {err}")
    finally:
        if conn:
            conn.close()

class GitHubCode(BaseModel):
    code: str

class UserResponse(BaseModel):
    id: int
    login: str
    email: Optional[str]
    avatar_url: Optional[str]
    github_id: str

    class Config:
        from_attributes = True

class ReferenceRange(BaseModel):
    min: float
    max: float

class TrendDataPoint(BaseModel):
    date: str
    value: float
    reference_range: ReferenceRange

class TrendAnalysisResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: List[TrendDataPoint]

@app.post("/api/auth/github/callback")
async def github_oauth(code_data: GitHubCode, db: Session = Depends(get_db)):
    # 获取GitHub访问令牌
    access_token = await get_github_access_token(code_data.code)
    
    # 获取GitHub用户信息
    github_user = await get_github_user_info(access_token)
    
    # 查找或创建用户
    user = db.query(User).filter(User.github_id == github_user["github_id"]).first()
    if not user:
        user = User(
            github_id=github_user["github_id"],
            username=github_user["username"],
            email=github_user["email"],
            avatar=github_user["avatar"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # 创建JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "login": user.username,
            "email": user.email,
            "avatar_url": user.avatar
        }
    }

@app.get("/api/user/info", response_model=UserResponse)
async def get_user_info(current_user: User = Depends(get_current_user)):
    return current_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 