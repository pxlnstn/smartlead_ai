import { sendChatMessage } from 'backend/ino-api.web';
import { createChatController } from 'public/chat-ui';

$w.onReady(() => {
  const controller = createChatController({
    input: $w('#chatInput'),
    sendButton: $w('#chatSendButton'),
    messagesText: $w('#chatMessagesText'),
    statusText: $w('#chatStatusText'),
    sendChatMessage,
  });

  $w('#chatSendButton').onClick(controller.send);
  $w('#chatInput').onKeyPress((event) => {
    if (event.key === 'Enter') controller.send();
  });
});
