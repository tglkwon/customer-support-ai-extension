# Gemini 사용을 위한 프롬프트 모음

## 프로젝트 요약
README.md 파일 읽고 이 프로젝트의 계획, 앞으로 할일을 확인하고, 이 프로젝트에 포함된 파일들을 읽어서 현재까지의 진행상황을 판단해봐.




curl -X POST \
-H "Authorization: Bearer ya29.a0AS3H6Nxh0ODGSo-ufUfsRTwd1KKqnCprzibvVCeTCqI_yEGg9BQ4yes4C1cedYYfL0OZQOQY8m_A4y7Bh3Cs59sHxTWn-19gPxuyn1bZex3Ga8Qf7kYtMgqxEKiQd7La9dr8w8SjQNmH9ovQgSkbHHBTQ1bOTABKcmf-QQwQaCgYKAakSARcSFQHGX2MipeXzK1jIFy_Cr_YHU74iRQ017" \
     -H "Content-Type: application/json" \
     "https://us-central1-aiplatform.googleapis.com/v1/projects/442212722968/locations/us-central1/endpoints/2380360210762956800:predict" \
     -d \
     $'{
       "instances": [
         {
           "prompt": "Package Name: com.banjihagames.seoul2033_backer\\nApp Version Name: 3.8.0\\nReviewer Language: ko\\nDevice: a52s\\nReview Submit Date and Time: 
      2024-07-17T10:00:00Z\\nStar Rating: 1\\n\\nReview Text: 업데이트 이후로 게임이 계속 튕겨요. 실행조차 안 됩니다."
        }
      ]
    }'