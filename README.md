# 💼 Flask Wallet API & Management Dashboard

Bu proje, **Flask** ve **Vanilla JavaScript** kullanılarak geliştirilmiş minimalist bir **Dijital Cüzdan Yönetim Sistemi** API'si ve yönetim panelidir.  
Projenin amacı; finansal teknolojilerdeki (Fintech) temel bakiye, para yükleme ve transfer mantığını simüle etmek; aynı zamanda temiz kod mimarisi, uç nokta (endpoint) doğrulama süreçleri ve dökümantasyon disiplinini göstermektir.

---

## 🚀 Öne Çıkan Özellikler ve Validasyonlar

Proje sadece temel CRUD işlemlerini değil, finansal uygulamalarda kritik olan iş mantığı doğrulama (Business Logic Validation) kurallarını da içerir:
- **Güvenli Cüzdan Oluşturma:** İsim kontrolü (en az 2 karakter) doğrulaması.
- **Tip ve Pozitif Sayı Kontrolü:** Para yükleme ve transfer işlemlerinde gelen miktarın `int` veya `float` olup olmadığı ve sıfırdan büyük olma şartı backend seviyesinde (`isinstance`) denetlenir.
- **Hassas Hesaplama (`round`):** Floating-point (ondalık sayı) aritmetik hatalarının önüne geçmek için tüm bakiye işlemleri `round(value, 2)` ile iki basamağa yuvarlanır.
- **Atomik Transfer Kontrolü:** Gönderen ve alıcının varlığı, yetersiz bakiye durumu ve kullanıcının *kendisine transfer yapma hatası* engellenmiştir.
- **Kronolojik Loglama:** Tüm başarılı yükleme ve transfer hareketleri anlık olarak ters kronolojik sırayla listelenir.

---

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Python 3.x, Flask (Modüler ve hafif RESTful mimari)
* **Frontend:** HTML5, Tailwind CSS (v4 - Standalone tarayıcı derleyicisi), Vanilla JavaScript (Async/Await & Fetch API)
* **Veri Yönetimi:** Bellek içi (In-Memory) veri yapıları (`dict` ve `list`) ile yüksek hızlı veri işleme.
  > 🧠 *Mimari Not: Projenin bu aşamasında, sıfır konfigürasyonla (Zero-Setup) hemen çalıştırılabilmesi ve hızlı prototipleme adına veri modeli bellek üzerinde kurgulanmıştır. İş mantığı katmanı, veritabanı bağımsız çalışacak şekilde izole edilmiştir.*

---

## 📂 Proje Yapısı

```text
├── main.py              # Flask backend sunucusu, validasyonlar ve API uç noktaları
├── templates/
│   └── index.html       # Tailwind CSS ve asenkron JS entegrasyonlu yönetim paneli
└── README.md            # Proje dökümantasyonu

---

## 🚀 Kurulum ve Çalıştırma

Proje, herhangi bir harici veritabanı veya Docker konfigürasyonu gerektirmediği için "Zero-Setup" mantığıyla doğrudan çalışmaya hazırdır.
* **Projeyi Klonlayın:** git clone [https://github.com/kullaniciadi/flask-wallet-api.git](https://github.com/kullaniciadi/flask-wallet-api.git)
cd flask-wallet-api

* **Sanal Ortam Oluşturun & Bağımlılıkları Yükleyin (Önerilen):** # Sanal ortam oluşturma
python -m venv venv
source venv/bin/activate  # Linux/Mac için
# venv\Scripts\activate  # Windows için

# Flask yüklemesi
pip install flask

* **Uygulamayı Başlatın:** python main.py.
---
