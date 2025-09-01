import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// 기본값과 빈 상태를 미리 정의
const emptyReview = {
  packageName: '',
  appVersion: '',
  language: 'ko',
  device: '',
  submitTime: '',
  rating: '',
  author: '',
  text: '',
};

function App() {
  // --- State Management --- //
  const [reviews, setReviews] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [fullPrompt, setFullPrompt] = useState('');
  const [reply, setReply] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isCopied, setIsCopied] = useState(false);

  const currentReview = reviews[currentIndex] || null;

  // --- Data Fetching and Syncing --- //

  // 저장소에서 리뷰 목록을 가져와 상태를 업데이트하는 함수
  const fetchAndSetReviews = () => {
    /* global chrome */
    if (!window.chrome || !window.chrome.storage) return;

    chrome.storage.local.get(['reviews', 'currentIndex'], (result) => {
      if (result.reviews && result.reviews.length > 0) {
        setReviews(result.reviews);
        setCurrentIndex(result.currentIndex || 0);
      }
    });
  };

  // 1. 메시지 리스너 설정 및 초기 데이터 로드
  useEffect(() => {
    // 초기 로드
    fetchAndSetReviews();

    const messageListener = (message) => {
      if (message.type === 'REVIEWS_UPDATED') {
        fetchAndSetReviews();
      } else if (message.type === 'SHOW_SCRAPE_FAILED_ERROR') {
        setError('리뷰를 찾을 수 없습니다. CSS 선택자를 확인해주세요.');
      }
    };

    if (window.chrome && window.chrome.runtime) {
      chrome.runtime.onMessage.addListener(messageListener);
    }
    return () => {
      if (window.chrome && window.chrome.runtime) {
        chrome.runtime.onMessage.removeListener(messageListener);
      }
    };
  }, []);

  // 2. currentReview가 변경될 때마다 AI에게 보낼 fullPrompt를 업데이트
  useEffect(() => {
    if (!currentReview) {
      setFullPrompt('');
      return;
    }
    const generateFullPrompt = () => {
      return `Author: ${currentReview.author}\nPackage Name: ${currentReview.url || 'N/A'}\nReview Submit Date and Time: ${currentReview.date}\nStar Rating: ${currentReview.stars}\nReview Text: ${currentReview.text}`;
    };
    setFullPrompt(generateFullPrompt());
  }, [currentReview]);


  // --- Event Handlers --- //

  const handleInitiateScrape = () => {
    setError('');
    setReviews([]); // 기존 리뷰 초기화
    /* global chrome */
    if (window.chrome && window.chrome.runtime) {
      chrome.runtime.sendMessage({ type: 'INITIATE_SCRAPE' });
    }
  };

  const handleNavigate = (direction) => {
    const newIndex = currentIndex + direction;
    if (newIndex >= 0 && newIndex < reviews.length) {
      setCurrentIndex(newIndex);
      // 변경된 인덱스를 저장소에 동기화
      chrome.storage.local.set({ currentIndex: newIndex });
    }
  };

  const handleGenerateReply = async () => {
    if (!currentReview) {
      setError('리뷰 내용이 없습니다.');
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
      setError('답변 생성에 실패했습니다. API 서버가 실행 중인지 확인해주세요.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(reply).then(() => {
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    });
  };

  // --- JSX --- //
  return (
    <div className="App">
      <header className="App-header">
        <h2>AI 고객 지원 답변 생성기</h2>

        <div className="container">
          <div className="form-group-row">
             <button onClick={handleInitiateScrape} className="primary-button">
              현재 페이지에서 리뷰 추출
            </button>
          </div>

          {reviews.length > 0 && currentReview && (
            <div className="review-navigation">
              <button onClick={() => handleNavigate(-1)} disabled={currentIndex === 0}>
                이전
              </button>
              <span>{currentIndex + 1} / {reviews.length}</span>
              <button onClick={() => handleNavigate(1)} disabled={currentIndex === reviews.length - 1}>
                다음
              </button>
            </div>
          )}

          <div className="form-group">
            <label htmlFor="prompt-textarea">고객 리뷰 원문 (Prompt)</label>
            <textarea
              id="prompt-textarea"
              name="text"
              value={currentReview ? currentReview.text : ''}
              readOnly
              placeholder="여기에 고객 리뷰 내용이 표시됩니다..."
              rows="8"
            />
            {currentReview && (
              <div className="context-display">
                <strong>Context:</strong>
                <p>Author: {currentReview.author}, Rating: {currentReview.stars} stars, Date: {currentReview.date}</p>
                <p>Source: {currentReview.url}</p>
              </div>
            )}
          </div>

          <button onClick={handleGenerateReply} disabled={loading || !currentReview}>
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
              <button onClick={handleCopy} className="secondary-button">
                {isCopied ? '복사 완료!' : '답변 복사하기'}
              </button>
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
