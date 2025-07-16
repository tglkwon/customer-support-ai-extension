import vertexai
from vertexai.generative_models import GenerativeModel

def generate_response(project_id: str, location: str, tuned_model_id: str, prompt: str) -> str:
    """Vertex AI의 튜닝된 모델로부터 답변을 생성합니다."""
    
    # Vertex AI 초기화
    vertexai.init(project=project_id, location=location)
    
    # 튜닝된 모델 로드
    # Vertex AI Studio의 튜닝 작업 페이지에서 '배포 및 사용' 버튼을 누르면
    # 정확한 모델 ID (엔드포인트)를 확인할 수 있습니다.
    model = GenerativeModel(model_name=tuned_model_id)
    
    # 모델에 프롬프트 전송 및 응답 생성
    response = model.generate_content([prompt])
    
    return response.text

if __name__ == '__main__':
    # === 튜닝 완료 후, 이 값들을 실제 값으로 변경해야 합니다. ===
    PROJECT_ID = "customer-support-ai-extension"
    LOCATION = "asia-northeast3" # 모델을 튜닝한 리전
    
    # 튜닝된 모델 ID는 Vertex AI 튜닝 페이지에서 확인 가능합니다. 
    # 보통 숫자 형태의 긴 ID이며, 튜닝 작업이 '성공' 상태가 되면 나타납니다.
    # 예시: "projects/1234567890/locations/asia-northeast3/models/9876543210"
    TUNED_MODEL_ID = "[YOUR-TUNED-MODEL-ID]" 
    # ==========================================================

    # 테스트용 프롬프트
    test_prompt = """
Package Name: com.banjihagames.seoul2033_backer
App Version Name: 3.8.0
Reviewer Language: ko
Review Submit Date and Time: 2025-07-13T10:00:00Z
Star Rating: 5
Review Text: 모험 좋아하는 사람으로서 최고의 게임이에요! 근데 어쩔 수 없이 많이 플레이하다보면 맨날 똑같은 느낌도 있어요. 모든 게임이 마찬가지인가 싶기도 하지만... 업데이트 주기가 좀 더 짧으면 좋을 것 같아요!
"""

    if TUNED_MODEL_ID == "[YOUR-TUNED-MODEL-ID]":
        print("스크립트 실행 준비 완료.")
        print("모델 튜닝이 완료되면, 'TUNED_MODEL_ID' 값을 실제 모델 ID로 변경한 후 다시 실행해 주세요.")
    else:
        try:
            print("모델에 답변 생성을 요청합니다...")
            generated_text = generate_response(PROJECT_ID, LOCATION, TUNED_MODEL_ID, test_prompt)
            print("\n--- 모델 생성 답변 ---")
            print(generated_text)
        except Exception as e:
            print(f"\n오류 발생: {e}")
            print("오류 메시지: TUNED_MODEL_ID가 올바른지, 모델이 엔드포인트에 배포되었는지 확인해 보세요.")
