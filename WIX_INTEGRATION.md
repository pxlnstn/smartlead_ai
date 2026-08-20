# ino - Wix Studio entegrasyon sözleşmesi

Bu klasördeki kodlar Wix Studio Code paneline taşınmak üzere hazırlanmıştır. Render API anahtarları
hiçbir zaman sayfa koduna konmaz; tüm dış istekler `backend/ino-api.web.js` üzerinden geçer.

Anahtarlar en az 32 rastgele bayttan üretilmeli ve `WIX_API_KEY` ile `ADMIN_API_KEY` için farklı
değerler kullanılmalıdır. Gerçek değerler `.env`, Git veya sayfa koduna eklenmemelidir.

## Hedef Wix sitesi

Hesapta iki Studio sitesi bulunuyor. Yayındaki `Inolab` (`22a1440e-5c29-4e1d-9e73-9f77ea3eeff1`)
20 Ağustos 2026 kontrolünde boş Wix şablonu gösteriyordu. Diğer site `My Site 1`
(`36d16b85-70b0-4718-9825-301e5e10c86a`) taslak durumda. Kod taşınmadan önce hedef site
kesinleştirilmelidir.

## Wix Secrets Manager

Üç secret oluşturun:

- `INO_API_BASE_URL`: Render servis adresi, ör. `https://...onrender.com`
- `INO_WIX_API_KEY`: Render'daki `WIX_API_KEY` ile aynı değer
- `INO_ADMIN_API_KEY`: Render'daki `ADMIN_API_KEY` ile aynı değer

`INO_ADMIN_API_KEY` yalnızca `Permissions.Admin` web metodunda okunur ve frontend'e dönmez.
`INO_WIX_API_KEY` chatbot ve form isteklerini yalnızca Wix backend üzerinden kabul ettirir.

## Dosya yerleşimi

- `wix/backend/ino-api.web.js` -> Backend / `ino-api.web.js`
- `wix/public/chat-ui.js` -> Public / `chat-ui.js`
- `wix/pages/masterPage.js` -> Master Page (tüm sayfalarda mini chatbot)
- `wix/pages/home.js` -> Demo formunun bulunduğu sayfa
- `wix/pages/chat.js` -> Tam chatbot sayfası
- `wix/pages/admin.js` -> Yalnızca yönetici lead sayfası

## Element ID sözleşmesi

| Alan | ID'ler |
|---|---|
| Ana chatbot | `chatInput`, `chatSendButton`, `chatMessagesText`, `chatStatusText` |
| Mini chatbot | `miniChatToggleButton`, `miniChatPanel`, `miniChatCloseButton`, `miniChatInput`, `miniChatSendButton`, `miniChatMessagesText`, `miniChatStatusText` |
| Demo formu | `leadNameInput`, `leadPhoneInput`, `leadNoteInput`, `leadSubmitButton`, `leadStatusText` |
| Admin | `adminStatusText`, `leadsRepeater`; repeater içinde `leadNameText`, `leadPhoneText`, `leadNoteText`, `leadDateText` |

Mini chatbot paneli ilk yüklemede daraltılır. `miniChatToggleButton` sayfanın sağ altına sabitlenmeli;
panel de butonun üzerinde sağ alta sabitlenmelidir.

Admin sayfası menüden gizlenmeli ve Wix sayfa erişimi mümkün olan en dar yönetici erişimine
ayarlanmalıdır. Veri ayrıca iki katmanda korunur: Wix web metodu `Permissions.Admin` ister ve
Render `/api/leads` çağrısı `X-Admin-Key` olmadan sonuç döndürmez.

## Render ortam değişkenleri

- `GEMINI_API_KEY`
- `GEMINI_MODEL=gemini-3.6-flash`
- `ADMIN_API_KEY` (Blueprint otomatik üretir)
- `WIX_API_KEY` (Blueprint otomatik üretir)
- `DATABASE_URL` (Blueprint içindeki `ino-postgres` bağlantısından gelir)
- `CORS_ORIGINS` (yayınlanmış Wix origin'i)
- `DEBUG=false`

Ücretsiz Render PostgreSQL prototip için uygundur ancak süreli olabilir; gerçek leadlerin kalıcı
tutulacağı canlı kullanım öncesinde ücretli/veri saklama garantili plana geçirilmelidir.
