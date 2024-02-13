from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import requests
import openai

app = FastAPI()

class Item(BaseModel):
    character_name: str


# アクセスの為のキーをopenai.api_keyに代入し、設定
openai.api_key = "apikey"

def run_gpt(character_name: str) -> str:
    request_to_gpt = f"アニメ・キングダムのキャラクター {character_name} のリーダーシップについて、企業経営をする上で重要な要素と照らし合わせて語ってください。"
     
    # 決めた内容を元にopenai.ChatCompletion.createでchatGPTにリクエスト。オプションとしてmodelにAIモデル、messagesに内容を指定
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": request_to_gpt },
        ],
    )

    # 返って来たレスポンスの内容はresponse.choices[0]["message"]["content"].strip()に格納されているので、これをoutput_contentに代入
    gpt_response = response.choices[0]["message"]["content"].strip()

    return gpt_response  # 返って来たレスポンスの内容を返す

# /onepiecesエンドポイントへのGETリクエストを処理
@app.post("/leader")
def get_description(item: Item):
    character_name = item.character_name
    description = run_gpt(character_name)
    return {"character_name": character_name, "description": description}