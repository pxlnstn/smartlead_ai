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

  function setStatus(text) {
    if (statusText) statusText.text = text;
  }

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
    setStatus('ino düşünüyor…');
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
      setStatus('');
    } catch (_error) {
      transcript.push({
        speaker: 'ino',
        text: 'Şu anda yanıt veremiyorum. Lütfen kısa süre sonra yeniden dene.',
      });
      setStatus('Bağlantı kurulamadı.');
    } finally {
      busy = false;
      sendButton.enable();
      render();
    }
  }

  return { send };
}
