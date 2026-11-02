# 网络文本违规检测流水线 (AI Content Audit Pipeline)

这是我学习 Python 和数据分析做的一个实战自练习小项目。
一开始是拿来给爬下来的书籍做分类的，后来觉得没意思，就把核心代码改成了网络评论的违规（辱骂、诈骗、极端情绪）检测，核心逻辑都是通用的。

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
1. 安装依赖：`pip install pandas openai matplotlib streamlit`
2. 在系统里配好环境变量 `ZHIPU_API_KEY`
3. 批量脚本运行：
   - 准备个 `comments.csv`（表头叫“文本”）
   - 运行 `python main.py`
4. Web 界面运行：
   - 运行 `streamlit run app.py`

> 注：里面还留着一些之前测试书籍分类的代码和垃圾数据，懒得删了。
