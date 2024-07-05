// Create a context menu item
chrome.contextMenus.create({
    id: "generateVideo",
    title: "Generate Video",
    contexts: ["selection"]
  });
  
  // Listen for context menu item clicks
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "generateVideo") {
      chrome.scripting.executeScript(
        {
          target: { tabId: tab.id },
          function: getSelectedText
        },
        (results) => {
          if (results && results[0] && results[0].result) {
            const selectedText = results[0].result;
            sendTextToServer(selectedText);
          }
        }
      );
    }
  });
  
  function getSelectedText() {
    return window.getSelection().toString().trim();
  }
  
  function sendTextToServer(text) {
    fetch("http://localhost:5000/generate-video", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ selected_text: text })
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert("Video generated successfully!");
        } else {
          alert("Failed to generate video: " + data.message);
        }
      })
      .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while generating the video.");
      });
  }
// Send a message to content script when video is generated
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.videoGenerated) {
        // Send message to content script
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            chrome.tabs.sendMessage(tabs[0].id, { videoGenerated: true });
        });
    }
});