# 网络文本违规检测流水线 (AI Content Audit Pipeline)

这是我学习 Python 和数据分析做的一个实战自练习小项目。
一开始是拿来给爬下来的书籍做分类的，后来觉得没意思，就把核心代码改成了网络评论的违规（辱骂、诈骗、极端情绪）检测，核心逻辑都是通用的。

## 架构说明：
前端：Streamlit 交互界面（app.py）
后端：FastAPI 接口服务（server.py）
数据流：前端发请求 -> 后端调智谱 AI 并清洗 JSON -> 前端接收并持久化到本地。

## 用到了啥
- Python, Pandas
- 智谱的免费大模型 API (GLM-4-Flash)
- SQLite 数据库
- Matplotlib 画图
- **Streamlit (Web 交互界面)**

## 干了啥
- 读本地的 CSV 文件。
- 循环把文本发给 AI 判断，并让 AI 返回结构化的 JSON 数据。
- 因为免费 API 老是报错，加了失败重试和限流（sleep）。
- 用正则表达式对 AI 可能乱输出的文本进行了强制清洗。
- 把判断的结果用 Pandas 存进 SQLite 数据库，并生成柱状图。
- **做了一个 Web 审核页面，支持单条文本实时审核，并在侧边栏展示、筛选、一键导出历史记录（JSON 格式持久化）。**

## 文件结构
- `config.py`: 存路径和表名
- `ai_client.py`: 调 API、处理 JSON 和重试的代码
- `db_handle.py`: 负责存数据库和查数据库
- `draw_charts.py`: 画图
- `main.py`: 批量处理主程序
- **`app.py`: 基于 Streamlit 的 Web 交互界面**

## 怎么跑
1. 安装依赖（一键安装所有需要的库）：
   `pip install -r requirements.txt`
2. 配置好环境变量 `ZHIPU_API_KEY`。
3. 先启动后端服务：
   `fastapi dev server.py`
4. 再启动前端页面：
   `streamlit run app.py`

# ![系统运行截图](ui_screenshot.png)

> 注：里面还留着一些之前测试书籍分类的代码和垃圾数据，懒得删了。
