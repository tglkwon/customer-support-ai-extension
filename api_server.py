from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel
import traceback

# --- Vertex AI 설정 ---
PROJECT_ID = "customer-support-ai-extension"
LOCATION = "asia-northeast3"
# 튜닝된 모델의 전체 리소스 이름 (버전 정보 제외)
TUNED_MODEL_ID = "projects/442212722968/locations/asia-northeast3/models/5441707346235490304"

# Vertex AI 초기화
vertexai.init(project=PROJECT_ID, location=LOCATION)

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

# --- API 엔드포인트 정의 ---
@app.post("/generate-reply", response_model=CompletionResponse)
def generate_reply(request: PromptRequest):
    """
    프롬프트를 받아 튜닝된 Gemini 모델을 호출하고, 생성된 답변을 반환합니다.
    """
    print("--- API-RECEIVED-PROMPT-START ---")
    print(request.prompt)
    print("--- API-RECEIVED-PROMPT-END ---")

    try:
        # 올바른 클래스(GenerativeModel)로 튜닝된 모델 로드
        model = GenerativeModel(TUNED_MODEL_ID)
        
        # 단순 문자열로 프롬프트 전달
        response = model.generate_content(request.prompt)
        
        print("--- AI-GENERATED-REPLY-START ---")
        print(response.text)
        print("--- AI-GENERATED-REPLY-END ---")

        return CompletionResponse(reply=response.text)
        
    except Exception as e:
        print("--- FULL-EXCEPTION-START ---")
        traceback.print_exc()
        print("--- FULL-EXCEPTION-END ---")
        error_message = f"모델 호출 중 오류가 발생했습니다: {getattr(e, 'message', str(e))}"
        return CompletionResponse(reply=error_message)

@app.get("/")
def read_root():
    return {"status": "Customer Support AI API is running."}