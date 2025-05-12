import mysql.connector
from mysql.connector import Error

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'health_exam'
}

def test_connection():
    try:
        # 连接数据库
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("成功连接到MySQL数据库")
            
            # 获取数据库信息
            db_info = conn.get_server_info()
            print(f"MySQL服务器版本: {db_info}")
            
            # 创建游标
            cursor = conn.cursor()
            
            # 执行查询
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\n数据库中的表:")
            for table in tables:
                print(f"- {table[0]}")
                
                # 获取表结构
                cursor.execute(f"DESCRIBE {table[0]}")
                columns = cursor.fetchall()
                print("  列结构:")
                for column in columns:
                    print(f"  - {column[0]}: {column[1]}")
                print()
            
    except Error as e:
        print(f"连接数据库时出错: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    test_connection() 