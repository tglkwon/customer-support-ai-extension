import os
import glob
import re
import email
from email import policy
from email.parser import BytesParser
from tqdm import tqdm
import pandas as pd

def get_email_body(msg):
    """
    이메일 메시지 객체에서 플레인 텍스트 본문을 추출합니다.
    멀티파트 이메일의 경우, 'text/plain' 파트만 찾아서 반환합니다.
    """
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    # 다양한 인코딩을 시도하여 본문을 디코딩합니다.
                    charset = part.get_content_charset('utf-8')
                    payload = part.get_payload(decode=True)
                    body = payload.decode(charset, 'replace')
                    break # 첫 번째 플레인 텍스트 파트를 찾으면 중단
                except (UnicodeDecodeError, AttributeError, LookupError):
                    # 디��딩 실패 시 다른 방법 시도
                    try:
                        body = part.get_payload(decode=False)
                    except Exception:
                        body = "[Body Decode Error]"
    else:
        # 싱글파트 이메일의 경우
        try:
            charset = msg.get_content_charset('utf-8')
            payload = msg.get_payload(decode=True)
            body = payload.decode(charset, 'replace')
        except (UnicodeDecodeError, AttributeError, LookupError):
            try:
                body = msg.get_payload(decode=False)
            except Exception:
                body = "[Body Decode Error]"
    return body

def anonymize_text(text):
    """
    주어진 텍스트에서 이메일 주소와 URL을 비식별화합니다.
    """
    if not isinstance(text, str):
        return ""
    # 이메일 주소 비식별화
    text = re.sub(r'[\w\.-]+@[\w\.-]+', '[email_address]', text)
    # URL 비식별화
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '[url]', text)
    return text

def main():
    """
    메인 실행 함수
    """
    # 이 스크립트 파일의 위치를 기준으로 프로젝트 루트 디렉터리를 찾습니다.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))

    # 입력 및 출력 디렉터리 경로를 설정합니다.
    input_dir = os.path.join(project_root, 'data', 'raw_data', 'email')
    output_dir = os.path.join(project_root, 'data', 'processed_data')
    output_filepath = os.path.join(output_dir, 'emails_processed.csv')

    # 출력 디렉터리가 없으면 생성합니다.
    os.makedirs(output_dir, exist_ok=True)

    # 입력 디렉터리에서 모든 .eml 파일 목록을 가져옵니다.
    eml_files = glob.glob(os.path.join(input_dir, '*.eml'))

    if not eml_files:
        print(f"No .eml files found in {input_dir}")
        return

    processed_data = []
    
    print(f"Found {len(eml_files)} .eml files. Starting processing...")

    # tqdm을 사용하여 진행률 표시
    for file_path in tqdm(eml_files, desc="Processing emails"):
        try:
            with open(file_path, 'rb') as f:
                msg = BytesParser(policy=policy.default).parse(f)

            date = msg.get('Date', 'N/A')
            subject = msg.get('Subject', 'N/A')

            # 답변 메일인지 확인 (제목에 'Re:'가 포함되어 있는지)
            if subject and 're:' in subject.lower():
                message_id = msg.get('Message-ID', 'N/A')
                in_reply_to = msg.get('In-Reply-To', 'N/A')
                references = msg.get('References', 'N/A')
                language = msg.get('Content-Language', 'N/A')
                
                body = get_email_body(msg)
                anonymized_body = anonymize_text(body)

                processed_data.append({
                    'source_file': os.path.basename(file_path),
                    'date': date,
                    'subject': subject,
                    'message_id': message_id,
                    'in_reply_to': in_reply_to,
                    'references': references,
                    'language': language,
                    'body_anonymized': anonymized_body
                })
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    if not processed_data:
        print("No data was processed. Output file will not be created.")
        return

    # 데이터프레임으로 변환 후 CSV로 저장
    df = pd.DataFrame(processed_data)
    # Excel에서 한글이 깨지지 않도록 'utf-8-sig' 인코딩 사용
    df.to_csv(output_filepath, index=False, encoding='utf-8-sig')

    # 상위 10개 행을 별도의 _head.csv 파일로 저장합니다.
    head_output_filepath = os.path.join(output_dir, 'emails_processed_head.csv')
    df.head(10).to_csv(head_output_filepath, index=False, encoding='utf-8-sig')

    print(f"\nSuccessfully processed {len(df)} files.")
    print(f"Output file saved to: {output_filepath}")
    print(f"Head file (first 10 rows) saved to: {head_output_filepath}")

if __name__ == '__main__':
    main()
