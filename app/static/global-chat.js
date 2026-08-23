(function () {
  'use strict';

  if (document.getElementById('inoGlobalChat')) return;

  var STORAGE_KEY = 'ino-global-chat-history-v1';
  var history = loadHistory();
  var busy = false;
  var pendingTimer = null;

  var root = document.createElement('div');
  root.id = 'inoGlobalChat';
  root.className = 'ino-global-chat';
  root.innerHTML = [
    '<section class="ino-global-chat__window" aria-label="ino stil asistani">',
      '<header class="ino-global-chat__header">',
        '<div class="ino-global-chat__avatar">ino</div>',
        '<div><div class="ino-global-chat__title">ino Asistan</div>',
        '<div class="ino-global-chat__subtitle">Stil hakk&#305;nda soru sor</div></div>',
      '</header>',
      '<div class="ino-global-chat__messages" id="inoGlobalChatMessages"></div>',
      '<div class="ino-global-chat__input-row">',
        '<input class="ino-global-chat__input" id="inoGlobalChatInput" type="text" placeholder="Mesaj&#305;n&#305; yaz..." autocomplete="off">',
        '<button class="ino-global-chat__send" id="inoGlobalChatSend" type="button" aria-label="G&#246;nder">',
          '<svg viewBox="0 0 24 24"><path d="M2.01 21 23 12 2.01 3 2 10l15 2-15 2z"/></svg>',
        '</button>',
      '</div>',
    '</section>',
    '<button class="ino-global-chat__toggle" id="inoGlobalChatToggle" type="button" aria-label="Chatbotu ac veya kapat">',
      '<svg class="ino-icon-chat" viewBox="0 0 24 24"><path d="M20 2H4a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2zm0 14H6l-2 2V4h16v12z"/></svg>',
      '<svg class="ino-icon-close" viewBox="0 0 24 24"><path d="m19 6.41-1.41-1.42L12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>',
    '</button>'
  ].join('');
  document.body.appendChild(root);

  var toggle = document.getElementById('inoGlobalChatToggle');
  var input = document.getElementById('inoGlobalChatInput');
  var sendButton = document.getElementById('inoGlobalChatSend');
  var messages = document.getElementById('inoGlobalChatMessages');

  renderHistory();

  toggle.addEventListener('click', function () {
    root.classList.toggle('is-open');
    if (root.classList.contains('is-open')) input.focus();
  });

  sendButton.addEventListener('click', sendMessage);
  input.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') sendMessage();
  });

  window.addEventListener('message', function (event) {
    var data = event.data;
    if (!data || data.type !== 'INO_CHAT_RESPONSE' || !busy) return;

    clearTimeout(pendingTimer);
    busy = false;
    sendButton.disabled = false;
    removeTyping();

    if (data.error) {
      addMessage('assistant', '\u00dczg\u00fcn\u00fcm, \u015fu anda yan\u0131t veremiyorum. L\u00fctfen tekrar dene.');
    } else {
      addMessage('assistant', String(data.reply || data.response || ''));
    }
    input.focus();
  });

  function sendMessage() {
    var message = input.value.trim();
    if (!message || busy) return;

    addMessage('user', message);
    input.value = '';
    busy = true;
    sendButton.disabled = true;
    addTyping();

    window.parent.postMessage({
      type: 'INO_CHAT_REQUEST',
      message: message,
      history: history.slice(-20)
    }, '*');

    pendingTimer = setTimeout(function () {
      if (!busy) return;
      busy = false;
      sendButton.disabled = false;
      removeTyping();
      addMessage('assistant', 'Yan\u0131t s\u00fcresi doldu. L\u00fctfen tekrar dene.');
    }, 25000);
  }

  function addMessage(role, content) {
    history.push({ role: role, content: content });
    history = history.slice(-20);
    saveHistory();
    appendBubble(role, content);
  }

  function appendBubble(role, content) {
    var bubble = document.createElement('div');
    bubble.className = 'ino-global-chat__message ino-global-chat__message--' + (role === 'user' ? 'user' : 'bot');
    bubble.textContent = content;
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
  }

  function renderHistory() {
    if (!history.length) {
      appendBubble('assistant', 'Merhaba! Ben ino, ki\u015fisel stil asistan\u0131n. Sana nas\u0131l yard\u0131mc\u0131 olabilirim?');
      return;
    }
    history.forEach(function (item) { appendBubble(item.role, item.content); });
  }

  function addTyping() {
    removeTyping();
    var typing = document.createElement('div');
    typing.id = 'inoGlobalChatTyping';
    typing.className = 'ino-global-chat__typing is-visible';
    typing.textContent = 'ino d\u00fc\u015f\u00fcn\u00fcyor...';
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;
  }

  function removeTyping() {
    var typing = document.getElementById('inoGlobalChatTyping');
    if (typing) typing.remove();
  }

  function loadHistory() {
    try {
      var parsed = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '[]');
      return Array.isArray(parsed) ? parsed.slice(-20) : [];
    } catch (_error) {
      return [];
    }
  }

  function saveHistory() {
    try { sessionStorage.setItem(STORAGE_KEY, JSON.stringify(history)); } catch (_error) {}
  }
})();
