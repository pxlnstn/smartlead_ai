import { sendChatMessage } from 'backend/ino-api.web';

// Mini chatbot is an embedded HTML iframe (#miniChatHtml). We never expose the
// API key or the Render URL inside that HTML — the iframe only exchanges plain
// chat text with this page via postMessage, and this code makes the actual
// (secured) backend call on its behalf.
$w.onReady(() => {
  const panel = $w('#miniChatHtml');
  const toggleButton = $w('#miniChatToggleButton');

  panel.hide();

  toggleButton.onClick(() => {
    if (panel.hidden) panel.show();
    else panel.hide();
  });

  panel.onMessage(async (event) => {
    const data = event.data;
    if (!data || typeof data !== 'object') return;

    if (data.type === 'ino-chat-close') {
      panel.hide();
      return;
    }

    if (data.type !== 'ino-chat-send') return;

    const message = String(data.message || '').trim();
    if (!message) return;

    try {
      const result = await sendChatMessage(message, data.history || []);
      panel.postMessage({
        type: 'ino-chat-response',
        response: result.response,
        userMessage: message,
      });
    } catch (_error) {
      panel.postMessage({ type: 'ino-chat-response', error: true });
    }
  });
});
