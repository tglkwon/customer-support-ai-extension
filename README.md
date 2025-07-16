# customer-support-ai-extension

---
### 작업 기록

#### v0.3.0: API 서버 및 프론트엔드 연동을 위한 전체 시스템 구축
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

#### v0.2.0: AI 학습 데이터셋 구축 및 데이터 파이프라인 정제
```
feat(data): AI 학습 데이터셋 생성 및 파이프라인 정제

- 노트북 구조 리팩토링:
  - 기존 3개의 노트북(탐색, 튜닝, 생성)을 역할에 따라 2개(데이터 처리, 모델링 계획)로 재구성하여 파이프라인의 명확성을 높임.
  - `1_data_processing.ipynb`: 데이터 탐색, 전처리, 학습셋 생성을 통합.
  - `2_modelling_plan.ipynb`: 생성된 학습셋을 검증하고 향후 모델링 계획을 수립.

- 데이터 처리 파이프라인 개선:
  - `integrate_data.py`: 여러 CSV를 통합하는 역할에만 집중하도록 수정 (데이터 필터링 기능 제거).
  - `1_data_processing.ipynb`: 데이터 정제(답변 없는 리뷰 제거 등) 로직을 담당하도록 역할을 명확히 함.

- 학습 데이터셋 생성 완료:
  - 수정된 파이프라인을 실행하여 606개의 유효한 'prompt/completion' 쌍으로 구성된 `training_data.csv` 파일 생성을 완료함.
  - 이로써 AI 모델 파인튜닝을 위한 데이터 준비(Phase 1, Part 3)를 마침.
```

---
### 다음 단계 (Next Steps)

- **Part 5: 튜닝된 모델 테스트 및 확장 프로그램 연동**
    1. **튜닝된 모델 ID 확인 및 적용**
        - Vertex AI의 '튜닝' 페이지에서 완료된 작업의 모델 ID를 복사합니다.
        - `api_server.py` 파일의 `TUNED_MODEL_ID` 변수 값을 복사한 ID로 교체합니다.
    2. **백엔드 API 서버 실행**
        - 프로젝트 루트 디렉터리에서 다음 명령어를 실행합니다: `uvicorn api_server:app --reload --port 8000`
    3. **프론트엔드 앱 실행 및 테스트**
        - 별도의 터미널에서 `extension` 디렉터리로 이동 후 `npm start`를 실행합니다.
        - 브라우저(localhost:3000)에서 'AI 답변 생성' 기능이 정상적으로 동작하는지 테스트합니다.
    4. **브라우저 확장 프로그램으로 빌드 및 테스트**
        - 프론트엔드 테스트가 완료되면, `npm run build` 명령어로 확장 프로그램을 빌드합니다.
        - 빌드된 `extension/build` 폴더를 브라우저의 '압축해제된 확장 프로그램을 로드합니다' 기능을 사용하여 실제 환경에서 테스트합니다.

