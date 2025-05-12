from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
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
class BloodRoutine(BaseModel):
    white_blood_cell: Optional[float] = None
    red_blood_cell: Optional[float] = None
    platelet_count: Optional[float] = None
    neutrophil_percentage: Optional[float] = None
    lymphocyte_percentage: Optional[float] = None
    monocyte_percentage: Optional[float] = None
    eosinophil_percentage: Optional[float] = None
    basophil_percentage: Optional[float] = None
    hemoglobin: Optional[float] = None
    hematocrit: Optional[float] = None
    mcv: Optional[float] = None
    mch: Optional[float] = None
    mchc: Optional[float] = None
    rdw: Optional[float] = None
    platelet_crit: Optional[float] = None
    mpv: Optional[float] = None
    pdw: Optional[float] = None

class UrineRoutine(BaseModel):
    urine_sugar: Optional[str] = None
    urine_bilirubin: Optional[str] = None
    urine_ketone: Optional[str] = None
    urine_specific_gravity: Optional[float] = None
    urine_ph: Optional[float] = None
    urine_protein: Optional[str] = None
    urine_urobilinogen: Optional[str] = None
    urine_nitrite: Optional[str] = None
    urine_blood: Optional[str] = None
    urine_leukocyte_esterase: Optional[str] = None
    red_blood_cell_microscopy: Optional[str] = None
    white_blood_cell_microscopy: Optional[str] = None
    pus_cell_microscopy: Optional[str] = None
    epithelial_cell_microscopy: Optional[str] = None
    granular_cast_microscopy: Optional[str] = None
    hyaline_cast_microscopy: Optional[str] = None
    mucus_thread_microscopy: Optional[str] = None
    fungus_microscopy: Optional[str] = None

class Biochemistry(BaseModel):
    total_bilirubin: Optional[float] = None
    direct_bilirubin: Optional[float] = None
    indirect_bilirubin: Optional[float] = None
    total_protein: Optional[float] = None
    albumin: Optional[float] = None
    globulin: Optional[float] = None
    albumin_globulin_ratio: Optional[float] = None
    alt: Optional[float] = None
    ast: Optional[float] = None
    alp: Optional[float] = None
    ggt: Optional[float] = None
    ldh: Optional[float] = None
    ck: Optional[float] = None
    ck_mb: Optional[float] = None
    total_bile_acid: Optional[float] = None
    creatinine: Optional[float] = None
    urea: Optional[float] = None
    uric_acid: Optional[float] = None
    blood_glucose: Optional[float] = None
    total_cholesterol: Optional[float] = None
    triglyceride: Optional[float] = None
    hdl_cholesterol: Optional[float] = None
    ldl_cholesterol: Optional[float] = None

class Ultrasound(BaseModel):
    liver_status: Optional[str] = None
    thyroid_status: Optional[str] = None
    prostate_status: Optional[str] = None
    neck_vessel_status: Optional[str] = None
    bladder_ureter_status: Optional[str] = None

class LiverFibrosis(BaseModel):
    fibrosis_index: Optional[float] = None
    hyaluronic_acid: Optional[float] = None
    type_iv_collagen: Optional[float] = None
    laminin: Optional[float] = None
    procollagen_iii: Optional[float] = None

class HealthDetail(BaseModel):
    record_id: str
    report_date: date
    gender: Optional[str] = None
    age: Optional[int] = None
    blood_routine: Optional[BloodRoutine] = None
    urine_routine: Optional[UrineRoutine] = None
    biochemistry: Optional[Biochemistry] = None
    ultrasound: Optional[Ultrasound] = None
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
        
        print(f"Debug - 开始查询记录ID: {record_id}")
        
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
        print(f"Debug - 基本信息查询结果: {basic_info}")
        
        if not basic_info:
            raise HTTPException(status_code=404, detail="记录不存在")
        
        # 获取血常规数据
        blood_sql = """
        SELECT 
            white_blood_cell,
            red_blood_cell,
            platelet_count,
            neutrophil_percentage,
            lymphocyte_percentage,
            monocyte_percentage,
            eosinophil_percentage,
            basophil_percentage,
            hemoglobin,
            hematocrit,
            mcv,
            mch,
            mchc,
            rdw,
            platelet_crit,
            mpv,
            pdw
        FROM blood_routine 
        WHERE record_id = %s
        """
        cursor.execute(blood_sql, (record_id,))
        blood_data = cursor.fetchone()
        print(f"Debug - 血常规数据查询结果: {blood_data}")
        
        # 获取尿常规数据
        urine_sql = """
        SELECT 
            urine_sugar,
            urine_bilirubin,
            urine_ketone,
            urine_specific_gravity,
            urine_ph,
            urine_protein,
            urine_urobilinogen,
            urine_nitrite,
            urine_blood,
            urine_leukocyte_esterase,
            red_blood_cell_microscopy,
            white_blood_cell_microscopy,
            pus_cell_microscopy,
            epithelial_cell_microscopy,
            granular_cast_microscopy,
            hyaline_cast_microscopy,
            mucus_thread_microscopy,
            fungus_microscopy
        FROM urine_routine 
        WHERE record_id = %s
        """
        cursor.execute(urine_sql, (record_id,))
        urine_data = cursor.fetchone()
        print(f"Debug - 尿常规数据查询结果: {urine_data}")
        
        # 获取生化指标数据
        bio_sql = """
        SELECT 
            total_bilirubin,
            direct_bilirubin,
            indirect_bilirubin,
            total_protein,
            albumin,
            globulin,
            albumin_globulin_ratio,
            alt,
            ast,
            alp,
            ggt,
            ldh,
            ck,
            ck_mb,
            total_bile_acid,
            creatinine,
            urea,
            uric_acid,
            blood_glucose,
            total_cholesterol,
            triglyceride,
            hdl_cholesterol,
            ldl_cholesterol
        FROM biochemistry 
        WHERE record_id = %s
        """
        cursor.execute(bio_sql, (record_id,))
        bio_data = cursor.fetchone()
        print(f"Debug - 生化指标数据查询结果: {bio_data}")
        
        # 获取超声检查数据
        us_sql = """
        SELECT 
            liver_status,
            thyroid_status,
            prostate_status,
            neck_vessel_status,
            bladder_ureter_status
        FROM ultrasound 
        WHERE record_id = %s
        """
        cursor.execute(us_sql, (record_id,))
        us_data = cursor.fetchone()
        print(f"Debug - 超声检查数据查询结果: {us_data}")
        
        # 获取肝纤维化数据
        lf_sql = """
        SELECT 
            fibrosis_index,
            hyaluronic_acid,
            type_iv_collagen,
            laminin,
            procollagen_iii
        FROM liver_fibrosis 
        WHERE record_id = %s
        """
        cursor.execute(lf_sql, (record_id,))
        lf_data = cursor.fetchone()
        print(f"Debug - 肝纤维化数据查询结果: {lf_data}")
        
        # 构建响应数据
        response_data = {
            "record_id": basic_info["record_id"],
            "report_date": basic_info["report_date"].isoformat() if basic_info["report_date"] else None,
            "gender": basic_info["gender"],
            "age": basic_info["age"],
            "blood_routine": blood_data if blood_data else None,
            "urine_routine": urine_data if urine_data else None,
            "biochemistry": bio_data if bio_data else None,
            "ultrasound": us_data if us_data else None,
            "liver_fibrosis": lf_data if lf_data else None
        }
        
        print(f"Debug - 最终响应数据: {response_data}")
        
        return DetailResponse(
            code=200,
            message="success",
            data=response_data
        )
        
    except Error as err:
        print(f"Debug - 数据库错误: {err}")
        raise HTTPException(status_code=500, detail=f"数据库查询错误: {err}")
    finally:
        if conn:
            conn.close()
            print("Debug - 数据库连接已关闭")
