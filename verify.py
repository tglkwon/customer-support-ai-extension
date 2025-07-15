import pandas as pd
pd.set_option('display.max_colwidth', None)
try:
    df = pd.read_csv('data/processed_data/training_data.csv')
    print(f'학습 데이터셋 크기: {df.shape}')
    print('\n--- 데이터 샘플 ---')
    print(df.head())
except FileNotFoundError:
    print("오류: data/processed_data/training_data.csv 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"오류 발생: {e}")

