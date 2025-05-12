from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
import mysql.connector

# 创建路由
router = APIRouter()

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'health_exam'
}

# 定义响应模型
class ComparisonResponse(BaseModel):
    code: int = 200
    data: dict

def connect_to_database():
    """连接到数据库"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"数据库连接错误: {err}")
        return None

@router.get("/api/health/comparison")
async def get_gender_comparison(age_range: str):
    try:
        # 验证年龄段参数
        valid_ranges = ["0-18", "19-30", "31-45", "46-60", "60+"]
        if age_range not in valid_ranges:
            raise HTTPException(status_code=400, detail="无效的年龄段参数")

        # 连接数据库
        conn = connect_to_database()
        if not conn:
            raise HTTPException(status_code=500, detail="数据库连接失败")
            
        cursor = conn.cursor(dictionary=True)
        
        # 根据年龄段构建查询条件
        if age_range == "60+":
            age_condition = "age >= 60"
        else:
            start_age, end_age = map(int, age_range.split("-"))
            age_condition = f"age >= {start_age} AND age <= {end_age}"
        
        # 构建查询SQL
        sql = f"""
        SELECT 
            gender,
            COUNT(*) as count
        FROM basic_info
        WHERE {age_condition}
        GROUP BY gender
        """
        
        # 执行查询
        cursor.execute(sql)
        results = cursor.fetchall()
        
        # 处理查询结果
        male_count = 0
        female_count = 0
        
        for result in results:
            if result['gender'] == '男':
                male_count = result['count']
            elif result['gender'] == '女':
                female_count = result['count']
        
        # 关闭数据库连接
        cursor.close()
        conn.close()
        
        return {
            "code": 200,
            "data": {
                "male_count": male_count,
                "female_count": female_count
            }
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器错误")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(router, host="0.0.0.0", port=8001)
