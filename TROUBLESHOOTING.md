# Vertex AI 모델 연동 트러블슈팅 기록

이 문서는 Vertex AI 튜닝 모델을 API 서버 및 프론트엔드와 연동하는 과정에서 발생했던 주요 오류와 해결 과정을 기록합니다.

### 1. `404 Publisher Model ... not found` 오류

-   **원인:** `api_server.py`의 `TUNED_MODEL_ID`에 **튜닝된 모델의 ID**가 아닌, **기반 모델(Publisher Model)의 ID**를 잘못 입력함.
-   **해결책:** Vertex AI의 **"튜닝"** 메뉴에서 완료된 튜닝 작업의 세부 정보로 이동하여, `projects/.../models/...` 형식의 **전체 모델 리소스 이름**을 찾아 정확히 입력해야 함.

### 2. `403 ... model was not allowlisted` 오류

-   **원인:** 프로젝트가 튜닝에 사용한 기반 모델(예: `gemini-1.5-flash-002`)을 사용할 수 있도록 **사전 승인(allowlist)되지 않음.**
-   **해결책:**
    1.  **(권장)** 별도의 승인이 필요 없는 **범용(GA) 모델** (예: `gemini-2.0-flash-lite-001`)을 사용하여 다시 튜닝.
    2.  (시간 소요) 모델 가든에서 해당 모델의 사용 권한을 별도로 요청하고 승인될 때까지 대기.

### 3. `us-central1 리전에서는 ... 모델을 사용할 수 없습니다` 오류

-   **원인:** **리전 불일치.** 모델이 튜닝된 리전과 Vertex AI Studio 또는 API 코드에서 호출하는 리전이 서로 다름.
-   **해결책:**
    *   모델을 튜닝할 때, API 서버의 `LOCATION` 설정과 **동일한 리전**을 선택하는 것이 가장 좋음.
    *   만약 다른 리전에서 튜닝했다면, `api_server.py`의 `LOCATION` 변수 값을 **모델이 실제로 있는 리전** (예: `us-central1`)으로 반드시 수정해야 함.

### 4. `400 Request contains an invalid argument` (지속적인 오류)

-   **개요:** 튜닝된 모델(`gemini-2.0-flash-lite-001` 기반)을 `GenerativeModel` SDK 클래스로 호출 시, 지속적으로 `400 Invalid Argument` 오류가 발생함. 이 문제는 코드 수준의 문제가 아닌, SDK와 로컬 환경, 엔드포인트 설정 간의 복합적인 문제로 최종 판명됨.
-   **진단 과정:**
    1.  **프롬프트 형식 불일치:** 학습 데이터와 API 호출 시의 프롬프트 형식이 미세하게 다른 것을 발견하고 수정했으나, 문제 해결에 실패.
    2.  **SDK 호출 방식 변경:** `GenerativeModel`의 `generate_content`, `start_chat` 등 다양한 메소드를 시도했으나 모두 실패.
    3.  **엔드포인트 배포 및 호출:** 튜닝된 모델을 온라��� 예측 엔드포인트에 배포 후, `aiplatform.Endpoint` 클래스로 호출 시도. `Gemini cannot be accessed through Vertex Predict/RawPredict API` 오류가 발생하며, 이 방법이 Gemini 모델에 적합하지 않음을 확인함.
    4.  **프로젝트 ID 불일치:** `vertexai.init()`에 사용된 문자열 프로젝트 ID와 모델 경로의 숫자 프로젝트 ID가 다른 것을 발견하고 일치시켰으나, 문제 해결에 실패.
    5.  **`curl`을 이용한 직접 호출 테스트:**
        -   **기본 모델 (`:generateContent`):** `curl`을 통해 기본 모델 API를 직접 호출하는 데 **성공**. 이는 로컬 환경의 인증/권한/네트워크에는 문제가 없음을 증명함.
        -   **튜닝된 모델 엔드포인트 (`:predict`):** `curl`을 통해 배포된 엔드포인트를 직접 호출 시, `401 UNAUTHENTICATED` 및 `ACCESS_TOKEN_TYPE_UNSUPPORTED` 오류 발생. 이는 엔드포인트가 외부에서의 직접적인 API 호출을 허용하도록 설정되지 않았음을 시사함.
-   **최종 결론 및 해결책:**
    -   **근본 원인:** 로컬 환경에서 Python Vertex AI SDK를 사용하여 튜닝된 모델의 엔드포인트를 호출할 때 발생하는, 문서화되지 않은 복합적인 문제.
    -   **우회 전략:** 문제가 있는 SDK와 엔드포인트 호출을 포기하고, **`curl` 테스트에서 유일하게 성공했던 기본 모델의 `:generateContent` API를 직접 호출**하는 방식으로 최종 결정.
    -   **최종 구현:** `api_server.py`에서 `vertexai` SDK를 모두 제거하고, `requests`와 `subprocess` 라이브러리를 사용하여 `gcloud`로 액세스 토큰을 받아 REST API를 직접 호출하도록 수정.

### 5. `FileNotFoundError: [WinError 2]`

-   **원인:** `subprocess.Popen`으로 `gcloud` 명령어를 호출할 때, Windows가 시스템 `PATH`에서 `gcloud.exe`를 찾지 못함.
-   **해결책:** `subprocess.Popen` 호출 시 `shell=True` 옵션을 추가하여, Windows의 기본 셸이 `PATH`를 해석하도록 함.