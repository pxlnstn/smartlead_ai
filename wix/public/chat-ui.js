export function createChatController({
  input,
  sendButton,
  messagesText,
  statusText,
  sendChatMessage,
}) {
  let history = [];
  let transcript = [];
  let busy = false;

  function render() {
    messagesText.text = transcript
      .map(({ speaker, text }) => `${speaker}: ${text}`)
      .join('\n\n');
  }

  async function send() {
    const message = String(input.value || '').trim();
    if (!message || busy) return;

    busy = true;
    sendButton.disable();
    statusText.text = 'ino düşünüyor…';
    transcript.push({ speaker: 'Sen', text: message });
    input.value = '';
    render();

    try {
      const result = await sendChatMessage(message, history);
      transcript.push({ speaker: 'ino', text: result.response });
      history = [
        ...history,
        { role: 'user', content: message },
        { role: 'assistant', content: result.response },
      ].slice(-20);
      statusText.text = '';
    } catch (_error) {
      transcript.push({
        speaker: 'ino',
        text: 'Şu anda yanıt veremiyorum. Lütfen kısa süre sonra yeniden dene.',
      });
      statusText.text = 'Bağlantı kurulamadı.';
    } finally {
      busy = false;
      sendButton.enable();
      render();
    }
  }

  return { send };
}
