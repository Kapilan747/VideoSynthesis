chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getSelectedText") {
      const selectedText = window.getSelection().toString().trim();
      sendResponse({ selectedText: selectedText });
    }
  });

// Listen for message from background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.videoGenerated) {
        // Show alert when video is generated
        alert('Video generated successfully!');
    }
});