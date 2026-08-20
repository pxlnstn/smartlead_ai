import { sendChatMessage } from 'backend/ino-api.web';
import { createChatController } from 'public/chat-ui';

$w.onReady(() => {
  const panel = $w('#miniChatPanel');
  panel.collapse();

  const controller = createChatController({
    input: $w('#miniChatInput'),
    sendButton: $w('#miniChatSendButton'),
    messagesText: $w('#miniChatMessagesText'),
    statusText: $w('#miniChatStatusText'),
    sendChatMessage,
  });

  $w('#miniChatToggleButton').onClick(() => {
    if (panel.collapsed) panel.expand();
    else panel.collapse();
  });
  $w('#miniChatCloseButton').onClick(() => panel.collapse());
  $w('#miniChatSendButton').onClick(controller.send);
  $w('#miniChatInput').onKeyPress((event) => {
    if (event.key === 'Enter') controller.send();
  });
});
