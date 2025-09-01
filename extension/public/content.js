// content.js

// 리뷰를 스크레이핑하는 함수
function scrapeReviews() {
    // Google Play Console 페이지 구조에 맞춘 CSS 선택자
    const reviewSelector = '.review-container'; // 1. 리뷰 하나 전체를 감싸는 컨테이너
    const authorSelector = '.author-display-name'; // 2. 작성자 이름
    const dateSelector = '.last-update-time'; // 3. 리뷰 작성 날짜
    const textSelector = 'text-with-highlights[debug-id="review-body"] span'; // 4. 리뷰 본문
    const starSelector = 'div[debug-id="star-icons"]'; // 5. 별점이 표시되는 부분

    const reviews = [];
    const reviewElements = document.querySelectorAll(reviewSelector);

    reviewElements.forEach(element => {
        try {
            const author = element.querySelector(authorSelector)?.textContent.trim();
            const date = element.querySelector(dateSelector)?.textContent.trim();
            const text = element.querySelector(textSelector)?.textContent.trim();
            
            const starElement = element.querySelector(starSelector);
            const ariaLabel = starElement?.getAttribute('aria-label') || '';
            const starMatch = ariaLabel.match(/(\d+)/);
            const stars = starMatch ? parseInt(starMatch[0], 10) : 0;

            if (author && date && text) {
                reviews.push({ author, date, text, stars });
            }
        } catch (e) {
            console.error('리뷰를 파싱하는 중 오류 발생:', e);
        }
    });

    if (reviews.length > 0) {
        console.log(`${reviews.length}개의 리뷰를 찾았습니다.`, reviews);
        // 백그라운드 스크립트로 데이터 전송
        chrome.runtime.sendMessage({ type: 'SCRAPED_REVIEWS', data: reviews });
    } else {
        console.log('리뷰를 찾을 수 없습니다. CSS 선택자를 확인해주세요.');
        // 실패 메시지를 보낼 수도 있습니다.
        chrome.runtime.sendMessage({ type: 'SCRAPE_FAILED' });
    }
}

// 백그라운드 스크립트 또는 팝업으로부터 메시지를 수신 대기
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'INITIATE_SCRAPE') {
        scrapeReviews();
    }
});