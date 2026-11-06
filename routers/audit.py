# 处理审核接口和鉴权
from pydantic import BaseModel,Field
import os
import pandas
from ai_client import get_text_violation_status
import json
import re
from config import DB_PATH
from db_handle import save_df_to_db
import logging
from limiter import limiter
from fastapi import APIRouter, Depends, Header, HTTPException, status, Request
import time


logger = logging.getLogger(__name__)
router = APIRouter()

class Item(BaseModel):
    model_config = {"strict": True}
    text: str = Field(min_length=1, max_length=500)
    timestamp: float

SECRET_KEY = os.getenv("API_SECRET_KEY")

def verify_token(request: Request, authorization: str = Header(None)):
    if authorization != SECRET_KEY:
        logger.warning("鉴权失败：暗号不对，有人企图非法访问！")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="暗号不对，拒绝访问！",
        )
    ua = request.headers.get("User-Agent", "")
    if "python-requests" in ua:
        logger.warning("风控拦截：检测到非浏览器请求，疑似脚本！")
        raise HTTPException(status_code=403, detail="非法客户端")

    return authorization

@router.post("/audit")
@limiter.limit("6/minute")
def create_item(request: Request, item: Item, token: str = Depends(verify_token)):
    current_time = time.time()
    time_diff = current_time - item.timestamp
    if time_diff > 20 or time_diff < 0.5:
        logger.warning(f"风控拦截：请求时间异常，时间差：{time_diff:.2f}秒")
        raise HTTPException(status_code=400, detail="请求超时或速度过快，请不要多次点击")

    logger.info(f"收到审核请求，文本长度：{len(item.text)}")
    result = get_text_violation_status(item.text)

    json_match = re.search(r'\{.*\}', result, re.DOTALL)

    if json_match:
        clean_dict = json.loads(json_match.group())
        df = pandas.DataFrame([{
            "文本": item.text,
            "违规状态": clean_dict.get("status", "未知"),
            "违规类型": clean_dict.get("type", "未知"),
            "判定理由": clean_dict.get("reason", "未知")
        }])
        save_df_to_db(df, DB_PATH, 'comment_audits')
        return clean_dict
    logger.error(f"AI 返回格式异常，原始返回内容：{result}")
    return {"status": "解析失败", "reason": result}