import os
import google.generativeai as genai

def generate_response(system_prompt: str, user_prompt: str) -> str:
    """Gemini 모델로부터 답변을 생성합니다."""
    
    # Gemini 모델 설정 (시스템 프롬프트 포함)
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        system_instruction=system_prompt
    )
    
    # 모델에 프롬프트 전송 및 응답 생성
    response = model.generate_content(user_prompt)
    
    return response.text

if __name__ == '__main__':
    # --- API 키 설정 ---
    # GOOGLE_API_KEY라는 이름의 환경 변수를 설정해야 합니다.
    # 예: export GOOGLE_API_KEY='당신의 API 키'
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        print("오류: GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("테스트를 실행하기 전에 'export GOOGLE_API_KEY="<YOUR_API_KEY>"' 명령을 실행하세요.")
    else:
        genai.configure(api_key=API_KEY)

        # --- 테스트용 프롬프트 설정 ---
        
        # 시스템 프롬프트 (모델의 역할을 정의)
        # api_server.py의 SYSTEM_PROMPTS 딕셔너리에서 가져온 예시입니다.
        test_system_prompt = "당신은 커뮤니케이션 매니저입니다. 사용자가 5점 만점의 긍정적인 리뷰를 남겼습니다. 진심 어린 감사를 표현하고, 게임을 계속 즐겨달라는 따뜻한 답변을 작성해주세요."

        # 사용자 프롬프트 (실제 사용자의 입력)
        test_user_prompt = """
Package Name: com.banjihagames.seoul2033_backer
App Version Name: 3.8.0
Reviewer Language: ko
Review Submit Date and Time: 2025-07-13T10:00:00Z
Star Rating: 5
Review Text: 모험 좋아하는 사람으로서 최고의 게임이에요! 근데 어쩔 수 없이 많이 플레이하다보면 맨날 똑같은 느낌도 있어요. 모든 게임이 마찬가지인가 싶기도 하지만... 업데이트 주기가 좀 더 짧으면 좋을 것 같아요!
"""
        # ==========================================================

        try:
            print("모델에 답변 생성을 요청합니다...")
            print("\n--- 시스템 프롬프트 ---")
            print(test_system_prompt)
            print("\n--- 사용자 프롬프트 ---")
            print(test_user_prompt)
            
            generated_text = generate_response(test_system_prompt, test_user_prompt)
            
            print("\n--- 모델 생성 답변 ---")
            print(generated_text)
            
        except Exception as e:
            print(f"\n오류 발생: {e}")
            print("오류 메시지: API 키가 올바른지, 네트워크 연결에 문제가 없는지 확인해 보세요.")