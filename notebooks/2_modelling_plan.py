# # 2. 모델링 계획 (Modelling Plan)
#
**목표:** `1_data_processing.ipynb`에서 생성된 최종 학습 데이터(`training_data.csv`)를 최종 검수한 뒤, Phase 2에서 진행할 AI 모델 학습의 구체적인 계획을 수립합니다.

import pandas as pd

# ## 2.1. 최종 학습 데이터셋 불러오기 및 확인

training_data_path = '../data/processed_data/training_data.csv'

try:
    df_train = pd.read_csv(training_data_path)
    print(f"'{training_data_path}' 파일을 성공적으로 불러왔습니다.")
except FileNotFoundError:
    print(f"오류: 파일을 찾을 수 없습니다. `1_data_processing.ipynb` 노트북을 먼저 실행하세요.")

# 데이터 구조 및 내용 확인
if 'df_train' in locals():
    print(f"학습 데이터셋 크기: {df_train.shape}")
    print("\n--- 데이터 샘플 ---")
    # prompt와 completion이 잘렸을 경우, 전체 내용이 보이도록 설정
    pd.set_option('display.max_colwidth', None)
    # display(df_train.head()) # display() is for notebooks, use print() in scripts
    print(df_train.head())

# ## 2.2. Phase 2: 모델 파인튜닝 계획
#
# Phase 1의 마지막 단계인 Part 4 (클라우드 인프라 설정)가 완료되면, Phase 2에서�� GCP Vertex AI를 사용하여 본격적인 모델 학습을 시작합니다.
#
# **다음 단계:**
#
# 1.  **GCP 프로젝트 생성 및 API 활성화 (Part 4)**
#     - `phase_1_plan.md` 문서를 참고하여 GCP 프로젝트를 생성하고, Vertex AI 및 Cloud Storage API를 활성화합니다.
#
# 2.  **Cloud Storage에 학습 데이터 업로드 (Part 4)**
#     - 이 노트북에서 확인한 `training_data.csv` 파일을 생성된 GCP Cloud Storage 버킷에 업로드합니다.
#     - **업로드 경로 예시:** `gs://[YOUR-BUCKET-NAME]/data/training_data.csv`
#
# 3.  **Vertex AI PaLM 2 모델 파인튜닝 작업 실행 (Phase 2)**
#     - Vertex AI의 '생성형 AI' 스튜디오으로 이동하여 '튜닝' 메뉴를 선택합니다.
#     - 기반 모델로 `text-bison` (PaLM 2 for Text)을 선택합니다.
#     - 데이터 소스로 위에서 업로드한 Cloud Storage의 `training_data.csv` 파일 경로를 지정합니다.
#     - 모델 튜닝 작업을 시작하고, 완료될 때까지 대기합니다. (수십 분 ~ 몇 시간 소요 예상)
#
# 4.  **튜닝된 모델 평가 및 배포 (Phase 2)**
#     - 학습이 완료된 모델의 성능을 평가합니다.
#     - 만족스러운 결과가 나오면, 모델을 엔드포인트에 배포하여 API 형태로 호출할 수 있도록 준비합니다.

# ### (참고) GCP 인증 및 gcloud CLI 설정
#
# Phase 2에서 Vertex AI 작업을 스크립트로 실행하려면, 로컬 환경에 GCP SDK(gcloud CLI)를 설치하고 인증을 받아야 합니다.

# !gcloud auth application-default login
# !gcloud config set project [YOUR-PROJECT-ID]
