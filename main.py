import pandas as pd
from config import DB_PATH
from ai_client import get_text_violation_status  # 👈 改动1：导入新的审核函数
from db_handle import save_df_to_db, query_table
from draw_charts import plot_category_chart

def main():
    # 👈 改动2：改读 comments.csv
    try:
        df = pd.read_csv('comments.csv', encoding='utf-8')
        df = df[['文本']].copy() # 列名改成了“文本”
    except Exception as e:
        print(f"读取失败: {e}")
        return

    total = len(df)
    print(f"=== 开始审核 {total} 条评论 ===")
    ai_tags = []

    for index, row in df.iterrows():
        text = row['文本']
        print(f"[{index+1}/{total}] 审核中: {text[:15]}...")
        # 👈 改动3：调用新的审核函数
        tag = get_text_violation_status(text)
        ai_tags.append(tag)

    df['AI分类'] = ai_tags # 为了配合画图代码，列名依然叫 AI分类

    # 👈 改动4：存进一个新的表名（comment_audits），不污染原来的图书数据
    table_name = 'comment_audits'
    save_df_to_db(df, DB_PATH, table_name)

    print("\n=== 审核结果统计 ===")
    stats = query_table(DB_PATH, f"SELECT AI分类, COUNT(*) as 数量 FROM {table_name} GROUP BY AI分类")
    print(stats)

    if not stats.empty:
        plot_category_chart(stats)

if __name__ == '__main__':
    main()