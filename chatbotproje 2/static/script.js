// API BASE URL
// Backend (sunucu) tarafında tanımlanmış olan tüm endpoint'lerin ortak başlangıç adresidir.
// Bu yapı sayesinde endpoint adresleri tek merkezden yönetilir ve ileride değişiklik yapılması kolaylaşır.
const API_URL = "/api";

// Giriş yapmış olan öğrencinin ID bilgisini tutan global değişken
// Chatbot ve diğer API çağrılarında kimlik doğrulama amacıyla kullanılır
let currentStudentId = null;

// ==========================
// DOM ELEMENT SEÇİMLERİ
// ==========================

// Chatbot widget'ının en dış kapsayıcısı
// Kullanıcı giriş yaptıktan sonra görünür hale getirilir
const widgetChat = document.getElementById('widgetChat');

// Chatbot'un açılıp kapanmasını sağlayan ana container
const chatWidget = document.getElementById('chatWidget');

// Mesaj gönderme formu (input + submit)
const chatForm = document.getElementById('chatForm');

// Kullanıcının mesaj yazdığı input alanı
const messageInput = document.getElementById('messageInput');

// Tüm mesajların listelendiği container
const chatMessages = document.getElementById('chatMessages');

// Chat başlığında görünen asistan adı
const chatHeaderName = document.getElementById('chatHeaderName');

// ==========================
// OBS DASHBOARD ELEMENTLERİ
// ==========================

// Sol menüde görünen öğrenci adı
const sidebarName = document.getElementById('sidebarName');

// Mini profil görseli (sidebar)
const miniProfileImg = document.getElementById('miniProfileImg');

// Ana ekranda görünen öğrenci adı
const mainName = document.getElementById('mainName');

// Ana profil görseli
const mainProfileImg = document.getElementById('mainProfileImg');

// Fakülte / bölüm bilgisi
const facultyDept = document.getElementById('facultyDept');

// Öğrenci numarası
const studentNo = document.getElementById('studentNo');

// ==========================
// GLOBAL LOGIN ELEMENTLERİ
// ==========================

// Giriş ekranı container'ı
const loginPage = document.getElementById('loginPage');

// Giriş sonrası ana uygulama alanı
const appContainer = document.getElementById('appContainer');

// Global giriş formu
const globalLoginForm = document.getElementById('globalLoginForm');

// ==========================
// INITIALIZE (SAYFA YÜKLENDİĞİNDE)
// ==========================

document.addEventListener('DOMContentLoaded', () => {
    // Sunum ve geliştirme aşamasında her yenilemede temiz bir başlangıç yapmak için
    // Tarayıcıda daha önce saklanmış tüm oturum verileri silinir
    localStorage.removeItem('student_id');
    localStorage.removeItem('student_name');
    localStorage.removeItem('student_grade');
    localStorage.removeItem('student_dept');
    localStorage.removeItem('student_agno');

    // Sayfa ilk açıldığında kullanıcıya her zaman giriş ekranı gösterilir
    showGlobalLogin();
});

// ==========================
// CHATBOT GÖRÜNÜRLÜK KONTROLÜ
// ==========================

function toggleChat() {
    // CSS üzerinden open class'ını ekleyip çıkararak chatbot'u açıp kapatır
    chatWidget.classList.toggle('open');
}

// ==========================
// GLOBAL LOGIN İŞLEMİ
// ==========================

globalLoginForm.addEventListener('submit', async (e) => {
    // Formun varsayılan submit davranışı engellenir (sayfa yenilenmez)
    e.preventDefault();

    // Kullanıcının girdiği öğrenci numarası alınır
    const id = document.getElementById('globalStudentId').value.trim();

    // Kullanıcının girdiği şifre alınır
    const password = document.getElementById('globalPassword').value.trim();

    // Submit butonuna erişilir (yükleniyor durumu için)
    const btn = globalLoginForm.querySelector('button[type="submit"]');

    try {
        // Kullanıcının tekrar tekrar tıklamasını engellemek için buton pasif yapılır
        btn.disabled = true;

        // Kullanıcıya görsel geri bildirim sağlanır
        btn.innerHTML = '<span>Lütfen bekleyiniz...</span> <i class="fas fa-spinner fa-spin"></i>';

        // Backend tarafındaki login endpoint'ine POST isteği gönderilir
        const res = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_id: id, password: password })
        });

        // HTTP hata kodu dönerse özel hata fırlatılır
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.detail || 'Giriş başarısız');
        }

        // Başarılı yanıt JSON formatında alınır
        const data = await res.json();

        // ==========================
        // BÖLÜM HESAPLAMA (SİMÜLASYON)
        // ==========================

        // Gerçek sistemde DB'den gelecek olan bölüm bilgisi
        // Sunum amacıyla burada basit bir simülasyon yapılmıştır
        let dept = "Mühendislik Fakültesi Bilgisayar Mühendisliği Programı";
        if (data.name.includes("Zeynep")) dept = "Tıp Fakültesi Tıp Programı";
        if (data.name.includes("Ali")) dept = "Hukuk Fakültesi Hukuk Programı";
        if (data.name.includes("Mehmet")) dept = "Mimarlık ve Tasarım Fakültesi Mimarlık Programı";

        // ==========================
        // OTURUM VERİLERİNİ SAKLAMA
        // ==========================

        // Kullanıcı bilgileri localStorage'a kaydedilir
        localStorage.setItem('student_grade', data.grade_level);
        localStorage.setItem('student_id', data.student_id);
        localStorage.setItem('student_name', data.name);
        localStorage.setItem('student_dept', dept);
        localStorage.setItem('student_agno', data.agno);

        // Giriş başarılı olduğu için dashboard ekranına geçilir
        showDashboard();

        // Kullanıcı bilgileri arayüze yazdırılır
        loginSuccess(data.student_id, data.name, data.grade_level, dept, data.agno);

    } catch (err) {
        // Giriş sırasında oluşan tüm hatalar kullanıcıya gösterilir
        alert(`Giriş Hatası: ${err.message}`);
    } finally {
        // İşlem sonucu ne olursa olsun buton eski haline getirilir
        btn.disabled = false;
        btn.innerHTML = '<span>Giriş</span> <i class="fas fa-arrow-right"></i>';
    }
});

// ==========================
// GİRİŞ BAŞARILI OLDUKTAN SONRA
// ==========================

function loginSuccess(id, name, grade, dept, agno) {
    // Global öğrenci ID atanır
    currentStudentId = id;

    // Sidebar ve ana ekrandaki isim alanları güncellenir
    if (sidebarName) sidebarName.textContent = name;
    if (mainName) mainName.innerHTML = `${name} <i class="fas fa-circle text-success" style="font-size: 10px; vertical-align: middle; color: #48bb78;"></i>`;

    // Öğrenci numarası yazdırılır
    if (studentNo) studentNo.textContent = id;

    // Fakülte ve bölüm bilgisi yazdırılır
    if (facultyDept) facultyDept.textContent = dept || "Mühendislik Fakültesi Bilgisayar Mühendisliği Programı";

    // Öğrencinin sınıf bilgisi güncellenir
    const gradeSpan = document.getElementById('studentGrade');
    if (gradeSpan && grade) gradeSpan.textContent = `${grade}.Sınıf`;

    // Kullanıcının adına göre otomatik avatar oluşturulur
    const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=0D8ABC&color=fff&size=128`;

    // Profil görselleri güncellenir
    if (miniProfileImg) miniProfileImg.src = avatarUrl;
    if (mainProfileImg) mainProfileImg.src = avatarUrl;

    // Giriş yapan kullanıcıya chatbot erişimi açılır
    widgetChat.style.display = 'flex';

    // Chat başlığında asistan adı gösterilir
    if (chatHeaderName) chatHeaderName.textContent = "Asistan";
}

// ==========================
// EKRAN GEÇİŞ FONKSİYONLARI
// ==========================

function showGlobalLogin() {
    loginPage.style.display = 'flex';
    appContainer.style.display = 'none';
}

function showDashboard() {
    loginPage.style.display = 'none';
    appContainer.style.display = 'flex';
}

// ==========================
// ÇIKIŞ İŞLEMİ
// ==========================

function logout() {
    // Tüm oturum verileri temizlenir
    localStorage.clear();

    // Sayfa yeniden yüklenir
    location.reload();
}

// ==========================
// CHATBOT MANTĞI
// ==========================

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // Kullanıcının yazdığı mesaj alınır
    const msg = messageInput.value.trim();

    // Boş mesaj gönderilmesi engellenir
    if (!msg) return;

    // Kullanıcı mesajı hemen ekrana basılır
    addMessage(msg, 'user');

    // Input alanı temizlenir
    messageInput.value = '';

    // Mesaj backend'e gönderilir
    fetchReply(msg);
});

function sendQuickMessage(msg) {
    addMessage(msg, 'user');
    fetchReply(msg);
}

function addMessage(text, sender) {
    // Yeni mesaj için div oluşturulur
    const div = document.createElement('div');

    // Mesaj tipi (user / bot) class olarak atanır
    div.classList.add('message', `${sender}-message`);

    // Mesajın gönderildiği saat hesaplanır
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Mesaj içeriği HTML olarak eklenir
    div.innerHTML = `
        <div class="message-content">${text}</div>
        <div class="message-time">${time}</div>
    `;

    // Mesaj listeye eklenir
    chatMessages.appendChild(div);

    // Otomatik kaydırma yapılır
    scrollToBottom();
}

async function fetchReply(message) {
    try {
        // Chatbot API endpoint'ine mesaj gönderilir
        const res = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_id: currentStudentId, message: message })
        });

        // Sunucu hata dönerse yakalanır
        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`Sunucu Hatası (${res.status}): ${errorText}`);
        }

        // Bot cevabı alınır
        const data = await res.json();

        // Bot mesajı ekrana basılır
        addMessage(data.response, 'bot');

    } catch (err) {
        // Chat sırasında oluşan hatalar konsola yazılır
        console.error("Chat Error:", err);

        // Kullanıcıya hata mesajı gösterilir
        addMessage(`Bir hata oluştu: ${err.message || "Bağlantı hatası"}`, 'bot');
    }
}

function scrollToBottom() {
    // Mesaj alanı her yeni mesajda en alta kaydırılır
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
