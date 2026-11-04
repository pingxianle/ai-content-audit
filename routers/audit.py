# 处理审核接口和鉴权
from pydantic import BaseModel,Field
import os
import pandas
from ai_client import get_text_violation_status
import json
import re
from fastapi import APIRouter, Depends, Header, HTTPException, status
from config import DB_PATH
from db_handle import save_df_to_db

router = APIRouter()

class Item(BaseModel):
    model_config = {"strict": True}
    text: str = Field(min_length=1, max_length=500)

SECRET_KEY = os.getenv("API_SECRET_KEY")

def verify_token(authorization: str = Header(None)):
    if authorization != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="暗号不对，拒绝访问！"
        )
    return authorization

@router.post("/audit")
def create_item(item: Item, token: str = Depends(verify_token)):
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
    return {"status": "解析失败", "reason": result}