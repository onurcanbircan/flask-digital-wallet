# 💼 Flask Wallet API & Management Dashboard

Bu proje, **Flask** ve **Vanilla JavaScript** kullanılarak geliştirilmiş minimalist bir **Dijital Cüzdan Yönetim Sistemi** API'si ve yönetim panelidir. 

Projenin amacı; finansal teknolojilerdeki (Fintech) temel bakiye, para yükleme ve transfer mantığını simüle etmek; aynı zamanda temiz kod mimarisi, uç nokta (endpoint) doğrulama süreçleri ve dökümantasyon disiplinini göstermektir.

---

## 🚀 Öne Çıkan Özellikler ve Validasyonlar

Proje sadece temel CRUD işlemlerini değil, finansal uygulamalarda kritik olan iş mantığı doğrulama (Business Logic Validation) kurallarını da içerir:

* **Güvenli Cüzdan Oluşturma:** İsim kontrolü (en az 2 karakter) doğrulaması.
* **Tip ve Pozitif Sayı Kontrolü:** Para yükleme ve transfer işlemlerinde gelen miktarın `int` veya `float` olup olmadığı ve sıfırdan büyük olma şartı backend seviyesinde (`isinstance`) denetlenir.
* **Hassas Hesaplama (`round`):** Floating-point (ondalık sayı) aritmetik hatalarının önüne geçmek için tüm bakiye işlemleri `round(value, 2)` ile iki basamağa yuvarlanır.
* **Atomik Transfer Kontrolü:** Gönderen ve alıcının varlığı, yetersiz bakiye durumu ve kullanıcının *kendisine transfer yapma hatası* engellenmiştir.
* **Kronolojik Loglama:** Tüm başarılı yükleme ve transfer hareketleri anlık olarak ters kronolojik sırayla listelenir.

---

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Python 3.12, Flask Web Framework
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
* **Veri Yönetimi:** Bellek içi (In-Memory) veri yapıları (`dict` ve `list`) ile yüksek hızlı veri işleme.

---

## 🔌 API Dokümantasyonu (Endpoints)

Proje, frontend ile asenkron olarak haberleşen aşağıdaki RESTful API uç noktalarına sahiptir:

| Metot | Uç Nokta (Endpoint) | Açıklama |
| :--- | :--- | :--- |
| `GET` | `/api/wallets` | Tüm cüzdanları ve bakiyeleri listeler. |
| `POST` | `/api/wallets` | Yeni bir cüzdan oluşturur. *(Payload: `{"name": "Ahmet"}`)* |
| `POST` | `/api/wallets/<id>/deposit` | Cüzdana para yükler. *(Payload: `{"amount": 150.50}`)* |
| `POST` | `/api/transfer` | Cüzdanlar arası transfer yapar. *(Payload: `{"sender_id": 1, "receiver_id": 2, "amount": 50.00}`)* |

---

## 📂 Proje Yapısı

```text
├── main.py              # Flask backend sunucusu, validasyonlar ve API uç noktaları
├── templates/
│   └── index.html       # Tailwind CSS ve asenkron JS entegrasyonlu yönetim paneli
├── requirements.txt     # Projenin bağımlılık listesi
└── README.md            # Proje dökümantasyonu
```

---
## ⚙️ Kurulum ve Çalıştırma
Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla takip edin:

### 1. Projeyi Klonlayın ve Dizinine Gidin
```Bash
git clone [https://github.com/onurcanbircan/flask-digital-wallet.git](https://github.com/onurcanbircan/flask-digital-wallet.git)
cd flask-digital-wallet
```

### 2. Sanal Ortam Oluşturun ve Aktif Edin
## Windows için:
```Bash
python -m venv venv
venv\Scripts\activate
```
---
## macOS/Linux için:
```Bash
python3 -m venv venv
source venv/bin/activate
```
---
### 3. Gerekli Kütüphaneleri Kurun
```Bash
pip install flask
```
---
### 4. Uygulamayı Başlatın
```Bash
python main.py
```
Uygulama başlatıldıktan sonra tarayıcınızdan http://127.0.0.1:5000 adresine giderek yönetim paneline ulaşabilirsiniz.
