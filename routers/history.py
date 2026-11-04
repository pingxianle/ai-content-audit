# 处理查询历史的接口
from fastapi import APIRouter
from db_handle import query_table
from config import DB_PATH

router = APIRouter()
@router.get("/history")
def get_history():
    df = query_table(DB_PATH,"SELECT 文本, 违规状态 AS 状态, 违规类型 AS 类型, 判定理由 AS 理由 FROM comment_audits")
    return df.to_dict(orient="records")