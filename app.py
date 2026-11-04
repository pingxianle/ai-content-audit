import streamlit as st
import requests
import json
import os


# def save_history(record_dict):
#     """
#     保存历史记录到文件
#     :param record_dict: 包含新记录的字典, 格式为 {"text": "xxx", "result": "xxx"}
#     :return: None
#     """
#     file_path = "history.json"
#     history_list = []
#
#     if os.path.exists(file_path):
#         with open(file_path, "r", encoding="utf-8") as f:
#             history_list = json.load(f)
#     history_list.append(record_dict)
#     with open(file_path, "w", encoding="utf-8") as f:
#         json.dump(history_list, f, ensure_ascii=False, indent=4)

# def load_history():
#     """
#     从文件加载历史记录
#     :return: 包含历史记录的列表, 每个记录为一个字典，格式为 {"text": "xxx", "result": "xxx"}
#     """
#     file_path = "history.json"
#     if not os.path.exists(file_path):
#         return []
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)

# 设置页面配置项
st.set_page_config(
    page_title="AI 网络内容安全审核系统",
    page_icon="🛡️",
    layout="wide", # center中间区域 or wide 整个区域 or None
    initial_sidebar_state="expanded", # 控制的是侧边栏的状态
    menu_items={ } # 网页右上角菜单的跳转信息 字典可为空
)

# 网页主体界面
st.title("🛡️ AI 网络内容安全审核系统")
text_input = st.text_area("请输入需要审核的文本：", "加微信abc123456，带你炒股稳赚，内部消息！")

if st.button("开始审核", type="primary"):
    if text_input.strip() == "":
        st.warning("请先输入文本！")
    else:
        with st.spinner("AI is analyzing..."):
            try:
                my_headers = {"Authorization": os.getenv("API_SECRET_KEY")}
                r = requests.post('http://127.0.0.1:8000/audit', json={'text': text_input}, headers=my_headers)

                if r.status_code == 200:
                    result_dict = r.json()
                    status = result_dict.get('status', '未知')
                    v_type = result_dict.get('type', '未知')
                    reason = result_dict.get('reason', '未知')

                    if status == "正常":
                        st.success("✅ 审核通过")
                    elif status == "违规":
                        st.error("❌ 发现违规")
                    else:
                        st.warning("⚠️ 无法确定")

                    st.write(f"**判定结果：** {status}")
                    st.write(f"**违规类型：** {v_type}")
                    st.write(f"**判定理由：** {reason}")
                else:
                    st.error("后端返回错误，状态码非 200")
            except requests.exceptions.ConnectionError:
                st.error("连不上后端！请检查 server.py 终端是否在运行。")

# 配置侧边栏
with st.sidebar:
    st.header("📜 历史记录")

    # 向数据库发送请求读取数据记录
    try:
        response = requests.get('http://127.0.0.1:8000/history')

        if response.status_code == 200:
            read_records = response.json()
        else:
            st.error("获取历史记录失败，请检查后端是否启动")
            read_records = []
    except requests.exceptions.ConnectionError:
        st.error("无法连接后端，历史记录加载失败")
        read_records = []

    # 数据筛选菜单
    option = st.selectbox(
        "筛选状态",
        ["全部", "正常", "违规", "不确定"],
    )
    all_data = read_records
    filtered_data = []
    if option == "全部":
        filtered_data = all_data
    elif option == "正常":
        filtered_data = [item for item in all_data if item["状态"] == "正常"]
    elif option == "违规":
        filtered_data = [item for item in all_data if item["状态"] == "违规"]
    elif option == "不确定":
        filtered_data = [item for item in all_data if item["状态"] == "不确定"]

    st.dataframe(filtered_data)
    if not filtered_data:
        st.info("暂无历史记录")

    # 下载数据
    if filtered_data:
        json_string = json.dumps(filtered_data, ensure_ascii=False, indent=4)
        st.download_button(
            label="📥 下载历史数据",
            data=json_string,
            file_name="history.json",
            mime="application/json",
        )

# streamlit run app.py