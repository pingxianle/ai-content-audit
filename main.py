import pandas as pd
from config import DB_PATH
from ai_client import get_text_violation_status
from db_handle import save_df_to_db, query_table
from draw_charts import plot_category_chart
import json
import re


def main():
    try:
        df = pd.read_csv('comments.csv', encoding='utf-8')
        df = df[['文本']].copy()
    except Exception as e:
        print(f"读取失败: {e}")
        return

    total = len(df)
    print(f"=== 开始审核 {total} 条评论 ===")
    ai_tags = []

    for index, row in df.iterrows():
        text = row['文本']
        print(f"[{index + 1}/{total}] 审核中: {text[:15]}...")
        result_str = get_text_violation_status(text)

        try:
            json_match = re.search(r'\{.*\}', result_str, re.DOTALL)
            if json_match:
                result_dict = json.loads(json_match.group())
            else:
                status_match = re.search(r'"status"\s*:\s*"([^"]+)"', result_str)
                type_match = re.search(r'"type"\s*:\s*"([^"]+)"', result_str)
                reason_match = re.search(r'"reason"\s*:\s*"([^"]+)"', result_str)

                result_dict = {
                    "status": status_match.group(1) if status_match else "解析失败",
                    "type": type_match.group(1) if type_match else "无",
                    "reason": reason_match.group(1) if reason_match else result_str[:20]
                }

            status = result_dict.get('status', '解析失败')
            if status == '无': status = '正常'

            v_type = result_dict.get('type', '解析失败')
            reason = result_dict.get('reason', '解析失败')

        except Exception as e:
            status, v_type, reason = "解析失败", "无", result_str

        ai_tags.append({
            '违规状态': status,
            '违规类型': v_type,
            '判定理由': reason
        })

    df_tags = pd.DataFrame(ai_tags)
    df = pd.concat([df, df_tags], axis=1)

    table_name = 'comment_audits'
    save_df_to_db(df, DB_PATH, table_name)

    print("\n=== 数据已入库，预览前 5 条判定结果 ===")
    preview_df = query_table(DB_PATH, f"SELECT * FROM {table_name} LIMIT 5")
    print(preview_df)

    print("\n=== 违规状态统计 ===")
    stats = query_table(DB_PATH, f"SELECT 违规状态, COUNT(*) as 数量 FROM {table_name} GROUP BY 违规状态")
    print(stats)

    if not stats.empty:
        plot_category_chart(stats)

if __name__ == '__main__':
    main()