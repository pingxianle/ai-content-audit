"""负责发请求、处理报错、返回标签"""
import os
import time
from openai import OpenAI

api_key = os.getenv('ZHIPU_API_KEY')
client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")

def get_book_category(book_name: str, max_retries: int = 3) -> str:
    """调用AI获取单本书的类别（返回纯文本标签）"""
    prompt = f"""
请对下面的书名进行图书类型分类，只返回分类标签，不要多余解释。
可选标签：悬疑、爱情、历史、科幻、文学、其他
书名：{book_name}
只输出标签名称。
"""
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model="glm-4-flash",
                messages=[{"role": "user", "content": prompt.strip()}],
                timeout=10
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f'  [警告] <<{book_name}>> 第 {attempt + 1} 次请求失败: {e}')
            if attempt == max_retries - 1:
                return "识别失败"
            time.sleep(2 * (attempt + 1))
        finally:
            time.sleep(1.5)


def get_text_violation_status(text: str, max_retries: int = 3) -> str:
    """判断文本是否违规（返回 JSON 格式字符串）"""
    prompt = f"""
你是一个严格的内容审核系统。
请对输入的文本进行分类，并严格输出 JSON 格式。
【输出要求】
1. 必须且只能包含以下三个键：status, type, reason。
2. status 的值只能是："正常"、"违规"、"不确定"（绝对不要写"无"）。
3. type 的值只能是："辱骂"、"诈骗"、"极端情绪"、"无"。
4. reason 必须是一句话简述，不超过20字。
5. 不要输出任何 Markdown 标记（如 ```json），不要输出任何多余的解释文字。

【标准输出示例】
{{"status": "违规", "type": "辱骂", "reason": "包含人身攻击词汇"}}
待审核文本：{text}
"""
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model="glm-4-flash",
                messages=[{"role": "user", "content": prompt.strip()}],
                timeout=10
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f'  [警告] <<{text}>> 第 {attempt + 1} 次请求失败: {e}')
            if attempt == max_retries - 1:
                return '{"status": "识别失败", "type": "无", "reason": "API重试均失败"}'
            time.sleep(2 * (attempt + 1))
        finally:
            time.sleep(1.5)
