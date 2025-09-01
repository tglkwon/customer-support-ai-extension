// background.js

// 확장 프로그램 설치 시 컨텍스트 메뉴 생성
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "generate-reply-with-ai",
    title: "AI로 답변 생성하기 (사이드 패널로 전송)",
    contexts: ["selection"]
  });
});

// 툴바 아이콘 클릭 시 사이드 패널 열기
chrome.action.onClicked.addListener((tab) => {
  chrome.sidePanel.open({ windowId: tab.windowId });
});

// 컨텍스트 메뉴 클릭 리스너
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "generate-reply-with-ai") {
    // 스크랩된 데이터와 동일한 형식으로 단일 리뷰 객체를 배열에 담아 저장
    const singleReview = {
      text: info.selectionText,
      url: info.pageUrl,
      author: 'N/A (직접 선택)',
      stars: 0,
      date: new Date().toISOString(),
    };
    
    chrome.storage.local.set({ reviews: [singleReview], currentIndex: 0 }, () => {
      chrome.sidePanel.open({ windowId: tab.windowId });
      chrome.runtime.sendMessage({ type: 'REVIEWS_UPDATED' });
    });
  }
});

// 모든 메시지를 처리하는 중앙 리스너
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // 1. 사이드 패널 -> content.js 로 스크랩 요청 전달
  if (message.type === 'INITIATE_SCRAPE') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.tabs.sendMessage(tabs[0].id, { type: 'INITIATE_SCRAPE' });
      }
    });
  }
  
  // 2. content.js -> background.js 로 스크랩 결과 전달
  else if (message.type === 'SCRAPED_REVIEWS' && message.data) {
    // 리뷰 배열 전체와 현재 인덱스를 저장
    chrome.storage.local.set({ reviews: message.data, currentIndex: 0 }, () => {
      console.log(`${message.data.length}개의 리뷰가 저장되었습니다.`);
      // 사이드 패널에 데이터가 업데이트되었음을 알림
      chrome.runtime.sendMessage({ type: 'REVIEWS_UPDATED' });
    });
  }

  // 3. content.js -> background.js 로 스크랩 실패 전달
  else if (message.type === 'SCRAPE_FAILED') {
    // 사이드 패널에 실패를 알림
    chrome.runtime.sendMessage({ type: 'SHOW_SCRAPE_FAILED_ERROR' });
  }
});