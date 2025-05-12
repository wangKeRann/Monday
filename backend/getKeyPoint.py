from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
import mysql.connector
from mysql.connector import Error

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'health_exam'
}

# 创建路由
router = APIRouter()

# 定义响应模型
class IndicatorRecord(BaseModel):
    record_id: str
    report_date: date
    gender: Optional[str] = None
    age: Optional[int] = None

class IndicatorResponse(BaseModel):
    code: int
    message: str
    data: List[IndicatorRecord]
    total: int

def connect_to_database():
    """连接到数据库"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as err:
        raise HTTPException(status_code=500, detail=f"数据库连接错误: {err}")

@router.get("/api/health/indicators", response_model=IndicatorResponse)
async def get_indicators(type: str):
    """
    获取关键指标数据
    
    参数:
    - type: 指标类型，可选值：
        - blood_routine: 血常规
        - urine_routine: 尿常规
        - biochemistry: 生化指标
        - ultrasound: 超声检查
        - liver_fibrosis: 肝纤维化
    """
    # 验证指标类型
    valid_types = ['blood_routine', 'urine_routine', 'biochemistry', 'ultrasound', 'liver_fibrosis']
    if type not in valid_types:
        raise HTTPException(status_code=400, detail=f"无效的指标类型。有效类型: {', '.join(valid_types)}")
    
    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        
        # 构建查询SQL
        sql = """
        SELECT 
            er.record_id,
            er.report_date,
            bi.gender,
            bi.age
        FROM exam_record er
        LEFT JOIN basic_info bi ON er.report_date = bi.report_date
        WHERE er.record_id IN (
            SELECT record_id FROM {}
        )
        ORDER BY er.report_date DESC
        """.format(type)
        
        # 执行查询
        cursor.execute(sql)
        records = cursor.fetchall()
        
        # 获取总记录数
        count_sql = f"SELECT COUNT(*) as total FROM {type}"
        cursor.execute(count_sql)
        total = cursor.fetchone()['total']
        
        # 转换日期格式
        for record in records:
            if record['report_date']:
                record['report_date'] = record['report_date'].isoformat()
        
        return IndicatorResponse(
            code=200,
            message="success",
            data=records,
            total=total
        )
        
    except Error as err:
        raise HTTPException(status_code=500, detail=f"数据库查询错误: {err}")
    finally:
        if conn:
            conn.close()
