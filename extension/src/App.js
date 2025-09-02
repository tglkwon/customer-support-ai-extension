import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

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

  const fetchAndSetReviewsFromStorage = () => {
    /* global chrome */
    if (!window.chrome || !window.chrome.storage) return;

    chrome.storage.local.get(['reviews', 'currentIndex'], (result) => {
      if (result.reviews && result.reviews.length > 0) {
        setReviews(result.reviews);
        setCurrentIndex(result.currentIndex || 0);
        setError(''); // 이전 에러 메시지 초기화
      } else {
        // 스토리지에 리뷰가 없는 경우, 초기 상태로 유지
        setReviews([]);
        setCurrentIndex(0);
      }
    });
  };

  useEffect(() => {
    fetchAndSetReviewsFromStorage();

    const messageListener = (message, sender, sendResponse) => {
      if (message.type === 'REVIEWS_UPDATED') {
        fetchAndSetReviewsFromStorage();
      } else if (message.type === 'SHOW_SCRAPE_FAILED_ERROR') {
        setError('리뷰를 찾을 수 없습니다. 페이지의 CSS 선택자를 확인해주세요.');
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

  useEffect(() => {
    if (!currentReview) {
      setFullPrompt('');
      return;
    }
    const promptText = `Author: ${currentReview.author}\nPackage Name: ${currentReview.url || 'N/A'}\nReview Submit Date and Time: ${currentReview.date}\nStar Rating: ${currentReview.stars}\nReview Text: ${currentReview.text}`;
    setFullPrompt(promptText);
  }, [currentReview]);


  // --- Event Handlers --- //

  const handleInitiateScrape = () => {
    setError('');
    setReviews([]);
    setReply('');
    setCurrentIndex(0);
    setLoading(true);
    
    if (!window.chrome || !window.chrome.tabs) {
        setError("Chrome API를 사용할 수 없습니다.");
        setLoading(false);
        return;
    }

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (!tabs[0] || !tabs[0].url) {
        setError("현재 탭의 URL을 가져올 수 없습니다.");
        setLoading(false);
        return;
      }
      const currentUrl = tabs[0].url;

      if (currentUrl.includes('play.google.com/console') || currentUrl.includes('appstoreconnect.apple.com') || currentUrl.includes('mail.google.com')) {
        chrome.runtime.sendMessage({ type: 'INITIATE_SCRAPE' });
      } else {
        setError('현재 페이지는 지원되지 않습니다. Google Play Console, App Store Connect 또는 Gmail에서 실행해주세요.');
      }
      // 로딩 상태는 메시지 수신 시 해제됨 (성공 또는 실패)
      // 타임아웃 추가
      setTimeout(() => {
          if(loading) {
              setLoading(false);
              setError("리뷰 추출 시간이 초과되었습니다. 페이지를 새로고침하고 다시 시도해주세요.");
          }
      }, 10000); // 10초 타임아웃
    });
  };

  // 로딩 상태는 리뷰가 업데이트되거나 에러가 발생하면 해제되어야 함
  useEffect(() => {
      if (reviews.length > 0 || error) {
          setLoading(false);
      }
  }, [reviews, error]);

  const handleNavigate = (direction) => {
    const newIndex = currentIndex + direction;
    if (newIndex >= 0 && newIndex < reviews.length) {
      setCurrentIndex(newIndex);
      if (window.chrome && window.chrome.storage) {
          chrome.storage.local.set({ currentIndex: newIndex });
      }
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
             <button onClick={handleInitiateScrape} className="primary-button" disabled={loading}>
              {loading ? '추출 중...' : '현재 페이지에서 리뷰 추출'}
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
