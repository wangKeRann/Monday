from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'health_exam'
}

def connect_to_database():
    """连接到数据库"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as err:
        logger.error(f"数据库连接错误: {err}")
        raise HTTPException(status_code=500, detail=f"数据库连接错误: {err}")

class AgeDistribution(BaseModel):
    age_range: str
    count: int
    total: int

class ResponseData(BaseModel):
    age_distribution: List[AgeDistribution]
    total_count: int
    abnormal_count: int

class SimpleResponse(BaseModel):
    code: int = 200
    data: ResponseData

@router.get("/api/health/abnormal-ranking", response_model=SimpleResponse)
async def get_abnormal_ranking(
    indicator_type: str = Query(..., description="指标类型，如：blood_routine, urine_routine, biochemistry")
):
    conn = None
    try:
        # 验证指标类型
        valid_types = ['blood_routine', 'urine_routine', 'biochemistry', 'ultrasound', 'liver_fibrosis']
        if indicator_type not in valid_types:
            raise HTTPException(status_code=400, detail=f"无效的指标类型。有效类型: {', '.join(valid_types)}")

        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)

        # 获取总人数
        total_sql = f"""
        SELECT COUNT(DISTINCT er.record_id) as total
        FROM exam_record er
        WHERE er.record_id IN (
            SELECT record_id FROM {indicator_type}
        )
        """
        cursor.execute(total_sql)
        total_count = cursor.fetchone()['total']

        # 获取各年龄段的人数统计
        age_sql = f"""
        SELECT 
            CASE 
                WHEN bi.age < 19 THEN '0-18'
                WHEN bi.age BETWEEN 19 AND 30 THEN '19-30'
                WHEN bi.age BETWEEN 31 AND 45 THEN '31-45'
                WHEN bi.age BETWEEN 46 AND 60 THEN '46-60'
                ELSE '60+'
            END as age_range,
            COUNT(DISTINCT er.record_id) as total
        FROM exam_record er
        LEFT JOIN basic_info bi ON er.report_date = bi.report_date
        WHERE er.record_id IN (
            SELECT record_id FROM {indicator_type}
        )
        GROUP BY 
            CASE 
                WHEN bi.age < 19 THEN '0-18'
                WHEN bi.age BETWEEN 19 AND 30 THEN '19-30'
                WHEN bi.age BETWEEN 31 AND 45 THEN '31-45'
                WHEN bi.age BETWEEN 46 AND 60 THEN '46-60'
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
        
        cursor.execute(age_sql)
        results = cursor.fetchall()
        
        # 构建返回数据
        age_distribution = []
        for result in results:
            age_distribution.append({
                "age_range": result['age_range'],
                "count": result['total'],  # 使用total作为count
                "total": result['total']
            })

        return {
            "code": 200,
            "data": {
                "age_distribution": age_distribution,
                "total_count": total_count,
                "abnormal_count": total_count  # 将总人数作为异常人数返回
            }
        }

    except Error as err:
        logger.error(f"数据库查询错误: {err}")
        raise HTTPException(status_code=500, detail=f"数据库查询错误: {err}")
    except Exception as e:
        logger.error(f"未预期的错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(router, host="0.0.0.0", port=8006)