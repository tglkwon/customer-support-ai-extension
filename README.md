# Customer Support AI Extension

**Version:** `v1.6`

이 프로젝트는 고객 지원(CS) 업무, 특히 앱 리뷰나 이메일 문의에 대한 답변을 AI를 통해 자동 생성하여 업무 효율을 높이는 브라우저 확장 프로그램입니다.

---

### 🛠️ 로컬 개발 환경 설정

새로운 컴퓨터에서 이 프로젝트를 실행하기 위해 필요한 설정 과정입니다.

1.  **프로젝트 복제 (Clone):**
    ```bash
    git clone https://github.com/tglkwon/customer-support-ai-extension.git
    cd customer-support-ai-extension
    ```

2.  **파이썬 가상 환경 생성 및 활성화:**
    - **가상 환경 생성 (공통):**
      ```bash
      python -m venv venv
      ```
    - **가상 환경 활성화:** 운영체제와 터미널 종류에 맞는 명령어를 사용하세요.
      - **Windows (CMD):**
        ```cmd
        .\venv\Scripts\activate
        ```
      - **Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
      - **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```
      > 활성화에 성공하면 터미널 프롬프트 맨 앞에 `(venv)`가 표시됩니다.

3.  **필요 라이브러리 설치:**
    > 반드시 가상 환경이 활성화된 상태(`(venv)`가 보이는 상태)에서 실행하세요.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Google API 키 설정:**
    [Google AI Studio](https://aistudio.google.com/app/apikey)에서 API 키를 발급받은 후, **서버를 실행할 바로 그 터미널에서** 아래 명령어를 실행하여 API 키를 설정합니다.
    - **Windows (CMD):**
      ```cmd
      set GOOGLE_API_KEY="YOUR_API_KEY_HERE"
      ```
    - **Windows (PowerShell):**
      ```powershell
      $env:GOOGLE_API_KEY="YOUR_API_KEY_HERE"
      ```
    - **macOS / Linux:**
      ```bash
      export GOOGLE_API_KEY='YOUR_API_KEY_HERE'
      ```

5.  **API 서버 실행:**
    > 반드시 가상 환경이 활성화되고 API 키가 설정된 터미널에서 실행하세요.
    ```bash
    uvicorn api_server:app --reload
    ```
    서버가 `http://127.0.0.1:8000`에서 실행됩니다.

6.  **브라우저 확장 프로그램 빌드 및 로드:**
    - `extension` 폴더로 이동하여 필요한 패키지를 설치하고 빌드합니다.
      ```bash
      cd extension
      npm install
      npm run build
      cd .. 
      ```
    - Chrome/Edge 브라우저에서 `chrome://extensions` 또는 `edge://extensions`로 이동합니다.
    - '개발자 모드'를 활성화합니다.
    - '압축 해제된 확장 프로그램을 로드합니다'를 클릭하고, 이 프로젝트의 `extension/build` 폴더를 선택합니다.

---

### 📝 작업 기록

#### v1.6: AI 모델 변경 (gemini-2.0-flash-lite)
```
refactor(model): AI 모델을 `gemini-2.0-flash-lite`로 변경

- **주요 변경:** `api_server.py`와 `test_model.py`에서 사용되는 AI 모델을 기존 `gemini-1.5-flash`에서 `gemini-2.0-flash-lite`로 업데이트했습니다.
```


#### v1.5: API 서버 프로덕션 배포 및 확장 프로그램 연동
```
feat(deploy): Gunicorn/Apache 기반 API 서버 배포 및 systemd 서비스 등록

- **주요 변경:** 개발 환경에서 실행되던 API 서버를 AWS 프로덕션 환경에 배포하고, 브라우저 확장 프로그램이 배포된 서버와 통신하도록 수정했습니다.
- **구현 내용:**
  - Gunicorn을 ASGI 워커(Uvicorn)와 함께 사용하여 FastAPI 애플리케이션을 실행하도록 설정.
  - Apache를 리버스 프록시로 설정하여 외부 요청을 Gunicorn으로 안전하게 전달.
  - Gunicorn 프로세스를 systemd 서비스로 등록하여 서버 재부팅 시 자동 시작 및 안정적인 운영을 보장.
  - 브라우저 확장 프로그램(App.js)의 API 요청 주소를 로컬(localhost)에서 프로덕션 서버 도메인으로 변경.
```

#### v1.4: API 호출 방식을 Vertex AI에서 Gemini API로 변경하고 기능 작동 시작함.
- **주요 변경:** 백엔드 API 서버(`api_server.py`)와 테스트 스크립트(`test_model.py`)가 튜닝된 Vertex AI 모델 대신, 표준 Gemini API (`gemini-1.5-flash`)를 사용하도록 전면 수정했습니다.
- **인증 방식:** `gcloud` 인증에서 `GOOGLE_API_KEY` 환경 변수를 사용하는 방식으로 변경하여 설정 과정을 간소화했습니다.
- **개발 환경:** 파이썬 가상 환경 설정 및 `requirements.txt`를 통한 라이브러리 관리 방법을 도입하고, `README.md`에 상세한 설정 가이드를 추가했습니다.

#### v1.3: 카테고리 기반 답변 생성 기능 추가 및 리드미 정리
```
feat(feature): 카테고리 선택을 통한 AI 답변 정확도 향상 기능 구현

- **주요 기능:**
  - AI 답변 생성 시, 문의 종류에 따른 '카테고리'를 선택하여 답변의 정확도를 높이는 기능 추가.
  - 사용자가 직접 카테고리를 선택하면, AI가 해당 분야의 전문가로서 답변을 생성하도록 프롬프트를 동적으로 변경.
- **구현 내용:**
  - 카테고리 목록을 관리하기 위한 `extension/public/categories.json` 설정 파일 추가.
  - `App.js`에 카테고리 선택 드롭다운 UI를 구현하고, 선택된 값을 API 서버로 전송.
  - `api_server.py`가 카테고리 값을 받아, 미리 정의된 역할(전문가 프롬프트)을 AI에 부여하도록 로직 수정.
  - '리뷰 5점', '4점 이하 불만 내용 없음' 등 신규 카테고리 2종 및 관련 프롬프트 추가.
- **기타:**
  - `README.md`의 작업 기록 버전 표기를 `vX.Y.Z`에서 `vX.Y` 형식으로 통일.
```

#### v1.2: Gmail 연동 기능 구현
```
feat(scraper): Gmail 연동을 통한 이메일 문의 추출 기능 구현

- **주요 기능:**
  - Gmail 웹페이지에서 현재 열려 있는 이메일의 제목, 작성자, 날짜, 본문을 추출하는 기능 추가.
- **구현 내용:**
  - `content_gmail.js` 콘텐츠 스크립트에 Gmail 페이지의 DOM에서 직접 이메일 정보를 추출하는 로직을 구현. (사용자와의 협업을 통해 CSS 선택자 확보)
  - `manifest.json`에 새 콘텐츠 스크립트가 `mail.google.com`에서 실행되도록 설정.
  - `App.js`의 로직을 수정하여, Gmail 페이지에서 '현재 페이지에서 리뷰 추출' 버튼 클릭 시 콘텐츠 스크립트가 실행되도록 변경.
```

#### v1.1: App Store 연동 방식 변경 (API → 웹 스크래핑)
```
refactor(scraper): App Store 리뷰 추출 방식을 API 호출에서 웹 스크래핑으로 변경

- **변경 이유:**
  - `api_server.py` 실행 및 환경 변수 설정의 번거로움을 없애고, 확장 프로그램 단독으로 작동하도록 사용성을 개선.
- **구현 내용:**
  - `content_appstore.js` 콘텐츠 스크립트를 새로 추가하여, App Store Connect 페이지의 DOM에서 직접 리뷰 정보를 추출하도록 구현. (사용자와의 협업을 통해 CSS 선택자 확보)
  - `manifest.json`에 새 콘텐츠 스크립트가 `appstoreconnect.apple.com`에서 실행되도록 설정.
  - `App.js`의 로직을 수정하여, 앱스토어 페이지에서 API 호출 대신 콘텐츠 스크립트를 실행하도록 변경.
  - 불필요해진 `api_server.py`의 App Store 관련 코드를 모두 삭제.
- **추가 수정:**
  - 리뷰 제목과 본문을 함께 추출하도록 로직 개선.
  - 작성자와 날짜가 뒤바뀌어 추출되던 버그 수정.
```

#### v1.0: 튜닝 모델 적용 및 App Store 연동 백엔드 구현
```
feat(api): 안정화된 튜닝 모델 적용 및 App Store 리뷰 API 구현

- **주요 변경 사항:**
  - `api_server.py`에서 API 요청 시, 기존의 기본 모델 대신 안정화된 튜닝 모델(`customer-support-ai-v2-stable`)을 사용하도록 업데이트하여 답변의 품질을 개선.
  - `README.md`에 장기 과제로 남아있던 튜닝 모델 엔드포인트 문제를 해결하고, 이를 기본 작동 방식으로 채택.
  - App Store Connect API를 통해 앱 리뷰를 직접 가져오는 백엔드 엔드포인트(`/fetch-app-store-reviews`)를 `api_server.py`에 추가. (프론트엔드 연동은 추후 과제)
```

#### v0.9: 리뷰 추출 워크플로우 및 UI/UX 개선
```
feat(workflow): 리뷰 추출 버튼 UI 개선 및 다중 리뷰 순회 기능 추가

- **UI/UX 개선:**
  - `content.js`가 페이지에 직접 생성하던 '리뷰 정보 추출하기' 버튼을 제거.
  - `App.js`의 사이드 패널 내부에 '현재 페이지에서 리뷰 추출' 버튼을 추가하여 워크플로우를 일원화.
- **기능 개선:**
  - `background.js`가 스크랩된 리뷰 배열 전체를 `chrome.storage`에 저장하도록 수정.
  - `App.js`에 '이전'/'다음' 버튼과 카운터(예: 3 / 10)를 추가하여, 추출된 여러 리뷰를 순서대로 넘겨볼 수 있는 기능 구현.
  - 전체적인 상태 관리 로직을 단일 리뷰에서 리뷰 배열 기반으로 리팩토링.
```

#### v0.8: 콘텐츠 스크립트를 이용한 구조화된 데이터 추출
```
feat(scraper): 콘텐츠 스크립트를 이용해 페이지의 구조화된 데이터(별점 포함) 추출 기능 구현

- **주요 기능:**
  - 구글 플레이 콘솔 페이지의 DOM을 직접 분석하여 리뷰 작성자, 날짜, 본문, **별점**을 포함한 전체 리뷰 데이터 추출.
- **구현 내용:**
  - `manifest.json`에 `content_scripts`를 설정하여 특정 페이지(`play.google.com/console`)에서 `content.js`가 실행되도록 함.
  - `content.js`에 CSS 선택자를 기반으로 페이지의 리뷰 정보를 스크래핑하는 로직을 작성. (사용자와의 협업을 통해 정확한 선택자 확보)
  - `background.js`가 스크랩된 데이터를 받아 `chrome.storage`에 저장하고, 사이드 패널에 업데이트를 알리도록 수정.
  - `App.js`가 구조화된 데이터를 받아 UI에 올바르게 표시하도록 상태 및 UI 로직을 업데이트.
```

#### v0.7: 확장 프로그램 UI 리팩토링 및 버그 수정
```
refactor(ui): 팝업 방식의 UI를 사이드 패널로 개선

- **문제점:** 기존 팝업 방식은 폭이 좁고, 외부 클릭 시 닫혀버려 텍스트 선택 및 내용 확인이 불편했음.
- **해결 조치:**
  - `manifest.json`을 수정하여 확장 프로그램의 동작을 'action popup'에서 'sidePanel'로 변경.
  - `background.js`를 수정하여 툴바 아이콘 클릭 및 컨텍스트 메뉴 실행 시 사이드 패널이 열리도록 로직 추가.
  - `App.css`에 `min-width`를 설정하여 사이드 패널의 최소 너비를 확보하고 UI가 깨지지 않도록 수정.

fix(bug): 사이드 패널이 열려있을 때 내용이 업데이트되지 않는 버그 수정

- **문제점:** 사이드 패널이 이미 열려있는 상태에서 컨텍스트 메뉴를 사용하면, 패널의 내용이 새로운 텍스트로 업데이트되지 않았음.
- **해결 조치:**
  - `background.js`가 컨텍스트 메뉴 클릭 시 `chrome.runtime.sendMessage`를 통해 메시지를 보내도록 수정.
  - `App.js`가 `chrome.runtime.onMessage` 리스너를 통해 해당 메시지를 수신하고, 수신 시 `chrome.storage`에서 최신 데이터를 가져와 화면을 업데이트하도록 리팩토링.
- **기대 효과:** 사용자가 웹페이지의 내용과 상호작용하면서 동시에 확장 기능을 편리하게 사용할 수 있게 됨.
```

#### v0.6: 외부 웹페이지 연동 기능 구현 (1단계)
```
feat(extension): 외부 웹페이지 텍스트 연동을 위한 컨텍스트 메뉴 구현

- **주요 기능:**
  - 웹페이지에서 텍스트 선택 후, 우클릭 메뉴('AI로 답변 생성하기')를 통해 해당 텍스트와 URL을 확장 프로그램으로 전송.
- **구현 내용:**
  - `manifest.json` 파일을 생성하여 확장 프로그램의 기본 구조(권한, 백그라운드 스크립트 등)를 설정.
  - `background.js` 스크립트를 생성하여 컨텍스트 메뉴 생성, 클릭 이벤트 처리, `chrome.storage`를 이용한 데이터 전달 로직을 구현.
  - `App.js`를 수정하여 확장 프로그램이 열릴 때 `chrome.storage`에 저장된 텍스트가 있는지 확인하고, 자동으로 입력창에 채워 넣는 기능 추가.
```

#### v0.5: 답변 복사하기 기능 추가
```
feat(ux): AI 생성 답변 '복사하기' 버튼 기능 추가

- AI가 생성한 답변 텍스트 박스 하단에 '답변 복사하기' 버튼을 추가함.
- 버튼 클릭 시, 답변이 클립보드에 복사되고 버튼 텍스트가 '복사 완료!'로 잠시 변경되어 사용자에게 피드백을 제공.
- `App.js`에 `handleCopy` 함수와 `isCopied` 상태를 추가하여 구현.
```

#### v0.4: Vertex AI 모델 연동 트러블슈팅 재튜닝
```
fix(model): Vertex AI 모델 연동 오류 해결 및 재튜닝

- 튜닝된 모델 연동 과정에서 발생한 `400`, `403`, `404` 오류를 해결하기 위한 집중적인 트러블슈팅을 진행함.
- **문제 원인 규명:**
  - **리전 불일치:** API 호출 리전과 모델이 실제 위치한 리전이 달라 발생한 문제.
  - **권한 부족:** `gemini-1.5-flash` 모델을 사용하기 위한 프로젝트 사전 승인(allowlist)이 누락됨.
  - **잘못된 모델 ID 및 SDK 사용법:** 초기 단계에서 부정확한 모델 ID를 사용하고, 튜닝된 모델에 맞지 않는 SDK 클래스(`aiplatform.Endpoint`)를 시도하는 등 여러 시행착오를 겪음.
- **해결 조치:**
  - `TROUBLESHOOTING.md` 파일을 생성하여 모든 오류의 원인과 해결 과정을 상세히 기록함.
  - 권한 문제가 없고 안정적인 **`gemini-1.0-pro-002`** 모델을 기반으로, **`us-central1`** 리전에서 새로운 모델(`customer-support-ai-v2-stable`) 튜닝을 시작함.
- **프론트엔드 개선:**
  - `App.js`를 리팩토링하여 API 요청 시 모델이 학습한 형식과 동일한 프롬프트를 생성하도록 수정.
  - 초기 UI를 개선하고 '예시 프롬프트 채우기' 기능을 복원하여 사용자 경험을 향상시킴.
```

#### v0.3: API 서버 및 프론트엔드 연동을 위한 전체 시스템 구축
```
feat(system): API 서버 및 프론트엔드 연동을 위한 전체 시스템 구축

- 데이터 파이프라인 개선:
  - Jupyter Notebook을 Python 스크립트(`.py`)로 변환.
  - 데이터 처리 스크립트(`1_data_processing.py`) 리팩토링:
    - 불필요한 데이터(리뷰 없는 행, 제목/링크 열) 제거 로직 추가.
    - Vertex AI 튜닝을 위해 출력 형식을 CSV에서 JSONL로 변경.

- 백엔드 API 서버 구축:
  - FastAPI를 사용하여 Vertex AI 모델을 호출하는 API 서버(`api_server.py`) 생성.
  - React 프론트엔드와 통신을 위한 CORS 설정 포함.

- 프론트엔드 UI 구현:
  - API 서버와 연동할 수 있도록 React 앱(`extension/src/App.js`) 재구성.
  - `axios`를 사용한 비동기 API 호출 로직 추가.
  - 리뷰 입력, 답변 생성 버튼, 결과 표시 등 전체 UI 구현.

- 프로젝트 계획 업데이트:
  - 모델 튜닝 계획을 Google AI Studio에서 Vertex AI로 공식화하고 README.md에 반영.
```

#### v0.2: AI 학습 데이터셋 구축 및 데이터 파이프라인 정제
```
feat(data): AI 학습 데이터셋 생성 및 파이프라인 정제

- 노트북 구조 리팩토링:
  - 기존 3개의 노트북(탐색, 튜닝, 생성)을 역할에 따라 2개(데이터 처리, 모델링 계획)로 구성하여 파이프라인의 명확성을 높임.
  - `1_data_processing.ipynb`: 데이터 탐색, 전처리, 학습셋 생성을 통합.
  - `2_modelling_plan.ipynb`: 생성된 학습셋을 검증하고 향후 모델링 계획을 수립.

- 데이터 처리 파이프라인 개선:
  - `integrate_data.py`: 여러 CSV를 통합하는 역할에만 집중하도록 수정 (데이터 필터링 기능 제거).
  - `1_data_processing.ipynb`: 데이터 정제(답변 없는 리뷰 제거 등) 로직을 담당하도록 역할을 명확히 함.

- 학습 데이터셋 생성 완료:
  - 수정된 파이프라인을 실행하여 606개의 유효한 'prompt/completion' 쌍으로 구성된 `training_data.csv` 파일 생성을 완료함.
  - 이로써 AI 모델 파인튜닝을 위한 데이터 준비(Phase 1, Part 3)를 마침.
```