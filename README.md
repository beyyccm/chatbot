🎓 OBS Akıllı Chatbot & Dashboard Sistemi
Bu proje, Atatürk Üniversitesi Öğrenci Bilgi Sistemi (OBS) arayüzünü modern bir Dashboard ve yapay zeka destekli bir Chatbot ile birleştiren tam kapsamlı bir web uygulamasıdır. Öğrenciler notlarını, sınavlarını ve programlarını hem görsel bir panel üzerinden takip edebilir hem de asistan ile konuşarak sorgulayabilirler.

🚀 Proje Genel Bakış
Uygulama, öğrenci odaklı bir kullanıcı deneyimi sunmak amacıyla iki ana bölüme ayrılmıştır:


Giriş Paneli: Kurumsal kimliğe uygun, güvenli giriş ekranı.



Öğrenci Dashboard: Kişisel bilgiler, duyurular, sınavlar ve notların yer aldığı dinamik yönetim alanı.



Akıllı Asistan: Kullanıcının doğal dildeki sorularını (örn: "Hangi bölümdeyim?", "Notlarım nasıl?") cevaplayan entegre chatbot.



🛠️ Teknik Mimari ve Çalışma Adımları
1. Backend (Sunucu Tarafı)

Framework: Python tabanlı FastAPI ile yüksek performanslı asenkron API yapısı.


Veritabanı: SQLite kullanılarak ilişkisel bir şema oluşturulmuştur (students, instructors, courses, enrollments).




Mantıksal İşlem: chatbot_logic.py dosyası, gelen mesajları analiz ederek veritabanından doğru bilgiyi çeker ve AGNO (ortalama) gibi hesaplamaları anlık yapar.


2. Frontend (Arayüz Tarafı)
HTML5 & CSS3: Responsive (mobil uyumlu) tasarım. Kurumsal kırmızı ve gece mavisi paleti ile profesyonel görünüm.



Vanilla JavaScript: Hiçbir ağır kütüphane kullanmadan, asenkron fetch istekleri ile backend ile haberleşen dinamik yapı.




State Management: Kullanıcı oturum verileri (ID, isim, bölüm vb.) tarayıcının localStorage alanında güvenli bir şekilde yönetilir.


3. Çalışma Adımları (İş Akışı)
Kullanıcı öğrenci numarası ve şifresiyle giriş yapar.



Backend kimlik doğrulamasını yapar ve öğrenciye ait AGNO, dersler gibi bilgileri döner.

Başarılı girişte script.js dashboard ekranını render eder ve asistanı aktifleşir.



Kullanıcı chat alanına mesaj yazdığında, asistan veritabanındaki güncel verileri (vize/final notu, sınav tarihi vb.) anında yanıtlar.
📁 Proje Dosya Yapısı

├── main.py              # API uç noktaları (Login & Chat)
├── database.py          # Veritabanı şeması ve örnek veri (Seed)
├── chatbot_logic.py     # Karar mekanizması ve NLP mantığı
├── requirements.txt     # Gerekli Python paketleri
├── static/              # Frontend kaynakları
│   ├── index.html       # Ana iskelet ve Dashboard yapısı
│   ├── style.css        # Responsive tasarım ve animasyonlar
│   └── script.js        # API entegrasyonu ve UI kontrolleri
└── tests/               # Otomatik test scriptleri
👥 Ekip ve Rol Dağılımı
Backend Developer: API tasarımı, veritabanı yönetimi ve chatbot algoritmasının geliştirilmesi.

Frontend Developer: Dashboard arayüz tasarımı, CSS animasyonları ve JavaScript asenkron veri yönetimi.

QA & Test: Login senaryoları, niyet (intent) testleri ve veritabanı doğrulama işlemleri.

⚙️ Kurulum ve Çalıştırma
Bağımlılıkları yükleyin: pip install -r requirements.txt.

Uygulamayı başlatın: ./run_app.sh veya python3 main.py.

Tarayıcıdan erişin: http://localhost:8000.

Not: Bu proje eğitim amaçlı geliştirilmiş bir OBS simülasyonudur. Veritabanı ilk çalıştırmada otomatik olarak örnek verilerle oluşturulur.Dört kişilik bir ekip çalışmasıdır.
