# All-Inkl Deployment Hızlı Başlangıç

## 🎯 Özet: 5 Adımda Yayınlama

### 1️⃣ Veritabanı Oluştur (All-Inkl KAS Panel)
- KAS paneline giriş yap
- "Datenbanken" → Yeni veritabanı oluştur
- PostgreSQL veya MySQL seç
- DB adı, kullanıcı, şifre not et

### 2️⃣ Dosyaları Yükle (FTP)
```
FTP Host: ftp.all-inkl.com
Kullanıcı: w016e54c
Dizin: /www/htdocs/lesezirkel/
```

Yüklenecekler:
- ✅ Tüm .py dosyaları
- ✅ templates/, static/, media/ dizinleri
- ✅ requirements.txt
- ✅ manage.py

Yüklenmeyecekler:
- ❌ .venv/, __pycache__/
- ❌ .git/
- ❌ *.sqlite3

### 3️⃣ SSH ile Kurulum
```bash
# SSH bağlantı
ssh w016e54c@ssh.all-inkl.com

# Proje dizini
cd /www/htdocs/lesezirkel/

# .env dosyası oluştur
nano .env
```

.env içeriği:
```bash
DJANGO_SECRET_KEY=buraya-güvenli-bir-key-yazın
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=lz-os.de,www.lz-os.de

DB_NAME=db_xxxxx     # All-Inkl'den aldığınız
DB_USER=db_xxxxx     # All-Inkl'den aldığınız
DB_PASSWORD=xxxxx    # Veritabanı şifresi
DB_HOST=localhost
DB_PORT=5432
```

Secret key oluştur:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4️⃣ Deployment Script
```bash
# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Paketler
pip install -r requirements.txt

# Django kurulum
python manage.py migrate --settings=lesezirkel_osnabrueck.settings_production
python manage.py collectstatic --noinput --settings=lesezirkel_osnabrueck.settings_production
python manage.py createsuperuser --settings=lesezirkel_osnabrueck.settings_production

# İzinler
chmod -R 755 media/ static/ logs/
```

### 5️⃣ All-Inkl Yapılandırma

**KAS Panel → Software → Python:**
- App Name: `lesezirkel`
- Python Version: `3.10+`
- App Directory: `/www/htdocs/lesezirkel/`
- WSGI File: `passenger_wsgi.py`
- Virtual Env: `/www/htdocs/lesezirkel/venv`

**Environment Variable ekle:**
```
DJANGO_SETTINGS_MODULE=lesezirkel_osnabrueck.settings_production
DJANGO_PRODUCTION=1
```

**Domain bağla:**
- Domain: `lz-os.de`
- SSL aktifleştir (Let's Encrypt)

## ✅ Test
```
https://lz-os.de          → Ana sayfa
https://lz-os.de/admin/   → Admin panel
```

## 🐛 Sorun mu var?

Log kontrol:
```bash
tail -f logs/production.log
tail -f logs/error.log
```

Restart:
```bash
touch tmp/restart.txt
```

Detaylı rehber: `DEPLOYMENT_ALLINKL.md`
