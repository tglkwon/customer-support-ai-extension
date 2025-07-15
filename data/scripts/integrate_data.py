import os
import pandas as pd
import glob

# 이 스크립트 파일의 위치를 기준으로 프로젝트 루트 디렉터리를 찾습니다.
# (data/scripts/ -> project_root)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 입력 및 출력 디렉터리 경로를 설정합니다.
input_dir = os.path.join(project_root, 'data', 'raw_data', 'google_play')
output_dir = os.path.join(project_root, 'data', 'processed_data')
output_filepath = os.path.join(output_dir, 'google_play_reviews_integrated.csv')

# 출력 디렉터리가 없으면 생성합니다.
os.makedirs(output_dir, exist_ok=True)

# 입력 디렉터리에서 모든 CSV 파일 목록을 가져옵니다.
csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

if not csv_files:
    print(f"No CSV files found in {input_dir}")
else:
    # 각 CSV 파일을 담을 리스트를 생성합니다.
    df_list = []
    print("Starting to read CSV files...")
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        try:
            # UTF-16 인코딩으로 CSV 파일을 읽습니다.
            df = pd.read_csv(file_path, encoding='utf-16')
            df_list.append(df)
            print(f"  - Successfully read: {filename}")
        except Exception as e:
            print(f"  - Failed to read {filename}. Error: {e}")

    if df_list:
        # ���든 데이터프레임을 하나로 합칩니다.
        integrated_df = pd.concat(df_list, ignore_index=True)
        
        # 통합된 데이터프레임을 UTF-8 인코딩으로 저장합니다.
        integrated_df.to_csv(output_filepath, index=False, encoding='utf-8-sig')
        
        # 상위 10개 행을 별도의 _head.csv 파일로 저장합니다.
        head_output_filepath = os.path.join(output_dir, 'google_play_reviews_integrated_head.csv')
        integrated_df.head(10).to_csv(head_output_filepath, index=False, encoding='utf-8-sig')

        print(f"""
Successfully integrated {len(df_list)} files.
Total rows: {len(integrated_df)}
Output file saved to: {output_filepath}
Head file (first 10 rows) saved to: {head_output_filepath}
""")
    else:
        print("\nNo dataframes were created. Could not generate output file.")
