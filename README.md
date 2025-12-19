# 🎓 OBS Akıllı Chatbot & Dashboard Sistemi

Bu proje, **Atatürk Üniversitesi Öğrenci Bilgi Sistemi (OBS)** arayüzünü modern bir **Dashboard** ve **yapay zekâ destekli Chatbot** ile birleştiren tam kapsamlı bir web uygulamasıdır. Öğrenciler; notlarını, sınavlarını ve ders programlarını hem görsel bir panel üzerinden takip edebilir hem de doğal dil kullanarak akıllı asistana soru sorabilir.

> **Not:** Proje eğitim amaçlı bir OBS simülasyonudur.

---

## 🚀 Proje Genel Bakış

Uygulama, öğrenci odaklı bir kullanıcı deneyimi sunmak amacıyla üç ana bileşenden oluşur:

### 🔐 Giriş Paneli

* Kurumsal kimliğe uygun, sade ve güvenli tasarım
* Öğrenci numarası ve şifre ile kimlik doğrulama

### 📊 Öğrenci Dashboard

* Kişisel bilgiler
* Duyurular
* Dersler, sınavlar ve notlar
* Dinamik ve responsive (mobil uyumlu) arayüz

### 🤖 Akıllı Asistan (Chatbot)

* Doğal dilde soruları anlama (örn: *“Hangi bölümdeyim?”*, *“AGNO kaç?”*)
* Veritabanından anlık veri çekme
* Not ortalaması (AGNO) gibi hesaplamaları gerçek zamanlı yapma

---

## 🛠️ Teknik Mimari

### Backend (Sunucu Tarafı)

* **Programlama Dili:** Python 3.x
* **Framework:** FastAPI (asenkron, yüksek performanslı API)
* **Veritabanı:** SQLite
* **ORM / Veri Erişimi:** Basit ve ilişkisel yapı

#### Veritabanı Şeması

* `students`
* `instructors`
* `courses`
* `enrollments`

#### İş Mantığı

* `chatbot_logic.py` dosyası:

  * Kullanıcı mesajını analiz eder
  * Niyet (intent) belirler
  * Veritabanından uygun bilgiyi çeker
  * AGNO ve benzeri hesaplamaları yapar

---

### Frontend (İstemci Tarafı)

* **HTML5:** Sayfa iskeleti ve semantik yapı
* **CSS3:** Responsive tasarım, animasyonlar ve kurumsal renk paleti

  * Kurumsal kırmızı
  * Gece mavisi
* **JavaScript (Vanilla JS):**

  * `fetch` API ile backend haberleşmesi
  * Dinamik içerik render işlemleri

#### State Management

* Kullanıcıya ait oturum verileri (`id`, `isim`, `bölüm` vb.)
* Tarayıcı **localStorage** alanında yönetilir

---

## 🔄 Uygulama İş Akışı

1. Kullanıcı, öğrenci numarası ve şifresiyle giriş yapar.
2. Backend, kimlik doğrulamasını gerçekleştirir.
3. Öğrenciye ait bilgiler (dersler, notlar, AGNO vb.) döndürülür.
4. Dashboard ekranı render edilir.
5. Chatbot aktifleşir.
6. Kullanıcı chat alanına mesaj gönderir.
7. Asistan, veritabanındaki güncel bilgileri kullanarak anında yanıt üretir.

---

## 📁 Proje Dosya Yapısı

```text
OBS-Chatbot-Dashboard/
│
├── main.py                # API uç noktaları (Login & Chat)
├── database.py            # Veritabanı şeması ve örnek veri (Seed)
├── chatbot_logic.py       # Chatbot karar mekanizması ve NLP mantığı
├── requirements.txt       # Gerekli Python paketleri
│
├── static/                # Frontend kaynakları
│   ├── index.html         # Dashboard ve arayüz iskeleti
│   ├── style.css          # Responsive tasarım ve animasyonlar
│   └── script.js          # API entegrasyonu ve UI kontrolleri
│
├── tests/                 # Otomatik test scriptleri
└── README.md              # Proje dokümantasyonu
```

---

## 👥 Ekip ve Rol Dağılımı

Bu proje **4 kişilik bir ekip** tarafından geliştirilmiştir:

* **Backend Developer**

  * API tasarımı
  * Veritabanı yönetimi
  * Chatbot algoritması ve iş mantığı

* **Frontend Developer**

  * Dashboard arayüz tasarımı
  * CSS animasyonları
  * JavaScript asenkron veri yönetimi

* **QA & Test**

  * Login senaryoları
  * Chatbot niyet (intent) testleri
  * Veritabanı doğrulama işlemleri

---

## ⚙️ Kurulum ve Çalıştırma

### 1️⃣ Depoyu Klonlayın

```bash
git clone https://github.com/kullanici-adi/obs-chatbot-dashboard.git
cd obs-chatbot-dashboard
```

### 2️⃣ Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 3️⃣ Uygulamayı Başlatın

```bash
python main.py
```

veya

```bash
./run_app.sh
```

### 4️⃣ Tarayıcıdan Erişin

```text
http://localhost:8000
```

---

## ℹ️ Ek Bilgiler

* Veritabanı, ilk çalıştırmada **otomatik olarak örnek verilerle** oluşturulur.
* Proje, gerçek OBS sistemlerini temsil etmez.
* Tamamen **eğitim ve akademik amaçlıdır**.

---

## 📌 Lisans

Bu proje eğitim amaçlıdır. Dört kişilik bir ekip ile yapılmıştır.İlgili üniversite ve kurumlarla resmi bir bağlantısı yoktur.

---

**Geri bildirimleriniz ve katkılarınız memnuniyetle karşılanır.**
