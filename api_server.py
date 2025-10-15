from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import traceback
import os

# --- Gemini AI 설정 ---
# 환경 변수에서 API 키를 가져옵니다.
# GOOGLE_API_KEY라는 이름의 환경 변수를 설정해야 합니다.
# 예: export GOOGLE_API_KEY='당신의 API 키'
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

genai.configure(api_key=API_KEY)

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
class GenerateRequest(BaseModel):
    prompt: str
    category: str | None = None

class CompletionResponse(BaseModel):
    reply: str

# --- 카테고리별 시스템 프롬프트 정의 ---
SYSTEM_PROMPTS = {
    "bug_report": "당신은 모바일 게임의 기술적인 문제를 해결하는 '버그 리포트 분석 전문가'입니다. 사용자가 버그를 신고했습니다. 문제 상황을 명확히 이해하고, 필요하다면 추가 정보(기기 종류, OS 버전 등)를 요청하는 답변을 생성해주세요.",
    "account_issue": "당신은 '계정 문제 해결 전문가'입니다. 사용자가 계정(로그인, 분실, 연동 등)과 관련된 문제를 겪고 있습니다. 친절하게 안심시키고, 계정 복구를 위한 절차를 안내하는 답변을 생성해주세요.",
    "billing_inquiry": "당신은 '결제 및 환불 정책 전문가'입니다. 사용자가 결제 또는 환불에 대해 문의했습니다. 회사의 정책에 기반하여 명확하고 정확한 답변을 생성해주세요.",
    "gameplay_question": "당신은 게임의 모든 것을 알고 있는 '마스터 게이머'입니다. 사용자가 게임 플레이에 대해 질문했습니다. 친절하고 상세하게 게임 공략법이나 팁을 알려주는 답변을 생성해주세요.",
    "event_reward_inquiry": "당신은 게임의 '이벤트 및 보상 담당자'입니다. 사용자가 이벤트 참여나 보상 지급에 대해 문의했습니다. 이벤트 내용을 확인하고, 보상 지급 조건과 상태를 안내하는 답변을 생성해주세요.",
    "content_suggestion": "당신은 게임의 미래를 기획하는 '게임 기획자'입니다. 사용자가 게임에 대한 새로운 아이디어를 제안했습니다. 소중한 의견에 감사하고, 긍정적으로 검토하겠다는 답변을 생성해주세요.",
    "review_5_star": "당신은 커뮤니티 매니저입니다. 사용자가 5점 만점의 긍정적인 리뷰를 남겼습니다. 진심 어린 감사를 표현하고, 게임을 계속 즐겨달라는 따뜻한 답변을 작성해주세요.",
    "review_4_star_no_complaint": "당신은 고객 경험 개선 담당자입니다. 사용자가 4점 이하의 리뷰를 남겼지만, 구체적인 불만 내용은 없습니다. 아쉬운 점이 있었는지 구체적인 피드백을 정중하게 요청하여, 게임을 개선할 기회를 만드는 답변을 작성해주세요.",
    "etc": "당신은 모든 종류의 문의에 대응하는 '만능 고객 지원 담당자'입니다. 사용자의 문의에 대해 최대한 친절하고 상세하게 답변해주세요."
}
DEFAULT_SYSTEM_PROMPT = "당신은 모바일 게임 회사의 고객 지원 담당자입니다. 다음 문의에 대해 친절하고 도움이 되는 답변을 생성해주세요."

# --- API 엔드포인트 정의 ---
@app.post("/generate-response", response_model=CompletionResponse)
def generate_response(request: GenerateRequest):
    """
    시스템 프롬프트와 사용자 프롬프트를 사용하여 Gemini 모델을 호출하고, 생성된 답변을 반환합니다.
    카테고리가 지정된 경우, 해당 카테고리에 맞는 특화된 시스템 프롬프트를 사용합니다.
    """
    
    # 카테고리에 따라 시스템 프롬프트 선택
    system_prompt = DEFAULT_SYSTEM_PROMPT
    if request.category and request.category in SYSTEM_PROMPTS:
        system_prompt = SYSTEM_PROMPTS[request.category]

    print("--- SYSTEM-PROMPT-TO-AI-START ---")
    print(system_prompt)
    print("--- SYSTEM-PROMPT-TO-AI-END ---")
    print("--- USER-PROMPT-TO-AI-START ---")
    print(request.prompt)
    print("--- USER-PROMPT-TO-AI-END ---")

    try:
        # Gemini 모델 설정 (시스템 프롬프트 포함)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-lite",
            system_instruction=system_prompt
        )
        
        # 모델 호출
        response = model.generate_content(request.prompt)
        
        reply_text = response.text

        print("--- AI-GENERATED-REPLY-START ---")
        print(reply_text)
        print("--- AI-GENERATED-REPLY-END ---")

        return CompletionResponse(reply=reply_text)
        
    except Exception as e:
        print("--- FULL-EXCEPTION-START ---")
        traceback.print_exc()
        print("--- FULL-EXCEPTION-END ---")
        raise HTTPException(status_code=500, detail=f"모델 호출 중 서버 내부 오류가 발생했습니다: {str(e)}")


@app.get("/")
def read_root():
    return {"status": "Customer Support AI API is running."}
