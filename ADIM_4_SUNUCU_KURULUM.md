# 🚀 ADIM 4: SUNUCUDA KURULUM (SSH Olmadan)

## ✅ TRANSFER TAMAMLANDI MI?

WinSCP'de transfer bittiğinde:
- Sağ panelde Django klasörleri görünecek
- Queue (1) → Queue (0) olacak

---

## 📝 SONRAKI ADIMLAR (Transfer bitince)

### 1️⃣ .env DOSYASI OLUŞTUR

**SORUN:** SSH yok, `.env` dosyasını nasıl oluşturacağız?

**ÇÖZÜM:** WinSCP ile dosya oluşturacağız!

#### WinSCP'de:
1. Sağ panelde (sunucu) → sağ tık
2. **"New" → "File"** seçin
3. Dosya adı: `.env`
4. **"OK"** tıklayın
5. Dosya açılacak → `.env.production` içeriğini kopyala-yapıştır
6. **Kaydet**

---

### 2️⃣ BOŞ KLASÖRLER OLUŞTUR

Sunucuda şu klasörleri oluşturun:

#### WinSCP'de sağ panel:
1. Sağ tık → **"New" → "Directory"**
2. `media` oluştur
3. Sağ tık → **"New" → "Directory"**
4. `logs` oluştur

---

### 3️⃣ DOSYA İZİNLERİ

Bazı klasörlere yazma izni vermemiz gerekebilir:

#### WinSCP'de:
1. `media` klasörüne sağ tık → **"Properties"**
2. **Permissions:** `0755` (rwxr-xr-x)
3. Aynısını `logs` için de yap

---

### 4️⃣ ALL-INKL KAS PANELİNDE PYTHON YAPILANDIRMASI

SSH olmadığı için All-Inkl'in "Software-Installation" özelliğini kullanacağız:

#### KAS Panelinde:
1. **"Software-Installation"** sekmesi
2. **"Python"** bul
3. Şu bilgileri gir:
   - **App Name:** lesezirkel
   - **Python Version:** 3.10 veya 3.11
   - **App Directory:** `/www/htdocs/w016e54c/`
   - **Entry Point:** `passenger_wsgi.py`

---

### 5️⃣ PAKET KURULUMU (Zor Kısım - SSH Olmadan)

**SORUN:** `pip install -r requirements.txt` nasıl çalıştıracağız?

**ÇÖZÜMLER:**

#### A) All-Inkl Python Console (Varsa)
- KAS panelinde "Python Console" var mı bak
- Varsa terminal açılır, komut çalıştırabilirsiniz

#### B) Cron Job ile
- Geçici bir script oluştur
- Cron job ile çalıştır

#### C) PHP Exec (Son çare)
- PHP ile Python komutları çalıştır

---

### 6️⃣ MIGRATION VE COLLECTSTATIC

Aynı şekilde:
```bash
python manage.py migrate --settings=lesezirkel_osnabrueck.settings_production
python manage.py collectstatic --noinput --settings=lesezirkel_osnabrueck.settings_production
python manage.py createsuperuser --settings=lesezirkel_osnabrueck.settings_production
```

---

## 🎯 SONRAKI ADIM

**Transfer bittiğinde bana haber verin!**

Adım adım ilerleyeceğiz:
1. .env dosyası oluştur ✅
2. Klasörler oluştur ✅
3. KAS panelinde Python yapılandır 🔧
4. Paket kurulumu (en zor kısım) ⚙️

**Transfer bitince devam edelim!** 🚀
