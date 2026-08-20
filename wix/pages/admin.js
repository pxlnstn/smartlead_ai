import { getLeads } from 'backend/ino-api.web';

$w.onReady(async () => {
  const status = $w('#adminStatusText');
  status.text = 'Lead kayıtları yükleniyor…';

  try {
    const { leads } = await getLeads();
    const rows = leads.map((lead) => ({
      _id: String(lead.id),
      ...lead,
      displayDate: new Date(lead.created_at).toLocaleString('tr-TR'),
    }));

    $w('#leadsRepeater').onItemReady(($item, row) => {
      $item('#leadNameText').text = row.name;
      $item('#leadPhoneText').text = row.phone_number;
      $item('#leadNoteText').text = row.note || '—';
      $item('#leadDateText').text = row.displayDate;
    });
    $w('#leadsRepeater').data = rows;
    status.text = rows.length ? `${rows.length} lead görüntüleniyor.` : 'Henüz lead yok.';
  } catch (_error) {
    status.text = 'Bu sayfayı görüntülemek için site yöneticisi olarak giriş yapmalısın.';
  }
});
