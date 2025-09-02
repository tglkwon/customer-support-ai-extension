/* global chrome */

// 참고: 이 스크립트는 사용자가 제공한 CSS 선택자를 기반으로 하며,
// Gmail의 웹사이트 구조가 변경되면 작동하지 않을 수 있습니다.

/**
 * 페이지에서 현재 열린 이메일 정보를 스크래핑하는 메인 함수
 */
function scrapeGmail() {
  console.log("Gmail Scraper: 스크래핑 시작...");

  // 사용자가 제공한 선택자를 기반으로 요소 검색
  // Gmail의 동적인 클래스 이름 대신, 비교적 안정적인 속성이나 구조를 활용
  const subjectEl = document.querySelector('h2.hP');
  const senderEl = document.querySelector('span[email]'); // 더 일반적인 선택자 사용
  const dateEl = document.querySelector('span.g3[title]');
  const bodyEl = document.querySelector('div[dir="auto"]');

  if (!subjectEl || !senderEl || !dateEl || !bodyEl) {
    console.error("Gmail Scraper: 필수 요소를 찾지 못했습니다. CSS 선택자가 변경되었을 수 있습니다.", {
        subjectEl, senderEl, dateEl, bodyEl
    });
    chrome.runtime.sendMessage({ type: 'SHOW_SCRAPE_FAILED_ERROR' });
    return;
  }

  const subject = subjectEl.innerText;
  const author = senderEl.getAttribute('name') || senderEl.getAttribute('email') || 'N/A';
  const date = dateEl.getAttribute('title') || 'N/A';
  const body = bodyEl.innerText;

  // 제목과 본문을 합쳐서 리뷰 텍스트로 구성
  const fullText = `${subject}\n\n${body}`;

  const scrapedData = [{
    author,
    date,
    stars: 0, // 이메일에는 별점이 없으므로 0으로 고정
    text: fullText,
    url: window.location.href
  }];

  console.log("Gmail Scraper: 스크래핑 완료된 데이터:", scrapedData);
  chrome.runtime.sendMessage({ type: 'SCRAPED_REVIEWS', data: scrapedData });
}

// 백그라운드 스크립트 또는 팝업으로부터 메시지를 수신 대기
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'INITIATE_SCRAPE') {
    // Gmail은 페이지 로드 후 내용이 동적으로 표시되므로, 약간의 지연 후 스크래핑 시도
    setTimeout(scrapeGmail, 500);
    return true; // 비동기 응답을 위해 true 반환
  }
});
