import pandas as pd
import mysql.connector
from datetime import datetime
import uuid
import os

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'health_exam'
}

def generate_record_id():
    """生成唯一的记录ID"""
    return str(uuid.uuid4()).replace('-', '')

def connect_to_database():
    """连接到数据库"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"数据库连接错误: {err}")
        return None

def create_tables(conn):
    """创建数据库表"""
    cursor = conn.cursor()
    
    # 创建基础信息表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS basic_info (
        report_date DATE PRIMARY KEY,
        gender VARCHAR(10),
        age INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 创建体检记录主表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_record (
        record_id VARCHAR(32) PRIMARY KEY,
        report_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (report_date) REFERENCES basic_info(report_date)
    )
    """)
    
    # 创建血常规表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blood_routine (
        record_id VARCHAR(32) PRIMARY KEY,
        white_blood_cell DECIMAL(5,2),
        neutrophil_percentage DECIMAL(5,2),
        lymphocyte_percentage DECIMAL(5,2),
        monocyte_percentage DECIMAL(5,2),
        eosinophil_percentage DECIMAL(5,2),
        basophil_percentage DECIMAL(5,2),
        neutrophil_absolute DECIMAL(5,2),
        lymphocyte_absolute DECIMAL(5,2),
        monocyte_absolute DECIMAL(5,2),
        eosinophil_absolute DECIMAL(5,2),
        basophil_absolute DECIMAL(5,2),
        red_blood_cell DECIMAL(5,2),
        hemoglobin DECIMAL(5,2),
        hematocrit DECIMAL(5,2),
        mcv DECIMAL(5,2),
        mch DECIMAL(5,2),
        mchc DECIMAL(5,2),
        rdw DECIMAL(5,2),
        platelet_count DECIMAL(5,2),
        platelet_crit DECIMAL(5,2),
        mpv DECIMAL(5,2),
        pdw DECIMAL(5,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (record_id) REFERENCES exam_record(record_id)
    )
    """)
    
    # 创建尿常规表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS urine_routine (
        record_id VARCHAR(32) PRIMARY KEY,
        urine_sugar VARCHAR(20),
        urine_bilirubin VARCHAR(20),
        urine_ketone VARCHAR(20),
        urine_specific_gravity DECIMAL(5,2),
        urine_ph DECIMAL(5,2),
        urine_protein VARCHAR(20),
        urine_urobilinogen VARCHAR(20),
        urine_nitrite VARCHAR(20),
        urine_blood VARCHAR(20),
        urine_leukocyte_esterase VARCHAR(20),
        red_blood_cell_microscopy VARCHAR(20),
        white_blood_cell_microscopy VARCHAR(20),
        pus_cell_microscopy VARCHAR(20),
        epithelial_cell_microscopy VARCHAR(20),
        granular_cast_microscopy VARCHAR(20),
        hyaline_cast_microscopy VARCHAR(20),
        mucus_thread_microscopy VARCHAR(20),
        fungus_microscopy VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (record_id) REFERENCES exam_record(record_id)
    )
    """)
    
    # 创建生化指标表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS biochemistry (
        record_id VARCHAR(32) PRIMARY KEY,
        total_bilirubin DECIMAL(5,2),
        direct_bilirubin DECIMAL(5,2),
        indirect_bilirubin DECIMAL(5,2),
        total_protein DECIMAL(5,2),
        albumin DECIMAL(5,2),
        globulin DECIMAL(5,2),
        albumin_globulin_ratio DECIMAL(5,2),
        alt DECIMAL(5,2),
        alp DECIMAL(5,2),
        ggt DECIMAL(5,2),
        ast DECIMAL(5,2),
        ldh DECIMAL(5,2),
        ck DECIMAL(5,2),
        ck_mb DECIMAL(5,2),
        total_bile_acid DECIMAL(5,2),
        fibronectin DECIMAL(5,2),
        haptoglobin DECIMAL(5,2),
        alpha1_acid_glycoprotein DECIMAL(5,2),
        potassium DECIMAL(5,2),
        sodium DECIMAL(5,2),
        chloride DECIMAL(5,2),
        calcium DECIMAL(5,2),
        urea DECIMAL(5,2),
        creatinine DECIMAL(5,2),
        uric_acid DECIMAL(5,2),
        cystatin_c DECIMAL(5,2),
        blood_glucose DECIMAL(5,2),
        fructosamine DECIMAL(5,2),
        total_cholesterol DECIMAL(5,2),
        triglyceride DECIMAL(5,2),
        hdl_cholesterol DECIMAL(5,2),
        ldl_cholesterol DECIMAL(5,2),
        apolipoprotein_a DECIMAL(5,2),
        apolipoprotein_b DECIMAL(5,2),
        lipoprotein_a DECIMAL(5,2),
        small_dense_ldl DECIMAL(5,2),
        aso DECIMAL(5,2),
        rf DECIMAL(5,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (record_id) REFERENCES exam_record(record_id)
    )
    """)
    
    # 创建超声检查表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ultrasound (
        record_id VARCHAR(32) PRIMARY KEY,
        liver_status TEXT,
        thyroid_status TEXT,
        prostate_status TEXT,
        neck_vessel_status TEXT,
        bladder_ureter_status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (record_id) REFERENCES exam_record(record_id)
    )
    """)
    
    # 创建肝纤维化表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS liver_fibrosis (
        record_id VARCHAR(32) PRIMARY KEY,
        fibrosis_index DECIMAL(5,2),
        hyaluronic_acid DECIMAL(5,2),
        type_iv_collagen DECIMAL(5,2),
        laminin DECIMAL(5,2),
        procollagen_iii DECIMAL(5,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (record_id) REFERENCES exam_record(record_id)
    )
    """)
    
    conn.commit()
    cursor.close()

def create_database():
    """创建数据库"""
    try:
        # 首先连接到MySQL服务器（不指定数据库）
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"数据库 {DB_CONFIG['database']} 创建成功或已存在")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"创建数据库时发生错误: {err}")
        return False
    return True

def import_basic_info(conn, df):
    """导入基础信息"""
    cursor = conn.cursor()
    
    # 准备数据
    basic_info_data = []
    for index, row in df.iterrows():
        try:
            # 检查日期列是否存在
            if 'OT01' not in row:
                print(f"警告：第{index+1}行缺少日期列(OT01)")
                continue
                
            # 尝试解析日期
            try:
                # 检查日期值是否为空
                if pd.isna(row['OT01']):
                    print(f"警告：第{index+1}行的日期为空值")
                    continue
                    
                # 将日期转换为datetime对象
                date_obj = pd.to_datetime(row['OT01'], errors='coerce')
                if pd.isna(date_obj):
                    print(f"警告：第{index+1}行的日期格式无效: {row['OT01']}")
                    continue
                
                # 转换为date对象
                report_date = date_obj.date()
                
            except Exception as e:
                print(f"警告：第{index+1}行的日期解析错误: {e}")
                continue
                
            # 检查性别和年龄
            if 'OT02' not in row or 'OT03' not in row:
                print(f"警告：第{index+1}行缺少性别或年龄信息")
                continue
                
            gender = str(row['OT02']).strip() if pd.notna(row['OT02']) else None
            try:
                age = int(row['OT03']) if pd.notna(row['OT03']) else None
            except (ValueError, TypeError):
                print(f"警告：第{index+1}行的年龄格式无效: {row['OT03']}")
                continue
            
            basic_info_data.append((report_date, gender, age))
            
        except Exception as e:
            print(f"警告：处理第{index+1}行时发生错误: {e}")
            continue
    
    if not basic_info_data:
        print("错误：没有有效的数据可以导入")
        return
        
    # 插入数据
    sql = """
    INSERT INTO basic_info (report_date, gender, age)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
    gender = VALUES(gender),
    age = VALUES(age)
    """
    
    try:
        cursor.executemany(sql, basic_info_data)
        conn.commit()
        print(f"成功导入 {len(basic_info_data)} 条基础信息记录")
    except Exception as e:
        print(f"导入基础信息时发生错误: {e}")
        conn.rollback()
    finally:
        cursor.close()

def import_exam_record(conn, df):
    """导入体检记录"""
    cursor = conn.cursor()
    
    # 准备数据
    exam_record_data = []
    record_mapping = {}
    
    for index, row in df.iterrows():
        try:
            # 检查日期列是否存在且有效
            if 'OT01' not in row:
                print(f"警告：第{index+1}行缺少日期列")
                continue
                
            # 检查日期值是否为空
            if pd.isna(row['OT01']):
                print(f"警告：第{index+1}行的日期为空值")
                continue
                
            # 生成记录ID
            record_id = generate_record_id()
            
            # 解析日期
            try:
                date_obj = pd.to_datetime(row['OT01'], errors='coerce')
                if pd.isna(date_obj):
                    print(f"警告：第{index+1}行的日期格式无效: {row['OT01']}")
                    continue
                report_date = date_obj.date()
            except Exception as e:
                print(f"警告：第{index+1}行的日期解析错误: {e}")
                continue
            
            # 添加到数据列表和映射字典
            exam_record_data.append((record_id, report_date))
            record_mapping[report_date] = record_id
            
        except Exception as e:
            print(f"警告：处理第{index+1}行时发生错误: {e}")
            continue
    
    if not exam_record_data:
        print("错误：没有有效的体检记录可以导入")
        return None
    
    # 插入数据
    sql = """
    INSERT INTO exam_record (record_id, report_date)
    VALUES (%s, %s)
    """
    
    try:
        cursor.executemany(sql, exam_record_data)
        conn.commit()
        print(f"成功导入 {len(exam_record_data)} 条体检记录")
        return record_mapping
    except Exception as e:
        print(f"导入体检记录时发生错误: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def import_blood_routine(conn, df, record_mapping):
    """导入血常规数据"""
    cursor = conn.cursor()
    
    # 准备数据
    blood_routine_data = []
    for index, row in df.iterrows():
        try:
            report_date = pd.to_datetime(row['OT01']).date()
            if report_date not in record_mapping:
                print(f"警告：第{index+1}行的日期 {report_date} 没有对应的记录ID")
                continue
                
            record_id = record_mapping[report_date]
            
            # 获取血常规相关列
            blood_data = [record_id]
            # 定义血常规指标列名
            bc_columns = [
                'BC_white_blood_cell', 'BC_neutrophil_percentage', 'BC_lymphocyte_percentage',
                'BC_monocyte_percentage', 'BC_eosinophil_percentage', 'BC_basophil_percentage',
                'BC_neutrophil_absolute', 'BC_lymphocyte_absolute', 'BC_monocyte_absolute',
                'BC_eosinophil_absolute', 'BC_basophil_absolute', 'BC_red_blood_cell',
                'BC_hemoglobin', 'BC_hematocrit', 'BC_mcv', 'BC_mch',
                'BC_mchc', 'BC_rdw', 'BC_platelet_count',
                'BC_platelet_crit', 'BC_mpv', 'BC_pdw'
            ]
            
            # 按顺序获取数据
            for col in bc_columns:
                value = row.get(col)
                if pd.isna(value):
                    blood_data.append(None)
                else:
                    try:
                        blood_data.append(float(value))
                    except (ValueError, TypeError):
                        blood_data.append(None)
            
            blood_routine_data.append(tuple(blood_data))
        except Exception as e:
            print(f"警告：处理第{index+1}行血常规数据时发生错误: {e}")
            continue
    
    if not blood_routine_data:
        print("错误：没有有效的血常规数据可以导入")
        return
    
    # 插入数据
    sql = """
    INSERT INTO blood_routine (
        record_id, white_blood_cell, neutrophil_percentage,
        lymphocyte_percentage, monocyte_percentage,
        eosinophil_percentage, basophil_percentage,
        neutrophil_absolute, lymphocyte_absolute,
        monocyte_absolute, eosinophil_absolute,
        basophil_absolute, red_blood_cell,
        hemoglobin, hematocrit, mcv, mch,
        mchc, rdw, platelet_count,
        platelet_crit, mpv, pdw
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        white_blood_cell = VALUES(white_blood_cell),
        neutrophil_percentage = VALUES(neutrophil_percentage),
        lymphocyte_percentage = VALUES(lymphocyte_percentage),
        monocyte_percentage = VALUES(monocyte_percentage),
        eosinophil_percentage = VALUES(eosinophil_percentage),
        basophil_percentage = VALUES(basophil_percentage),
        neutrophil_absolute = VALUES(neutrophil_absolute),
        lymphocyte_absolute = VALUES(lymphocyte_absolute),
        monocyte_absolute = VALUES(monocyte_absolute),
        eosinophil_absolute = VALUES(eosinophil_absolute),
        basophil_absolute = VALUES(basophil_absolute),
        red_blood_cell = VALUES(red_blood_cell),
        hemoglobin = VALUES(hemoglobin),
        hematocrit = VALUES(hematocrit),
        mcv = VALUES(mcv),
        mch = VALUES(mch),
        mchc = VALUES(mchc),
        rdw = VALUES(rdw),
        platelet_count = VALUES(platelet_count),
        platelet_crit = VALUES(platelet_crit),
        mpv = VALUES(mpv),
        pdw = VALUES(pdw)
    """
    
    try:
        cursor.executemany(sql, blood_routine_data)
        conn.commit()
        print(f"成功导入 {len(blood_routine_data)} 条血常规数据")
    except Exception as e:
        print(f"导入血常规数据时发生错误: {e}")
        conn.rollback()
    finally:
        cursor.close()

def import_urine_routine(conn, df, record_mapping):
    """导入尿常规数据"""
    cursor = conn.cursor()
    
    # 准备数据
    urine_routine_data = []
    for index, row in df.iterrows():
        try:
            report_date = pd.to_datetime(row['OT01']).date()
            if report_date not in record_mapping:
                print(f"警告：第{index+1}行的日期 {report_date} 没有对应的记录ID")
                continue
                
            record_id = record_mapping[report_date]
            
            # 获取尿常规相关列
            urine_data = [record_id]
            # 定义尿常规指标列名
            uc_columns = [
                'UC_sugar', 'UC_bilirubin', 'UC_ketone',
                'UC_specific_gravity', 'UC_ph', 'UC_protein',
                'UC_urobilinogen', 'UC_nitrite', 'UC_blood',
                'UC_leukocyte_esterase', 'UC_red_blood_cell_microscopy',
                'UC_white_blood_cell_microscopy', 'UC_pus_cell_microscopy',
                'UC_epithelial_cell_microscopy', 'UC_granular_cast_microscopy',
                'UC_hyaline_cast_microscopy', 'UC_mucus_thread_microscopy',
                'UC_fungus_microscopy'
            ]
            
            # 按顺序获取数据
            for col in uc_columns:
                value = row.get(col)
                if pd.isna(value):
                    urine_data.append(None)
                else:
                    urine_data.append(str(value))
            
            urine_routine_data.append(tuple(urine_data))
        except Exception as e:
            print(f"警告：处理第{index+1}行尿常规数据时发生错误: {e}")
            continue
    
    if not urine_routine_data:
        print("错误：没有有效的尿常规数据可以导入")
        return
    
    # 插入数据
    sql = """
    INSERT INTO urine_routine (
        record_id, urine_sugar, urine_bilirubin,
        urine_ketone, urine_specific_gravity,
        urine_ph, urine_protein, urine_urobilinogen,
        urine_nitrite, urine_blood,
        urine_leukocyte_esterase,
        red_blood_cell_microscopy,
        white_blood_cell_microscopy,
        pus_cell_microscopy,
        epithelial_cell_microscopy,
        granular_cast_microscopy,
        hyaline_cast_microscopy,
        mucus_thread_microscopy,
        fungus_microscopy
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        urine_sugar = VALUES(urine_sugar),
        urine_bilirubin = VALUES(urine_bilirubin),
        urine_ketone = VALUES(urine_ketone),
        urine_specific_gravity = VALUES(urine_specific_gravity),
        urine_ph = VALUES(urine_ph),
        urine_protein = VALUES(urine_protein),
        urine_urobilinogen = VALUES(urine_urobilinogen),
        urine_nitrite = VALUES(urine_nitrite),
        urine_blood = VALUES(urine_blood),
        urine_leukocyte_esterase = VALUES(urine_leukocyte_esterase),
        red_blood_cell_microscopy = VALUES(red_blood_cell_microscopy),
        white_blood_cell_microscopy = VALUES(white_blood_cell_microscopy),
        pus_cell_microscopy = VALUES(pus_cell_microscopy),
        epithelial_cell_microscopy = VALUES(epithelial_cell_microscopy),
        granular_cast_microscopy = VALUES(granular_cast_microscopy),
        hyaline_cast_microscopy = VALUES(hyaline_cast_microscopy),
        mucus_thread_microscopy = VALUES(mucus_thread_microscopy),
        fungus_microscopy = VALUES(fungus_microscopy)
    """
    
    try:
        cursor.executemany(sql, urine_routine_data)
        conn.commit()
        print(f"成功导入 {len(urine_routine_data)} 条尿常规数据")
    except Exception as e:
        print(f"导入尿常规数据时发生错误: {e}")
        conn.rollback()
    finally:
        cursor.close()

def import_biochemistry(conn, df, record_mapping):
    """导入生化指标数据"""
    cursor = conn.cursor()
    
    # 准备数据
    biochemistry_data = []
    for index, row in df.iterrows():
        try:
            report_date = pd.to_datetime(row['OT01']).date()
            if report_date not in record_mapping:
                print(f"警告：第{index+1}行的日期 {report_date} 没有对应的记录ID")
                continue
                
            record_id = record_mapping[report_date]
            
            # 获取生化指标相关列
            bio_data = [record_id]
            # 定义生化指标列名
            bio_columns = [
                'BIO_total_bilirubin', 'BIO_direct_bilirubin', 'BIO_indirect_bilirubin',
                'BIO_total_protein', 'BIO_albumin', 'BIO_globulin',
                'BIO_albumin_globulin_ratio', 'BIO_alt', 'BIO_alp',
                'BIO_ggt', 'BIO_ast', 'BIO_ldh',
                'BIO_ck', 'BIO_ck_mb', 'BIO_total_bile_acid',
                'BIO_fibronectin', 'BIO_haptoglobin', 'BIO_alpha1_acid_glycoprotein',
                'BIO_potassium', 'BIO_sodium', 'BIO_chloride',
                'BIO_calcium', 'BIO_urea', 'BIO_creatinine',
                'BIO_uric_acid', 'BIO_cystatin_c', 'BIO_blood_glucose',
                'BIO_fructosamine', 'BIO_total_cholesterol', 'BIO_triglyceride',
                'BIO_hdl_cholesterol', 'BIO_ldl_cholesterol', 'BIO_apolipoprotein_a',
                'BIO_apolipoprotein_b', 'BIO_lipoprotein_a', 'BIO_small_dense_ldl',
                'BIO_aso', 'BIO_rf'
            ]
            
            # 按顺序获取数据
            for col in bio_columns:
                value = row.get(col)
                if pd.isna(value):
                    bio_data.append(None)
                else:
                    try:
                        bio_data.append(float(value))
                    except (ValueError, TypeError):
                        bio_data.append(None)
            
            biochemistry_data.append(tuple(bio_data))
        except Exception as e:
            print(f"警告：处理第{index+1}行生化指标数据时发生错误: {e}")
            continue
    
    if not biochemistry_data:
        print("错误：没有有效的生化指标数据可以导入")
        return
    
    # 插入数据
    sql = """
    INSERT INTO biochemistry (
        record_id, total_bilirubin, direct_bilirubin,
        indirect_bilirubin, total_protein, albumin,
        globulin, albumin_globulin_ratio, alt, alp,
        ggt, ast, ldh, ck, ck_mb, total_bile_acid,
        fibronectin, haptoglobin, alpha1_acid_glycoprotein,
        potassium, sodium, chloride, calcium, urea,
        creatinine, uric_acid, cystatin_c, blood_glucose,
        fructosamine, total_cholesterol, triglyceride,
        hdl_cholesterol, ldl_cholesterol, apolipoprotein_a,
        apolipoprotein_b, lipoprotein_a, small_dense_ldl,
        aso, rf
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        total_bilirubin = VALUES(total_bilirubin),
        direct_bilirubin = VALUES(direct_bilirubin),
        indirect_bilirubin = VALUES(indirect_bilirubin),
        total_protein = VALUES(total_protein),
        albumin = VALUES(albumin),
        globulin = VALUES(globulin),
        albumin_globulin_ratio = VALUES(albumin_globulin_ratio),
        alt = VALUES(alt),
        alp = VALUES(alp),
        ggt = VALUES(ggt),
        ast = VALUES(ast),
        ldh = VALUES(ldh),
        ck = VALUES(ck),
        ck_mb = VALUES(ck_mb),
        total_bile_acid = VALUES(total_bile_acid),
        fibronectin = VALUES(fibronectin),
        haptoglobin = VALUES(haptoglobin),
        alpha1_acid_glycoprotein = VALUES(alpha1_acid_glycoprotein),
        potassium = VALUES(potassium),
        sodium = VALUES(sodium),
        chloride = VALUES(chloride),
        calcium = VALUES(calcium),
        urea = VALUES(urea),
        creatinine = VALUES(creatinine),
        uric_acid = VALUES(uric_acid),
        cystatin_c = VALUES(cystatin_c),
        blood_glucose = VALUES(blood_glucose),
        fructosamine = VALUES(fructosamine),
        total_cholesterol = VALUES(total_cholesterol),
        triglyceride = VALUES(triglyceride),
        hdl_cholesterol = VALUES(hdl_cholesterol),
        ldl_cholesterol = VALUES(ldl_cholesterol),
        apolipoprotein_a = VALUES(apolipoprotein_a),
        apolipoprotein_b = VALUES(apolipoprotein_b),
        lipoprotein_a = VALUES(lipoprotein_a),
        small_dense_ldl = VALUES(small_dense_ldl),
        aso = VALUES(aso),
        rf = VALUES(rf)
    """
    
    try:
        cursor.executemany(sql, biochemistry_data)
        conn.commit()
        print(f"成功导入 {len(biochemistry_data)} 条生化指标数据")
    except Exception as e:
        print(f"导入生化指标数据时发生错误: {e}")
        conn.rollback()
    finally:
        cursor.close()

def import_ultrasound(conn, df, record_mapping):
    """导入超声检查数据"""
    cursor = conn.cursor()
    
    # 准备数据
    ultrasound_data = []
    for index, row in df.iterrows():
        try:
            report_date = pd.to_datetime(row['OT01']).date()
            if report_date not in record_mapping:
                print(f"警告：第{index+1}行的日期 {report_date} 没有对应的记录ID")
                continue
                
            record_id = record_mapping[report_date]
            
            # 获取超声检查相关列
            us_data = [record_id]
            # 定义超声检查指标列名
            us_columns = [
                'US_liver_status', 'US_thyroid_status', 'US_prostate_status',
                'US_neck_vessel_status', 'US_bladder_ureter_status'
            ]
            
            # 按顺序获取数据
            for col in us_columns:
                value = row.get(col)
                if pd.isna(value):
                    us_data.append(None)
                else:
                    us_data.append(str(value))
            
            ultrasound_data.append(tuple(us_data))
        except Exception as e:
            print(f"警告：处理第{index+1}行超声检查数据时发生错误: {e}")
            continue
    
    if not ultrasound_data:
        print("错误：没有有效的超声检查数据可以导入")
        return
    
    # 插入数据
    sql = """
    INSERT INTO ultrasound (
        record_id, liver_status, thyroid_status,
        prostate_status, neck_vessel_status,
        bladder_ureter_status
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    try:
        cursor.executemany(sql, ultrasound_data)
        conn.commit()
        print(f"成功导入 {len(ultrasound_data)} 条超声检查数据")
    except Exception as e:
        print(f"导入超声检查数据时发生错误: {e}")
        conn.rollback()
    finally:
        cursor.close()

def import_liver_fibrosis(conn, df, record_mapping):
    """导入肝纤维化数据"""
    cursor = conn.cursor()
    
    # 准备数据
    liver_fibrosis_data = []
    for index, row in df.iterrows():
        try:
            report_date = pd.to_datetime(row['OT01']).date()
            if report_date not in record_mapping:
                print(f"警告：第{index+1}行的日期 {report_date} 没有对应的记录ID")
                continue
                
            record_id = record_mapping[report_date]
            
            # 获取肝纤维化相关列
            lf_data = [record_id]
            # 定义肝纤维化指标列名
            lf_columns = [
                'LF_fibrosis_index', 'LF_hyaluronic_acid',
                'LF_type_iv_collagen', 'LF_laminin',
                'LF_procollagen_iii'
            ]
            
            # 按顺序获取数据
            for col in lf_columns:
                value = row.get(col)
                if pd.isna(value):
                    lf_data.append(None)
                else:
                    try:
                        lf_data.append(float(value))
                    except (ValueError, TypeError):
                        lf_data.append(None)
            
            liver_fibrosis_data.append(tuple(lf_data))
        except Exception as e:
            print(f"警告：处理第{index+1}行肝纤维化数据时发生错误: {e}")
            continue
    
    if not liver_fibrosis_data:
        print("错误：没有有效的肝纤维化数据可以导入")
        return
    
    # 插入数据
    sql = """
    INSERT INTO liver_fibrosis (
        record_id, fibrosis_index, hyaluronic_acid,
        type_iv_collagen, laminin, procollagen_iii
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    try:
        cursor.executemany(sql, liver_fibrosis_data)
        conn.commit()
        print(f"成功导入 {len(liver_fibrosis_data)} 条肝纤维化数据")
    except Exception as e:
        print(f"导入肝纤维化数据时发生错误: {e}")
        conn.rollback()
    finally:
        cursor.close()

def clean_data(df):
    """清洗数据"""
    print("\n开始数据清洗...")
    
    # 复制数据框以避免修改原始数据
    df_clean = df.copy()
    
    # 1. 处理日期列
    print("1. 处理日期列...")
    df_clean['OT01'] = pd.to_datetime(df_clean['OT01'], errors='coerce')
    
    # 删除日期异常的数据
    print("  删除日期异常的数据...")
    # 删除日期为空的数据
    df_clean = df_clean.dropna(subset=['OT01'])
    
    # 删除日期超出合理范围的数据（例如：未来日期或过早的日期）
    current_date = pd.Timestamp.now()
    min_date = pd.Timestamp('2000-01-01')  # 设置一个合理的最早日期
    df_clean = df_clean[
        (df_clean['OT01'] <= current_date) & 
        (df_clean['OT01'] >= min_date)
    ]
    
    # 删除重复日期的数据（保留最新的一条）
    df_clean = df_clean.sort_values('OT01', ascending=False).drop_duplicates(subset=['OT01'], keep='first')
    
    print(f"  删除日期异常后的数据行数: {len(df_clean)}")
    
    # 2. 处理数值列
    print("2. 处理数值列...")
    # 处理血常规数据
    bc_columns = [col for col in df_clean.columns if col.startswith('BC_')]
    for col in bc_columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        # 删除异常值（例如：负值或超出正常范围的值）
        if col in ['BC_white_blood_cell', 'BC_red_blood_cell', 'BC_platelet_count']:
            df_clean = df_clean[df_clean[col] > 0]  # 这些指标不应该为负值
    
    # 处理生化指标数据
    bio_columns = [col for col in df_clean.columns if col.startswith('BIO_')]
    for col in bio_columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        # 删除异常值
        if col in ['BIO_blood_glucose', 'BIO_total_cholesterol', 'BIO_triglyceride']:
            df_clean = df_clean[df_clean[col] > 0]  # 这些指标不应该为负值
    
    # 3. 处理分类数据
    print("3. 处理分类数据...")
    # 处理性别
    if 'OT02' in df_clean.columns:
        df_clean['OT02'] = df_clean['OT02'].fillna('未知')
        df_clean['OT02'] = df_clean['OT02'].astype(str).str.strip()
        # 标准化性别值
        gender_mapping = {
            '男': '男',
            '女': '女',
            'M': '男',
            'F': '女',
            'male': '男',
            'female': '女'
        }
        df_clean['OT02'] = df_clean['OT02'].map(gender_mapping).fillna('未知')
    
    # 处理年龄
    if 'OT03' in df_clean.columns:
        df_clean['OT03'] = pd.to_numeric(df_clean['OT03'], errors='coerce')
        # 删除异常年龄（例如：小于0或大于120）
        df_clean = df_clean[(df_clean['OT03'] >= 0) & (df_clean['OT03'] <= 120)]
    
    # 4. 处理尿常规数据
    print("4. 处理尿常规数据...")
    uc_columns = [col for col in df_clean.columns if col.startswith('UC_')]
    for col in uc_columns:
        df_clean[col] = df_clean[col].fillna('未检测')
        df_clean[col] = df_clean[col].astype(str).str.strip()
    
    # 5. 处理超声检查数据
    print("5. 处理超声检查数据...")
    us_columns = [col for col in df_clean.columns if col.startswith('US_')]
    for col in us_columns:
        df_clean[col] = df_clean[col].fillna('未检查')
        df_clean[col] = df_clean[col].astype(str).str.strip()
    
    # 6. 处理肝纤维化数据
    print("6. 处理肝纤维化数据...")
    lf_columns = [col for col in df_clean.columns if col.startswith('LF_')]
    for col in lf_columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        # 删除异常值
        df_clean = df_clean[df_clean[col] >= 0]  # 这些指标不应该为负值
    
    # 7. 删除完全为空的行
    print("7. 删除完全为空的行...")
    df_clean = df_clean.dropna(how='all')
    
    # 8. 统计清洗结果
    print("\n数据清洗完成！")
    print(f"原始数据行数: {len(df)}")
    print(f"清洗后数据行数: {len(df_clean)}")
    print(f"删除的数据行数: {len(df) - len(df_clean)}")
    
    # 统计每列的空值数量
    null_counts = df_clean.isnull().sum()
    print("\n各列空值统计：")
    for col in df_clean.columns:
        if null_counts[col] > 0:
            print(f"{col}: {null_counts[col]} 个空值")
    
    # 统计异常值处理情况
    print("\n异常值处理统计：")
    print(f"日期异常删除: {len(df) - len(df_clean)} 行")
    print(f"年龄异常删除: {len(df) - len(df_clean[df_clean['OT03'].notna()])} 行")
    
    return df_clean

def main():
    print("开始数据导入流程...")
    
    # 创建数据库
    print("\n1. 正在创建数据库...")
    if not create_database():
        print("数据库创建失败，请检查数据库配置")
        return
    print("数据库创建成功")
    
    # 读取Excel文件
    print("\n2. 正在读取Excel文件...")
    excel_file = '../firstWeek/processed_health_checkup_data.xlsx'
    if not os.path.exists(excel_file):
        print(f"错误：找不到文件 {excel_file}")
        return
    print(f"成功找到文件: {excel_file}")
    
    df = pd.read_excel(excel_file)
    print(f"成功读取数据，共 {len(df)} 条记录")
    
    # 清洗数据
    df = clean_data(df)
    
    # 连接数据库
    print("\n3. 正在连接数据库...")
    conn = connect_to_database()
    if not conn:
        print("数据库连接失败，请检查数据库配置")
        return
    print("数据库连接成功")
    
    try:
        # 创建表
        print("\n4. 正在创建数据库表...")
        create_tables(conn)
        print("数据库表创建完成")
        
        # 导入基础信息
        print("\n5. 正在导入基础信息...")
        import_basic_info(conn, df)
        print("基础信息导入完成")
        
        # 导入体检记录
        print("\n6. 正在导入体检记录...")
        record_mapping = import_exam_record(conn, df)
        if record_mapping is None:
            return
        print("体检记录导入完成")
        
        # 导入各类指标数据
        print("\n7. 正在导入各类指标数据...")
        print("  - 正在导入血常规数据...")
        import_blood_routine(conn, df, record_mapping)
        print("  - 血常规数据导入完成")
        
        print("  - 正在导入尿常规数据...")
        import_urine_routine(conn, df, record_mapping)
        print("  - 尿常规数据导入完成")
        
        print("  - 正在导入生化指标数据...")
        import_biochemistry(conn, df, record_mapping)
        print("  - 生化指标数据导入完成")
        
        print("  - 正在导入超声检查数据...")
        import_ultrasound(conn, df, record_mapping)
        print("  - 超声检查数据导入完成")
        
        print("  - 正在导入肝纤维化数据...")
        import_liver_fibrosis(conn, df, record_mapping)
        print("  - 肝纤维化数据导入完成")
        
        print("\n所有数据导入完成！")
        
    except Exception as e:
        print(f"\n导入过程中出现错误: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("\n数据库连接已关闭")

if __name__ == "__main__":
    main() 