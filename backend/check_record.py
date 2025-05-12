import mysql.connector
from mysql.connector import Error

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
        print(f"数据库连接错误: {err}")
        return None

def check_record(record_id):
    """检查特定记录ID的数据"""
    conn = None
    try:
        conn = connect_to_database()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        
        # 检查基本信息
        print("\n=== 检查基本信息 ===")
        basic_sql = """
        SELECT * FROM exam_record WHERE record_id = %s
        """
        cursor.execute(basic_sql, (record_id,))
        basic_info = cursor.fetchone()
        print(f"基本信息: {basic_info}")
        
        # 检查血常规数据
        print("\n=== 检查血常规数据 ===")
        blood_sql = """
        SELECT * FROM blood_routine WHERE record_id = %s
        """
        cursor.execute(blood_sql, (record_id,))
        blood_data = cursor.fetchone()
        print(f"血常规数据: {blood_data}")
        
        # 检查尿常规数据
        print("\n=== 检查尿常规数据 ===")
        urine_sql = """
        SELECT * FROM urine_routine WHERE record_id = %s
        """
        cursor.execute(urine_sql, (record_id,))
        urine_data = cursor.fetchone()
        print(f"尿常规数据: {urine_data}")
        
        # 检查生化指标数据
        print("\n=== 检查生化指标数据 ===")
        bio_sql = """
        SELECT * FROM biochemistry WHERE record_id = %s
        """
        cursor.execute(bio_sql, (record_id,))
        bio_data = cursor.fetchone()
        print(f"生化指标数据: {bio_data}")
        
        # 检查超声检查数据
        print("\n=== 检查超声检查数据 ===")
        us_sql = """
        SELECT * FROM ultrasound WHERE record_id = %s
        """
        cursor.execute(us_sql, (record_id,))
        us_data = cursor.fetchone()
        print(f"超声检查数据: {us_data}")
        
        # 检查肝纤维化数据
        print("\n=== 检查肝纤维化数据 ===")
        lf_sql = """
        SELECT * FROM liver_fibrosis WHERE record_id = %s
        """
        cursor.execute(lf_sql, (record_id,))
        lf_data = cursor.fetchone()
        print(f"肝纤维化数据: {lf_data}")
        
    except Error as err:
        print(f"查询错误: {err}")
    finally:
        if conn:
            conn.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    record_id = "14ab883de3a84ecca04964983de6fabb"
    check_record(record_id) 