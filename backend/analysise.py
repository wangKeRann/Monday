from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict
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
class ReferenceRange(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None

class TrendDataPoint(BaseModel):
    date: str
    value: float
    reference_range: ReferenceRange

class TrendAnalysisResponse(BaseModel):
    code: int
    message: str
    data: List[TrendDataPoint]

# 健康记录详情相关模型
class BloodRoutine(BaseModel):
    white_blood_cell: Optional[float] = None
    red_blood_cell: Optional[float] = None
    platelet_count: Optional[float] = None
    hemoglobin: Optional[float] = None

class UrineRoutine(BaseModel):
    urine_ph: Optional[float] = None
    urine_specific_gravity: Optional[float] = None

class Biochemistry(BaseModel):
    alt: Optional[float] = None
    ast: Optional[float] = None
    blood_glucose: Optional[float] = None
    total_cholesterol: Optional[float] = None

class LiverFibrosis(BaseModel):
    fibrosis_index: Optional[float] = None
    hyaluronic_acid: Optional[float] = None

class HealthDetail(BaseModel):
    record_id: str
    report_date: date
    gender: Optional[str] = None
    age: Optional[int] = None
    blood_routine: Optional[BloodRoutine] = None
    urine_routine: Optional[UrineRoutine] = None
    biochemistry: Optional[Biochemistry] = None
    liver_fibrosis: Optional[LiverFibrosis] = None

class DetailResponse(BaseModel):
    code: int
    message: str
    data: HealthDetail

def connect_to_database():
    """连接到数据库"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as err:
        raise HTTPException(status_code=500, detail=f"数据库连接错误: {err}")

@router.get("/api/health/detail/{record_id}", response_model=DetailResponse)
async def get_health_detail(record_id: str):
    """
    获取健康报告详情
    
    参数:
    - record_id: 记录ID
    """
    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        
        # 获取基本信息
        basic_sql = """
        SELECT 
            er.record_id,
            er.report_date,
            bi.gender,
            bi.age
        FROM exam_record er
        LEFT JOIN basic_info bi ON er.report_date = bi.report_date
        WHERE er.record_id = %s
        """
        cursor.execute(basic_sql, (record_id,))
        basic_info = cursor.fetchone()
        
        if not basic_info:
            raise HTTPException(status_code=404, detail="记录不存在")
        
        # 获取血常规数据
        blood_sql = """
        SELECT 
            white_blood_cell,
            red_blood_cell,
            platelet_count,
            hemoglobin
        FROM blood_routine 
        WHERE record_id = %s
        """
        cursor.execute(blood_sql, (record_id,))
        blood_data = cursor.fetchone()
        
        # 获取尿常规数据
        urine_sql = """
        SELECT 
            urine_ph,
            urine_specific_gravity
        FROM urine_routine 
        WHERE record_id = %s
        """
        cursor.execute(urine_sql, (record_id,))
        urine_data = cursor.fetchone()
        
        # 获取生化指标数据
        bio_sql = """
        SELECT 
            alt,
            ast,
            blood_glucose,
            total_cholesterol
        FROM biochemistry 
        WHERE record_id = %s
        """
        cursor.execute(bio_sql, (record_id,))
        bio_data = cursor.fetchone()
        
        # 获取肝纤维化数据
        lf_sql = """
        SELECT 
            fibrosis_index,
            hyaluronic_acid
        FROM liver_fibrosis 
        WHERE record_id = %s
        """
        cursor.execute(lf_sql, (record_id,))
        lf_data = cursor.fetchone()
        
        # 构建响应数据
        response_data = {
            "record_id": basic_info["record_id"],
            "report_date": basic_info["report_date"],
            "gender": basic_info["gender"],
            "age": basic_info["age"],
            "blood_routine": blood_data if blood_data else None,
            "urine_routine": urine_data if urine_data else None,
            "biochemistry": bio_data if bio_data else None,
            "liver_fibrosis": lf_data if lf_data else None
        }
        
        return DetailResponse(
            code=200,
            message="success",
            data=response_data
        )
        
    except Error as err:
        raise HTTPException(status_code=500, detail=f"数据库查询错误: {err}")
    finally:
        if conn:
            conn.close()

# 指标配置
INDICATOR_CONFIG = {
    'blood_routine': {
        'table': 'blood_routine',
        'indicators': {
            'white_blood_cell': {'min': 4.0, 'max': 10.0},
            'red_blood_cell': {'min': 3.5, 'max': 5.5},
            'hemoglobin': {'min': 110, 'max': 160},
            'platelet_count': {'min': 100, 'max': 300}
        }
    },
    'urine_routine': {
        'table': 'urine_routine',
        'indicators': {
            'urine_ph': {'min': 4.5, 'max': 8.0},
            'urine_specific_gravity': {'min': 1.005, 'max': 1.030}
        }
    },
    'biochemistry': {
        'table': 'biochemistry',
        'indicators': {
            'alt': {'min': 0, 'max': 40},
            'ast': {'min': 0, 'max': 40},
            'blood_glucose': {'min': 3.9, 'max': 6.1},
            'total_cholesterol': {'min': 0, 'max': 5.2}
        }
    },
    'liver_fibrosis': {
        'table': 'liver_fibrosis',
        'indicators': {
            'fibrosis_index': {'min': 0, 'max': 2.0},
            'hyaluronic_acid': {'min': 0, 'max': 100}
        }
    }
}

@router.get("/api/health/trend-analysis", response_model=TrendAnalysisResponse)
async def get_trend_analysis(
    start_date: str = Query(..., description="开始日期 (YYYY-MM-DD)"),
    end_date: str = Query(..., description="结束日期 (YYYY-MM-DD)"),
    indicator_type: str = Query(..., description="指标类型 (blood_routine/urine_routine/biochemistry/liver_fibrosis)"),
    indicator_name: str = Query(..., description="具体指标名称")
):
    """
    获取健康指标趋势分析
    
    参数:
    - start_date: 开始日期
    - end_date: 结束日期
    - indicator_type: 指标类型
    - indicator_name: 具体指标名称
    """
    try:
        # 验证指标类型
        if indicator_type not in INDICATOR_CONFIG:
            raise HTTPException(status_code=400, detail="无效的指标类型")
            
        # 验证具体指标
        if indicator_name not in INDICATOR_CONFIG[indicator_type]['indicators']:
            raise HTTPException(status_code=400, detail="无效的指标名称")
            
        # 获取参考范围
        reference_range = INDICATOR_CONFIG[indicator_type]['indicators'][indicator_name]
        
        # 连接数据库
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        
        # 构建查询SQL
        table_name = INDICATOR_CONFIG[indicator_type]['table']
        sql = f"""
        SELECT 
            er.report_date,
            {table_name}.{indicator_name}
        FROM exam_record er
        JOIN {table_name} ON er.record_id = {table_name}.record_id
        WHERE er.report_date BETWEEN %s AND %s
        AND {table_name}.{indicator_name} IS NOT NULL
        ORDER BY er.report_date ASC
        """
        
        # 执行查询
        cursor.execute(sql, (start_date, end_date))
        results = cursor.fetchall()
        
        # 处理查询结果
        trend_data = []
        for record in results:
            trend_data.append(TrendDataPoint(
                date=record['report_date'].strftime('%Y-%m-%d'),
                value=float(record[indicator_name]),
                reference_range=ReferenceRange(
                    min=reference_range['min'],
                    max=reference_range['max']
                )
            ))
        
        return TrendAnalysisResponse(
            code=200,
            message="success",
            data=trend_data
        )
        
    except Error as err:
        raise HTTPException(status_code=500, detail=f"数据库查询错误: {err}")
    finally:
        if conn:
            conn.close()
