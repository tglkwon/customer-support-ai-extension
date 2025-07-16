from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel

# --- Vertex AI 설정 (test_model.py에서 가져옴) ---
PROJECT_ID = "customer-support-ai-extension"
LOCATION = "asia-northeast3"
# 튜닝이 완료되면 이 ID를 실제 값으로 변경해야 합니다.
TUNED_MODEL_ID = "[YOUR-TUNED-MODEL-ID]" 

# Vertex AI 초기화
vertexai.init(project=PROJECT_ID, location=LOCATION)

# --- FastAPI 앱 설정 ---
app = FastAPI()

# CORS 미들웨어 추가 (React 앱과의 통신을 위해)
# 주의: 프로덕션 환경에서는 origins를 특정 도메인으로 제한해야 합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# --- API 요청/응답 모델 정의 ---
class PromptRequest(BaseModel):
    prompt: str

class CompletionResponse(BaseModel):
    reply: str

# --- API 엔드포인트 정의 ---
@app.post("/generate-reply", response_model=CompletionResponse)
def generate_reply(request: PromptRequest):
    """
    프롬프트를 받아 Vertex AI 모델을 호출하고, 생성된 답변을 반환합니다.
    """
    if TUNED_MODEL_ID == "[YOUR-TUNED-MODEL-ID]":
        return CompletionResponse(reply="오류: 모델 튜닝이 아직 완료되지 않았거나 모델 ID가 설정되지 않았습니다.")
    
    try:
        # 튜닝된 모델 로드
        model = GenerativeModel(model_name=TUNED_MODEL_ID)
        
        # 모델로부터 답변 생성
        response = model.generate_content([request.prompt])
        
        return CompletionResponse(reply=response.text)
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return CompletionResponse(reply=f"모델 호출 중 오류가 발생했습니다: {e}")

@app.get("/")
def read_root():
    return {"status": "Customer Support AI API is running."}

