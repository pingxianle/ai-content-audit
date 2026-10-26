"""负责发请求、处理报错、返回标签"""
import os
import time
from openai import OpenAI


api_key = os.getenv('ZHIPU_API_KEY')
client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")

def get_book_category(book_name: str, max_retries: int = 3) -> str:
    """调用AI获取单本书的类别, 以及自动重试机制"""
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
                timeout = 10
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f'  [警告] <<{book_name}>> 第 {attempt + 1} 次请求失败: {e}')
            if attempt == max_retries - 1:
                print(f' [失败] <<{book_name}>> 重试 {max_retries} 次均失败, 标记为"识别失败"')
                return "识别失败"
            time.sleep(2 * (attempt + 1))
        finally:
            time.sleep(1.5)

# 新增的文本审核函数
def get_text_violation_status(text: str, max_retries: int = 3) -> str:
    """判断文本是否违规（网络暴力、诈骗、极端情绪）"""
    prompt = f"""
请作为一名网络安全审核员，判断下面这段文本是否包含：网络暴力、辱骂、诈骗广告或极端情绪。
只返回以下三个标签之一，不要任何多余解释：
【正常】、【违规】、【不确定】
文本：{text}
只输出标签名称。
"""
    # 下面的重试和请求逻辑跟之前一模一样
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
                return "识别失败"
            time.sleep(2 * (attempt + 1))
        finally:
            time.sleep(1.5)