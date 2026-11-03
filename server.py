from fastapi import FastAPI
from pydantic import BaseModel
from ai_client import get_text_violation_status
import json
import re
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    text: str

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@ app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/audit")
def create_item(item: Item):
    result = get_text_violation_status(item.text)

    json_match = re.search(r'\{.*\}', result, re.DOTALL)

    if json_match:
        clean_dict = json.loads(json_match.group())
        return clean_dict
    return {"status": "解析失败", "reason": result}

