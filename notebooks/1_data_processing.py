# # 1. 데이터 처리 (Data Processing)
#
# **목표:** `google_play_reviews_integrated.csv` 원본 데이터를 탐색하고, AI 모델 학습에 적합한 'prompt'와 'completion' 형식의 `training_data.csv`를 생성합니다.

# ## 1.1. 라이브러리 임포트 및 설정

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (Windows)
plt.rc('font', family='Malgun Gothic')

# 마이너스 부호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# ## 1.2. 데이터 불러오기

import os

# 스크립트 파일의 디렉터리를 기준으로 경로 설정
script_dir = os.path.dirname(__file__)
input_file_path = os.path.join(script_dir, '../data/processed_data/google_play_reviews_integrated.csv')
output_file_path = os.path.join(script_dir, '../data/processed_data/training_data.jsonl')

try:
    df = pd.read_csv(input_file_path)
    print(f"'{input_file_path}' 파일을 성공적으로 불러왔습니다.")
except FileNotFoundError:
    print(f"오류: 파일을 찾을 수 없습니다. 경로를 확인하세요: {input_file_path}")

# ## 1.3. 데이터 탐색 (Exploratory Data Analysis)

print("--- 데이터 샘플 (상위 5개) ---")
# display(df.head()) # display() is for notebooks, use print() in scripts
print(df.head())

print("\n--- 데이터 정보 (데이터 타입, 결측치 등) ---")
df.info()

# 'Review Title'이 있는 데이터 개수 확인
if 'Review Title' in df.columns:
    # NaN 값을 빈 문자열로 대체 후, 공백 제거하고 비어있지 않은 문자열의 개수를 셉니다.
    review_title_count = df['Review Title'].fillna('').str.strip().astype(bool).sum()
    print(f"\n'Review Title'이(가) 포함된 리뷰 수: {review_title_count}")

# 별점 분포 시각화

plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Star Rating')
plt.title('리뷰 별점 분포')
plt.xlabel('별점')
plt.ylabel('리뷰 수')
plt.show()

# ## 1.4. 데이터 전처리 및 학습 데이터셋 생성

print(f"원본 데이터 크기: {df.shape}")

# 'Review Link' 열은 프롬프트 생성에 필요 없으므로 제거합니다.
if 'Review Link' in df.columns:
    df.drop(columns=['Review Link'], inplace=True)
    print("'Review Link' 열을 제거했습니다.")

# 'Review Title' 열은 유의미한 데이터가 없으므로 제거합니다.
if 'Review Title' in df.columns:
    df.drop(columns=['Review Title'], inplace=True)
    print("'Review Title' 열을 제거했습니다.")

# 'Review Text' 또는 'Developer Reply Text' 열이 비어있는 행은 학습에 사용할 수 없으므로 제거합니다.
df.dropna(subset=['Review Text', 'Developer Reply Text'], inplace=True)
df = df[df['Review Text'].str.strip() != '']
df = df[df['Developer Reply Text'].str.strip() != '']
print(f"전처리 후 최종 데이터 크기: {df.shape}")

def create_prompt(row):
    # 'Developer Reply Text' 열을 제외한 모든 열을 prompt로 구성
    prompt_cols = row.drop('Developer Reply Text')
    # 각 열에 대해 "키: 값" 형식의 문자열을 만들고 줄바꿈으로 연결
    return '\n'.join([f"{col}: {val}" for col, val in prompt_cols.items()])

# prompt 생성
prompts = df.apply(create_prompt, axis=1)

# completion 은 'Developer Reply Text' 열
completions = df['Developer Reply Text'].astype(str).str.strip()

# 새로운 데이터프레임 생성
training_df = pd.DataFrame({
    'prompt': prompts,
    'completion': completions
})

print("학습 데이터셋 생성 완료.")

# ## 1.5. ���성된 데이터셋 확인 및 저장

print(f"최종 데이터셋 크기: {training_df.shape}")
print("\n--- 생성된 데이터 샘플 ---")
for i in range(min(3, len(training_df))):
    print("[PROMPT]")
    print(training_df.iloc[i]['prompt'])
    print("\n[COMPLETION]")
    print(training_df.iloc[i]['completion'])
    print("------------------------------------\n")

# .jsonl 파일로 저장
training_df.to_json(output_file_path, orient='records', lines=True, force_ascii=False)

print(f"학습 데이터가 성공적으로 '{output_file_path}' 에 저장되었습니다.")
