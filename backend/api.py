from fastapi import APIRouter, Query, HTTPException, Depends, Header
from typing import List, Optional
from pydantic import BaseModel
import mysql.connector
from datetime import datetime
import json

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
class HealthRecord(BaseModel):
    report_date: str
    gender: Optional[str] = None
    age: Optional[int] = None
    record_id: Optional[str] = None

class HealthHistoryResponse(BaseModel):
    code: int = 200
    data: List[HealthRecord]
    total: int

async def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="无效的认证格式")
    token = authorization.split(" ")[1]
    # 这里应该添加实际的token验证逻辑
    if not token:
        raise HTTPException(status_code=401, detail="无效的token")
    return token

def connect_to_database():
    """连接到数据库"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"数据库连接错误: {err}")
        return None

@router.get("/api/health/history", response_model=HealthHistoryResponse)
async def get_health_history(
    startDate: str = Query(..., description="开始日期 (YYYY-MM-DD)"),
    endDate: str = Query(..., description="结束日期 (YYYY-MM-DD)"),
    token: str = Depends(verify_token)
):
    try:
        # 验证日期格式
        try:
            datetime.strptime(startDate, '%Y-%m-%d')
            datetime.strptime(endDate, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误")
            
        # 连接数据库
        conn = connect_to_database()
        if not conn:
            raise HTTPException(status_code=500, detail="数据库连接失败")
            
        cursor = conn.cursor(dictionary=True)
        
        # 构建查询SQL
        sql = """
        SELECT 
            bi.report_date,
            bi.gender,
            bi.age,
            er.record_id
        FROM basic_info bi
        LEFT JOIN exam_record er ON bi.report_date = er.report_date
        WHERE bi.report_date BETWEEN %s AND %s
        ORDER BY bi.report_date DESC
        """
        
        # 执行查询
        cursor.execute(sql, (startDate, endDate))
        history_records = cursor.fetchall()
        
        # 处理查询结果
        formatted_history = []
        for record in history_records:
            if 'report_date' in record and record['report_date']:
                record['report_date'] = record['report_date'].strftime('%Y-%m-%d')
            if 'age' in record:
                record['age'] = int(record['age']) if record['age'] is not None else None
            formatted_history.append(record)
        
        # 关闭数据库连接
        cursor.close()
        conn.close()
        
        return {
            "code": 200,
            "data": formatted_history,
            "total": len(formatted_history)
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器错误") 