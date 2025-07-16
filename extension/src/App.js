import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [reply, setReply] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // 테스트를 위한 기본 프롬프트 예시
  const defaultPrompt = `Package Name: com.banjihagames.seoul2033_backer
App Version Name: 3.8.0
Reviewer Language: ko
Device: a52s
Review Submit Date and Time: 2024-07-17T10:00:00Z
Star Rating: 1
Review Text: 업데이트 이후로 게임이 계속 튕겨요. 실행조차 안 됩니다.`;

  const handleGenerateReply = async () => {
    if (!prompt.trim()) {
      setError('리뷰 내용을 입력해주세요.');
      return;
    }
    
    setLoading(true);
    setError('');
    setReply('');

    try {
      const response = await axios.post('http://localhost:8000/generate-reply', {
        prompt: prompt,
      });
      setReply(response.data.reply);
    } catch (err) {
      console.error("API 호출 오류:", err);
      setError('답변 생성에 실패했습니다. API 서버가 실행 중인지 확인해주세요.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h2>AI 고객 지원 답변 생성기</h2>
        <div className="container">
          <div className="form-group">
            <label htmlFor="prompt-textarea">고객 리뷰 원문 (Prompt)</label>
            <textarea
              id="prompt-textarea"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="여기에 고객 리뷰 내용을 입력하세요..."
              rows="10"
            />
            <button onClick={() => setPrompt(defaultPrompt)} className="secondary-button">
              예시 프롬프트 채우기
            </button>
          </div>

          <button onClick={handleGenerateReply} disabled={loading}>
            {loading ? '답변 생성 중...' : 'AI 답변 생성'}
          </button>

          {error && <p className="error-message">{error}</p>}

          {reply && (
            <div className="result-group">
              <label htmlFor="reply-textarea">AI 생성 답변 (Completion)</label>
              <textarea
                id="reply-textarea"
                value={reply}
                readOnly
                rows="10"
              />
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
