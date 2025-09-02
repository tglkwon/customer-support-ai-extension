from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import subprocess
import json
import traceback
import os

# --- Vertex AI 설정 ---
PROJECT_ID = "customer-support-ai-extension"
LOCATION = "us-central1"
# 안정성을 위해 :generateContent API로 직접 호출할 튜닝된 모델 ID
TUNED_MODEL_ID = "customer-support-ai-v2-stable"

# --- FastAPI 앱 설정 ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API 요청/응답 모델 정의 ---
class PromptRequest(BaseModel):
    prompt: str

class CompletionResponse(BaseModel):
    reply: str

# --- Helper 함수 ---
def get_access_token():
    """gcloud CLI를 통해 액세스 토큰을 가져옵니다."""
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"], shell=True).decode("utf-8").strip()
        return token
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"gcloud를 통해 액세스 토큰을 얻는 중 오류 발생: {e}")
        raise RuntimeError("gcloud 인증에 실패했습니다. gcloud CLI가 설치 및 인증되었는지 확인하세요.")

# --- API 엔드포인트 정의 ---
@app.post("/generate-reply", response_model=CompletionResponse)
def generate_reply(request: PromptRequest):
    """
    프롬프트를 받아 튜닝된 Gemini 모델의 REST API(:generateContent)를 직접 호출하고, 생성된 답변을 반환합니다.
    """
    print("--- API-RECEIVED-PROMPT-START ---")
    print(request.prompt)
    print("--- API-RECEIVED-PROMPT-END ---")

    try:
        token = get_access_token()
        
        # 튜닝된 모델을 호출하기 위한 :generateContent 엔드포인트 URL
        url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{TUNED_MODEL_ID}:generateContent"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        # :generateContent API가 요구하는 요청 본문 형식
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": request.prompt}]
                }
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        response_json = response.json()
        
        # API 응답 구조에 따라 답변 추출
        reply_text = response_json['candidates'][0]['content']['parts'][0]['text']

        print("--- AI-GENERATED-REPLY-START ---")
        print(reply_text)
        print("--- AI-GENERATED-REPLY-END ---")

        return CompletionResponse(reply=reply_text)
        
    except requests.exceptions.HTTPError as http_err:
        error_body = http_err.response.text
        print(f"--- HTTP-ERROR-START ---\n{http_err}\n--- RESPONSE-BODY ---\n{error_body}\n--- HTTP-ERROR-END ---")
        # 클라이언트가 오류를 명확히 인지하도록 HTTPException을 발생시킵니다.
        raise HTTPException(status_code=http_err.response.status_code, detail=f"모델 API 호출 중 HTTP 오류가 발생했습니다: {error_body}")
    except Exception as e:
        print("--- FULL-EXCEPTION-START ---")
        traceback.print_exc()
        print("--- FULL-EXCEPTION-END ---")
        raise HTTPException(status_code=500, detail=f"모델 호출 중 서버 내부 오류가 발생했습니다: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "Customer Support AI API is running."}