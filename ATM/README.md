# ATM Uygulaması 🏧

Python ile yazılmış QR kod desteği olan profesyonel ATM simülatörü.

**TürkBank ATM** — Gerçekçi bankacılık işlemleri, otomatik maaş sistemi ve kapsamlı hesap yönetimi.

## 🎯 Temel Özellikler

| Özellik | Açıklama |
|---------|----------|
| 🔐 **İkili Giriş** | Kartlı (kullanıcı adı/şifre) + Kartsız (QR kod) |
| 💳 **7 Ana İşlem** | Para çekme, transfer, yatırma, fatura ödeme, maaş takibi, hesap yönetimi |
| 🧾 **Akıllı Fatura** | 4 fatura türü, aylık otomatik üretim, gerçekçi tutarlar |
| 💰 **Maaş Otomasyonu** | İki tür maaş (elden/bankaya), aylık otomatik yatırma |
| 📊 **İşlem İzleme** | İşlem türü, tutar, saat belirterek son işlemleri gösterme |
| 🔊 **Sesli Arayüz** | pyttsx3 TTS, microfon girdisi desteği |
| 🛡️ **Güvenlik** | SHA-256 şifreleme, 3 yanlış şifreden sonra bloke |
| ⚙️ **Arka Plan Sistemleri** | Daemon thread'ler ile 24/7 maaş kontrolü

## 🚀 Kurulum

### Gereksinimler
- Python 3.13 veya üzeri
- Windows/Linux/macOS

### Adım 1: Projeyi İndir
```bash
git clone https://github.com/KULLANICI_ADINIZ/ATM.git
cd ATM
```

### Adım 2: Gerekli Paketleri Yükle
```bash
pip install -r requirements.txt
```

### Adım 3: Çalıştır
```bash
python exe.py
```

## 📂 Proje Yapısı

```
ATM/
├── exe.py                 # Ana giriş noktası
├── fonksiyonlar.py        # ATM işlem fonksiyonları
├── db.py                  # Veritabanı ayarları
├── fatura.py              # Fatura işlemleri
├── admin_paneli.py        # Admin paneli
├── sesler.py              # Sesli komut işlemleri
├── sesler_resimler/       # Ses dosyaları ve resimler
└── kullanici_data.db      # SQLite veritabanı
```

## Uygulama Mimarisi

### 1️⃣ Uygulama Başlangıcı

```
exe.py → atm_baslat()
    ├─ Maaş thread'lerini başlat (arka planda)
    ├─ Hoşgeldiniz sesi çal
    └─ Ana menü döngüsü
          ├─ 1) Kartlı işlem
          ├─ 2) Kartsız işlem
          └─ 3) Çıkış
```

### 2️⃣ Giriş Yöntemleri

#### **Kartlı İşlem** (kullanıcı adı + şifre)
```
kartli()
    ├─ 1) Mevcut hesap
    │   └─ mevcut_hesap_dogrula()
    │       ├─ Kullanıcı adı doğrula
    │       ├─ Şifre doğrula (SHA-256)
    │       ├─ 3 yanlış şifreden sonra hesap bloke
    │       └─ Başarılıysa islem() menüsüne git
    │
    ├─ 2) Yeni hesap aç
    │   └─ yeni_hesap_ac()
    │       ├─ Kullanıcı adı + şifre kuralları kontrol
    │       ├─ Otomatik IBAN üret
    │       ├─ 1000 TL bonus banka bakiyesi
    │       └─ islem() menüsüne git
    │
    └─ 3) Geri
```

#### **Kartsız İşlem** (QR kod)
```
kartsiz()
    ├─ 1) Resimden QR kodu oku
    │   └─ resimden_giris()
    │       └─ Dosya seçici → QR decode → islem()
    │
    ├─ 2) Kameradan QR oku (Canlı)
    │   └─ QR_giris()
    │       └─ Kamera aç → canlı okuma → ESC tuşu ile iptal
    │
    └─ 3) Geri
```

### 3️⃣ Ana İşlem Menüsü — `islem()`

Başarılı girişten sonra açılır. 7 seçenek içeren döngü:

```
1️⃣  PARA ÇEKME
    ├─ Sabit tutarlar: 100, 500, 1000, 2000, 5000, 10000 TL
    ├─ Özel tutar seçeneği
    ├─ Günlük limit: 10.000 TL ⚠️
    └─ Başarılı çekimde: bakiye → cep_bakiyesi aktarımı

2️⃣  PARA TRANSFERİ
    ├─ Tutar gir
    ├─ Alıcı IBAN gir (TR otomatik eklenir)
    ├─ DB'de IBAN kontrolü
    ├─ Günlük limit: 10.000 TL ⚠️
    └─ işlem kaydı

3️⃣  PARA YATIRMA (Cep → Hesap)
    ├─ Sabit tutarlar: 100, 500, 1000, 2000, 5000, 10000 TL
    ├─ Özel tutar seçeneği
    └─ Başarılı çekimde: cep_bakiyesi → bakiye aktarımı

4️⃣  ÖDEME İŞLEMLERİ
    └─ Fatura ödeme
        └─ 4 fatura türü seç veya tümünü öde
            ├─ Su (200–1200 TL)
            ├─ Elektrik (200–1100 TL)
            ├─ Doğalgaz (300–2500 TL, kış ↑)
            └─ İnternet (500–1250 TL)

5️⃣  MAAŞ TAKİBİ
    ├─ Elden (cep_bakiyesine yatırılır)
    └─ Bankaya (bakiyeye yatırılır)
        ├─ Meslek, tutar, gün kaydedilir
        ├─ Bugün maaş günüyse anında yatır
        └─ Kalanı gün veya saat cinsinden söyle

6️⃣  DİĞER İŞLEMLER
    ├─ Hesap bilgileri → hesap_sorgula()
    ├─ Kart yenileme → kart_yenileme() [yeni IBAN]
    ├─ Şifre değiştirme → sifre_degistirme() [şifre yenileme]
    ├─ Kartı bloke et → kart_bloke() [admin panelinden açılmalı]
    ├─ İşlem geçmişi (Son 20) → islem_gecmisi_goster() [son işlemlerin listesini ver]
    └─ Geri

7️⃣  ÇIKIŞ
    └─ Ana menüye dön
```

### 4️⃣ Arka Plan Sistemleri (Threading)

```
maas_sistemini_baslat()
    ├─ Daemon thread 1: maas_kontrol_sistemi_elden()
    │   └─ Her saat kontrol → Gün değişince elden maaş alan hesaplara yatır
    │
    └─ Daemon thread 2: maas_kontrol_sistemi_bakiye()
        └─ Her saat kontrol → Gün değişince banka maaş alan hesaplara yatır
```

### 5️⃣ Fatura Sistemi

```
Yeni hesap açılırken:
    └─ yeni_hesap_fatura_olustur()
        └─ 4 rastgele fatura tutarı üret → debts tablosuna kaydet

Her ay veya istek üzerine:
    └─ fatura_goster()
        └─ Bu ay fatura var mı kontrol
            ├─ Varsa: göster
            └─ Yoksa: yeni oluştur → su, elektrik, doğalgaz, internet

Ödeme sırasında:
    └─ fatura_ode()
        └─ Seçilen fatura bakiyeden azalt, debts tablosundan sıfırla
```

## 🗄️ Veritabanı Yapısı

```
kullanici_data.db (SQLite)
│
├─ users
│   ├─ id (Primary Key)
│   ├─ kullanici_adi (TEXT)
│   ├─ sifre (TEXT, SHA-256)
│   ├─ aktif (INTEGER: 1=aktif, 0=bloke)
│   ├─ bakiye (REAL, Başlangıç: 1000 TL)
│   ├─ cep_bakiyesi (REAL, Başlangıç: 0 TL)
│   └─ iban (TEXT, 24 karakter)
│
├─ transactions
│   ├─ id (Primary Key)
│   ├─ kullanici_id (Foreign Key)
│   ├─ islem_turu (TEXT)
│   ├─ tutar (REAL)
│   ├─ tarih (TIMESTAMP)
│   └─ aciklama (TEXT)
│
├─ personal_info
│   ├─ id (Primary Key)
│   ├─ kullanici_id (Foreign Key)
│   ├─ meslek (TEXT)
│   ├─ maas (REAL)
│   ├─ maas_gunu (INTEGER: 1–31)
│   └─ maas_turu (TEXT: 'E'=elden, 'B'=bankaya)
│
└─ debts
    ├─ id (Primary Key)
    ├─ kullanici_id (Foreign Key)
    ├─ elektrik (REAL)
    ├─ dogalgaz (REAL)
    ├─ su (REAL)
    ├─ internet (REAL)
    └─ odeme_tarihi (DATE)
```

## 🔊 Ses Sistemi

```
sesler.py
├─ sesli_input() → Bip sesi çalar
├─ hosgeldiniz() → Welcome to TurkBank (Bir kez)
├─ islem_turu_konustur() → "Please choose your transaction" (Bir kez)
├─ hesap_dogrula_konustur() → "Verifying account information" (Bir kez)
└─ pin_konustur() → "Please enter your PIN" (Bir kez)

Teknoloji: pyttsx3 (Text-to-Speech)
Girdi: speech_recognition (Microfon desteği)
```

## 🛡️ Güvenlik & Limitler

| Kısıtlama | Değer |
|-----------|-------|
| Şifre yanlış giriş | 3 kez → Hesap bloke |
| Kullanıcı adı yanlış | 5 kez → Ana menüye dön |
| Günlük para çekme | 10.000 TL max |
| Günlük transfer | 10.000 TL max |
| Şifre kuralları | Min 8 karakter, 1 büyük/küçük harf, 1 rakam |
| Şifreleme | SHA-256 hash |

## 👨‍💼 Admin Paneli

```
admin_paneli.py
├─ kullanici_aktiflik_ayarla()
│   └─ Bloke edilen kullanıcıyı tekrar aktif yapar
└─ Gelecek özellikler:...(çalışma aşamasında)
```

## 🛠️ Teknolojiler

- Python 3.8+
- SQLite3
- pyttsx3 (Sesli çıkış)
- SpeechRecognition (Sesli giriş)

## � Test Hesap Bilgileri

İlk kez çalıştırırken test etmek için bir hesap oluşturabilirsiniz:
- **Kullanıcı Adı**: test
- **Şifre**: Test1234 (8+ karakter, büyük/küçük harf, rakam)

Yeni hesap açtığında otomatik olarak:
- 1000 TL bakiye
- Rastgele IBAN

## 🚀 Adım Adım Çalışma Akışı

1. **Başlatma**: `python exe.py`
2. **Giriş**: Kartlı veya Kartsız yöntem seç
3. **İşlem**: 5 ana işlemden birini seç
4. **Ödeme**: Fatura öde veya para transfer et
5. **Takip**: İşlem geçmişini kontrol et
6. **Çıkış**: Ana menüye dön ve uygulamadan çık

## 💻 Test Hesap Bilgileri

İlk kez çalıştırırken test etmek için bir hesap oluşturabilirsiniz:
- **Kullanıcı Adı**: test
- **Şifre**: Test1234 (8+ karakter, büyük/küçük harf, rakam)

Yeni hesap açtığında otomatik olarak:
- 1000 TL bakiye
- Rastgele IBAN

## 📝 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasını gör.

## 🤝 Katkıda Bulunma

1. Repository'yi Fork et
2. Feature Branch oluştur (`git checkout -b feature/YeniOzellik`)
3. Değişiklikleri Commit et (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'e Push et (`git push origin feature/YeniOzellik`)
5. Pull Request aç

## ❓ Sıkça Sorulan Sorular

**S: İlk maaş tarihi ne zaman?**
- **C:** Maaş günü belirledikten sonra, o gün gelince otomatik yatırılır.

**S: Günlük limitler nedir?**
- **C:** Para çekme ve transfer için 10.000 TL günlük limit.

**S: Hesap bloke olursa ne yapmalıyım?**
- **C:** Admin panelinde `kullanici_aktiflik_ayarla()` ile tekrar açabilirsiniz.

**S: IBAN nasıl üretiliyor?**
- **C:** Otomatik rastgele üretiyor, TR ile başlayıp 24 karakter uzunluğunda.

**S: Şifre kuralları neler?**
- **C:** Minimum 8 karakter, en az 1 büyük harf, 1 küçük harf, 1 rakam gereklidir.

## 📧 İletişim

sametturkoglu4216@gmail.com

---

</div>
