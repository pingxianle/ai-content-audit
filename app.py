import streamlit as st
from ai_client import get_text_violation_status
import json
import re
# 大标题
st.title("🛡️ AI 网络内容安全审核系统")

# 输入框
text_input = st.text_area("请输入需要审核的文本：", "加微信abc123456，带你炒股稳赚！")

# 一个按钮
if st.button("开始审核"):
    if text_input:
        with st.spinner("AI 正在分析中..."):
            result_str = get_text_violation_status(text_input)

            # 用你今天学到的正则防弹衣解析
            json_match = re.search(r'\{.*\}', result_str, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                st.success("审核完成！")
                st.write(f"**判定结果：** {result.get('status')}")
                st.write(f"**违规类型：** {result.get('type')}")
                st.write(f"**判定理由：** {result.get('reason')}")
            else:
                st.error("AI 返回格式异常")