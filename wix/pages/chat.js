import { sendChatMessage } from 'backend/ino-api.web';
import { createChatController } from 'public/chat-ui';

$w.onReady(() => {
  const controller = createChatController({
    input: $w('#inputMessage'),
    sendButton: $w('#btnSend'),
    messagesText: $w('#txtResponse'),
    sendChatMessage,
  });

  $w('#btnSend').onClick(controller.send);
  $w('#inputMessage').onKeyPress((event) => {
    if (event.key === 'Enter') controller.send();
  });
});
