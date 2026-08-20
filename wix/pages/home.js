import { submitDemoRequest } from 'backend/ino-api.web';

$w.onReady(() => {
  $w('#leadSubmitButton').onClick(submitLead);
});

async function submitLead() {
  const button = $w('#leadSubmitButton');
  const status = $w('#leadStatusText');
  const lead = {
    name: String($w('#leadNameInput').value || '').trim(),
    number: String($w('#leadPhoneInput').value || '').trim(),
    note: String($w('#leadNoteInput').value || '').trim(),
  };

  if (!lead.name || lead.number.replace(/\D/g, '').length < 7) {
    status.text = 'Lütfen adını ve geçerli bir telefon numarası gir.';
    return;
  }

  button.disable();
  status.text = 'Talebin gönderiliyor…';
  try {
    await submitDemoRequest(lead);
    status.text = 'Teşekkürler! Demo talebini aldık; yakında iletişime geçeceğiz.';
    $w('#leadNameInput').value = '';
    $w('#leadPhoneInput').value = '';
    $w('#leadNoteInput').value = '';
  } catch (_error) {
    status.text = 'Talebin gönderilemedi. Lütfen kısa süre sonra tekrar dene.';
  } finally {
    button.enable();
  }
}
