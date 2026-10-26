"""负责把 DataFrame 存进库或者从库里查出来"""
import sqlite3
import pandas as pd

def save_df_to_db(df, db_path, table_name):
    """将DataFrame存入SQLite"""
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"数据已成功写入数据库：{table_name} 表")

def query_table(db_path, sql_query):
    """执行SQL查询并返回DataFrame"""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df
