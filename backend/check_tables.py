import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

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

def check_table_structure():
    """检查所有表的结构"""
    conn = None
    try:
        conn = connect_to_database()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # 获取所有表名
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("\n=== 数据库表结构检查 ===\n")
        
        for table in tables:
            table_name = table[0]
            print(f"\n表名: {table_name}")
            
            # 获取表结构
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            # 使用tabulate格式化输出
            headers = ["字段名", "类型", "空值", "键", "默认值", "额外信息"]
            print(tabulate(columns, headers=headers, tablefmt="grid"))
            
            # 获取记录数
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\n记录数: {count}")
            
            # 获取示例数据
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                sample = cursor.fetchone()
                print("\n示例数据:")
                for i, col in enumerate(cursor.description):
                    print(f"{col[0]}: {sample[i]}")
            
            print("\n" + "="*50)
            
    except Error as err:
        print(f"查询错误: {err}")
    finally:
        if conn:
            conn.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    check_table_structure() 