from fastapi import FastAPI, Header, HTTPException, status, Depends
from pydantic import BaseModel,Field
from ai_client import get_text_violation_status
import json
import re
from fastapi.middleware.cors import CORSMiddleware
from db_handle import save_df_to_db,query_table
import pandas
from config import DB_PATH
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    model_config = {"strict": True}
    text: str = Field(min_length=1, max_length=500)

@ app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/history")
def get_history():
    df = query_table(DB_PATH,"SELECT 文本, 违规状态 AS 状态, 违规类型 AS 类型, 判定理由 AS 理由 FROM comment_audits")
    return df.to_dict(orient="records")

SECRET_KEY = os.getenv("SECRET_KEY")

def verify_token(authorization: str = Header(None)):
    if authorization != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="暗号不对，拒绝访问！"
        )
    return authorization

@app.post("/audit")
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

