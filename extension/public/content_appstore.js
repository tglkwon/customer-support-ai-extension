/* global chrome */

// 참고: 이 스크립트는 사용자가 제공한 CSS 선택자를 기반으로 하며,
// 웹사이트의 구조가 변경되면 작동하지 않을 수 있습니다.

/**
 * 작성자와 날짜가 합쳐진 문자열에서 각각을 분리합니다.
 * 예: "작성자 이름 – 2025년 9월 5일"
 * @param {string} text - 파싱할 텍스트
 * @returns {{author: string, date: string}}
 */
function parseAuthorAndDate(text) {
  if (!text) return { author: 'N/A', date: 'N/A' };
  // 긴 대시(–) 또는 짧은 대시(-)로 분리 시도
  const parts = text.split(/–|-/);
  if (parts.length >= 2) {
    const date = parts[0].trim();
    const author = parts.slice(1).join('-').trim();
    return { author, date };
  }
  return { author: text.trim(), date: 'N/A' };
}

/**
 * 별점 컨테이너 요소에서 실제 별점(숫자)을 추출합니다.
 * 여기서는 자식 요소(예: 별 아이콘)의 개수를 세는 방식을 사용합니다.
 * @param {Element} ratingContainer - 별점을 포함하는 DOM 요소
 * @returns {number}
 */
function parseRating(ratingContainer) {
  if (!ratingContainer) return 0;
  // 자식 요소의 개수로 별점을 추정합니다. (예: 꽉 찬 별 SVG 아이콘 5개)
  return ratingContainer.childElementCount;
}

/**
 * 페이지에서 리뷰를 스크래핑하는 메인 함수
 */
function scrapeAppStoreReviews() {
  console.log("App Store Scraper: 스크래핑 시작...");

  const reviewElements = document.querySelectorAll('div.idyRmo');

  if (!reviewElements || reviewElements.length === 0) {
    console.error("App Store Scraper: 리뷰 컨테이너 요소를 찾지 못했습니다. CSS 선택자가 변경되었을 수 있습니다.");
    chrome.runtime.sendMessage({ type: 'SHOW_SCRAPE_FAILED_ERROR' });
    return;
  }

  console.log(`App Store Scraper: ${reviewElements.length}개의 리뷰 요소를 찾았습니다.`);

  const scrapedData = Array.from(reviewElements).map(reviewEl => {
    const authorDateEl = reviewEl.querySelector('p.hHcFfp.XTNqW.fNybhB');
    const ratingEl = reviewEl.querySelector('div.jA-dPmr');
    const titleEl = reviewEl.querySelector('p.dZVhlA.XTNqW.fgJAH'); // 제목 요소 선택자 추가
    const textEl = reviewEl.querySelector('p.fLbpYN.XTNqW.hhdlTb');

    const authorDateText = authorDateEl ? authorDateEl.innerText : null;
    const { author, date } = parseAuthorAndDate(authorDateText);
    
    const stars = parseRating(ratingEl);
    const titleText = titleEl ? titleEl.innerText : '';
    const reviewBodyText = textEl ? textEl.innerText : '';

    // 제목과 내용을 합쳐서 하나의 텍스트로 만듭니다.
    const fullReviewText = titleText ? `${titleText}\n\n${reviewBodyText}` : reviewBodyText;

    return {
      author,
      date,
      stars,
      text: fullReviewText, // 수정된 전체 리뷰 텍스트
      url: window.location.href
    };
  });

  console.log("App Store Scraper: 스크래핑 완료된 데이터:", scrapedData);
  chrome.runtime.sendMessage({ type: 'SCRAPED_REVIEWS', data: scrapedData });
}

// 백그라운드 스크립트 또는 팝업으로부터 메시지를 수신 대기
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'INITIATE_SCRAPE') {
    scrapeAppStoreReviews();
    return true; // 비동기 응답을 위해 true 반환
  }
});