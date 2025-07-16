import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// 기본값과 빈 상태를 미리 정의
const defaultReview = {
  packageName: 'com.banjihagames.seoul2033_backer',
  appVersion: '3.8.0',
  language: 'ko',
  device: 'a52s',
  submitTime: '2024-07-17T10:00:00Z',
  rating: 1,
  text: '업데이트 이후로 게임이 계속 튕겨요. 실행조차 안 됩니다.',
};

const emptyReview = {
  packageName: '',
  appVersion: '',
  language: '',
  device: '',
  submitTime: '',
  rating: '',
  text: '',
};

function App() {
  // 초기 상태를 완전히 비운다
  const [review, setReview] = useState(emptyReview);
  
  const [fullPrompt, setFullPrompt] = useState('');
  const [reply, setReply] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // review 객체가 변경될 때마다 fullPrompt를 업데이트
  useEffect(() => {
    const generateFullPrompt = () => {
      if (!review.text.trim()) return '';
      
      return `Package Name: ${review.packageName}
App Version Name: ${review.appVersion}
Reviewer Language: ${review.language}
Device: ${review.device}
Review Submit Date and Time: ${review.submitTime}
Star Rating: ${review.rating}
Review Text: ${review.text}`;
    };
    setFullPrompt(generateFullPrompt());
  }, [review]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    // 사용자가 직접 입력할 때는 기본 컨텍스트를 채워준다
    if (name === 'text' && !review.packageName) {
      setReview(prev => ({ ...prev, ...defaultReview, text: value }));
    } else {
      setReview(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleGenerateReply = async () => {
    if (!review.text.trim()) {
      setError('리뷰 내용을 입력해주세요.');
      return;
    }
    
    setLoading(true);
    setError('');
    setReply('');

    try {
      const response = await axios.post('http://localhost:8000/generate-reply', {
        prompt: fullPrompt,
      });
      setReply(response.data.reply);
    } catch (err) {
      console.error("API 호출 오류:", err);
      let errorMessage = '답변 생성에 실패했습니다. API 서버가 실행 중인지 확인해주세요.';
      if (err.response && err.response.data && err.response.data.reply) {
        errorMessage = err.response.data.reply;
      }
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // 예시 프롬프트 채우기 핸들러
  const fillWithDefaultPrompt = () => {
    setReview(defaultReview);
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
              name="text"
              value={review.text}
              onChange={handleInputChange}
              placeholder="여기에 고객 리뷰 내용을 입력하세요..."
              rows="6"
            />
            {/* 컨텍스트 정보가 있을 때만 표시 */}
            {review.packageName && (
              <div className="context-display">
                <strong>Context:</strong>
                <p>Package: {review.packageName}, Version: {review.appVersion}, Rating: {review.rating} stars</p>
              </div>
            )}
            <button onClick={fillWithDefaultPrompt} className="secondary-button">
              예시 프롬프트 채우기
            </button>
          </div>

          <button onClick={handleGenerateReply} disabled={loading || !review.text.trim()}>
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
