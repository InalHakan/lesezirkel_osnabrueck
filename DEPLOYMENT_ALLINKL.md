# 🚀 All-Inkl'de Deployment Rehberi

Bu rehber, Lesezirkel Osnabrück projesinin All-Inkl hosting'de yayınlanması için adım adım talimatlar içerir.

## 📋 Ön Hazırlık

### 1. Gerekli Bilgileri Toplayın

All-Inkl KAS panelinizden şu bilgileri not edin:

- ✅ FTP kullanıcı adı: `w016e54c` (ekran görüntünüzde mevcut)
- ✅ FTP şifresi
- ✅ FTP sunucu adresi: Genellikle `lz-os.de` veya `ftp.all-inkl.com`
- ✅ SSH erişim bilgileri (varsa)
- ✅ Veritabanı adı, kullanıcı adı ve şifresi

### 2. Veritabanı Oluşturun

1. All-Inkl KAS paneline giriş yapın
2. **Datenbanken** (Veritabanları) bölümüne gidin
3. Yeni bir veritabanı oluşturun:
   - PostgreSQL (önerilen) veya MySQL seçin
   - Veritabanı adı: `db_lesezirkel` (veya otomatik verilen ad)
   - Kullanıcı ve şifre oluşturun
   - Bu bilgileri not edin!

### 3. Python Sürümü Kontrolü

All-Inkl'de Python 3.8+ kurulu olduğundan emin olun:
- KAS panelinden "Software" > "Python" bölümüne bakın
- Gerekirse Python'u aktifleştirin

## 📁 Dosyaları Sunucuya Yükleme

### Yöntem 1: FTP ile (Önerilen - İlk Yükleme için)

1. **FileZilla** veya benzeri FTP programı kullanın:
   ```
   Host: ftp.all-inkl.com veya lz-os.de
   Kullanıcı: w016e54c
   Şifre: [All-Inkl şifreniz]
   Port: 21 (FTP) veya 22 (SFTP)
   ```

2. Şu dosyaları **YÜKLEMEYIN**:
   - `.venv/` dizini
   - `__pycache__/` dizinleri
   - `*.pyc` dosyaları
   - `.git/` dizini
   - `lesezirkel_osnabrueck.sqlite3` (local veritabanı)
   - `.env` dosyası (sunucuda oluşturacaksınız)

3. Yükleyeceğiniz dosyalar:
   - Tüm Python dosyaları (`.py`)
   - `requirements.txt`
   - `manage.py`
   - `static/` dizini
   - `media/` dizini (boş olabilir)
   - `templates/` dizini
   - `main/` ve `lesezirkel_osnabrueck/` dizinleri
   - `locale/` dizini

### Yöntem 2: Git ile (SSH Erişimi Varsa)

SSH ile sunucuya bağlanın ve:

```bash
cd /www/htdocs/
git clone https://github.com/InalHakan/lesezirkel_osnabrueck.git
cd lesezirkel_osnabrueck
```

## ⚙️ Sunucuda Kurulum

### 1. SSH ile Sunucuya Bağlanın

```bash
ssh w016e54c@lz-os.de
# veya
ssh w016e54c@ssh.all-inkl.com
```

### 2. Proje Dizinine Gidin

```bash
cd /www/htdocs/lesezirkel_osnabrueck  # veya proje dizininiz
```

### 3. Environment Dosyasını Oluşturun

```bash
nano .env
# veya
vim .env
```

Şu içeriği ekleyin (kendi bilgilerinizle değiştirin):

```bash
DJANGO_SECRET_KEY=güvenli-bir-secret-key-buraya-yazın
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=lesezirkel-os.de,www.lesezirkel-os.de

DB_NAME=db_XXXXX  # All-Inkl'den aldığınız DB adı
DB_USER=db_XXXXX  # All-Inkl DB kullanıcısı
DB_PASSWORD=veritabani-sifreniz
DB_HOST=localhost
DB_PORT=5432  # PostgreSQL için, MySQL için 3306
```

**Secret Key Oluşturma:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Virtual Environment Oluşturun

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Paketleri Yükleyin

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Not:** All-Inkl'de PostgreSQL kullanıyorsanız:
```bash
pip install psycopg2-binary
```

MySQL kullanıyorsanız:
```bash
pip install mysqlclient
```

### 6. Environment Variables Yükleyin

`.env` dosyasını okumak için `python-decouple` veya `python-dotenv` yükleyin:

```bash
pip install python-decouple
```

Sonra `settings_production.py` dosyasını güncelleyin:

```python
from decouple import config

SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

### 7. Deployment Script'i Çalıştırın

```bash
chmod +x deploy_allinkl.sh
./deploy_allinkl.sh
```

Veya manuel olarak:

```bash
# Migration'lar
python manage.py migrate --settings=lesezirkel_osnabrueck.settings_production

# Static dosyalar
python manage.py collectstatic --noinput --settings=lesezirkel_osnabrueck.settings_production

# Çeviri dosyaları
python manage.py compilemessages --settings=lesezirkel_osnabrueck.settings_production

# Admin kullanıcısı
python manage.py createsuperuser --settings=lesezirkel_osnabrueck.settings_production
```

### 8. Dosya İzinlerini Ayarlayın

```bash
chmod -R 755 media/
chmod -R 755 static/
chmod -R 755 logs/
mkdir -p logs
```

## 🌐 All-Inkl KAS Panelinde Ayarlar

### 1. Python Uygulaması Yapılandırma

All-Inkl KAS panelinde:

1. **Software** > **Python** bölümüne gidin
2. Yeni bir Python uygulaması ekleyin:
   - **App Name:** `lesezirkel`
   - **Python Version:** 3.10 veya 3.11
   - **App Directory:** `/www/htdocs/lesezirkel_osnabrueck`
   - **WSGI File:** `lesezirkel_osnabrueck/wsgi.py`
   - **Virtual Env:** `/www/htdocs/lesezirkel_osnabrueck/venv`

3. **Environment Variables** ekleyin:
   ```
   DJANGO_SETTINGS_MODULE=lesezirkel_osnabrueck.settings_production
   ```

### 2. Domain Ayarları

1. **Domain** bölümünde:
   - `lz-os.de` domain'ini seçin
   - Python uygulamanıza yönlendirin
   - SSL/TLS sertifikasını aktifleştirin (Let's Encrypt - ücretsiz)

### 3. .htaccess Dosyası (Gerekirse)

All-Inkl'de Apache kullanılıyorsa, proje kök dizinine `.htaccess` dosyası ekleyin:

```apache
# .htaccess
RewriteEngine On

# Static dosyalar
RewriteCond %{REQUEST_URI} ^/static/
RewriteRule ^(.*)$ - [L]

# Media dosyalar
RewriteCond %{REQUEST_URI} ^/media/
RewriteRule ^(.*)$ - [L]

# Django'ya yönlendir
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ /passenger_wsgi.py [L]
```

## 🔐 Güvenlik Kontrolleri

### 1. DEBUG Modu Kapalı mı?

```bash
python manage.py shell --settings=lesezirkel_osnabrueck.settings_production
>>> from django.conf import settings
>>> print(settings.DEBUG)  # False olmalı
>>> exit()
```

### 2. ALLOWED_HOSTS Doğru mu?

```bash
>>> print(settings.ALLOWED_HOSTS)  # ['lz-os.de', 'www.lz-os.de'] olmalı
```

### 3. Secret Key Güvenli mi?

- `.env` dosyası git'e eklenmemeli
- Secret key en az 50 karakter olmalı

### 4. HTTPS Aktif mi?

- All-Inkl KAS panelinden SSL sertifikası kontrolü
- Tarayıcıda kilit ikonu görünmeli

## 📊 Test ve Kontroller

### 1. Siteyi Ziyaret Edin

```
https://lz-os.de
```

### 2. Admin Paneline Giriş

```
https://lz-os.de/admin/
```

### 3. Static Dosyalar Yükleniyor mu?

- CSS stilleri görünüyor mu?
- Görseller yükleniyor mu?
- JavaScript çalışıyor mu?

### 4. Veritabanı Bağlantısı

- Veritabanı hatası alıyor musunuz?
- Migration'lar çalıştı mı?

## 🐛 Sorun Giderme

### Static Dosyalar Yüklenmiyor

```bash
python manage.py collectstatic --noinput --clear --settings=lesezirkel_osnabrueck.settings_production
```

### Veritabanı Bağlantı Hatası

- `.env` dosyasındaki DB bilgilerini kontrol edin
- All-Inkl'de veritabanının aktif olduğundan emin olun

### 500 Internal Server Error

Log dosyalarını kontrol edin:
```bash
tail -f logs/production.log
tail -f logs/error.log
```

### Import Hatası

```bash
pip install -r requirements.txt --force-reinstall
```

## 📝 Güncellemeler için

Kod değişikliklerinden sonra:

```bash
cd /www/htdocs/lesezirkel_osnabrueck
source venv/bin/activate
git pull origin main  # Git kullanıyorsanız
pip install -r requirements.txt
python manage.py migrate --settings=lesezirkel_osnabrueck.settings_production
python manage.py collectstatic --noinput --settings=lesezirkel_osnabrueck.settings_production
```

Sonra uygulamayı yeniden başlatın (KAS panelinden veya):
```bash
touch tmp/restart.txt  # Passenger için
```

## 📞 Yardım

Sorun yaşarsanız:

1. All-Inkl destek ekibi: https://all-inkl.com/support/
2. Django dokümantasyonu: https://docs.djangoproject.com/
3. Proje log dosyaları: `logs/production.log`

## ✅ Kontrol Listesi

- [ ] Veritabanı oluşturuldu
- [ ] `.env` dosyası yapılandırıldı
- [ ] Virtual environment kuruldu
- [ ] Paketler yüklendi
- [ ] Migration'lar çalıştırıldı
- [ ] Static dosyalar toplandı
- [ ] Admin kullanıcısı oluşturuldu
- [ ] Domain bağlandı
- [ ] SSL aktifleştirildi
- [ ] Site test edildi
- [ ] Admin paneli çalışıyor

---

**Başarılar! 🎉**

Herhangi bir sorunla karşılaşırsanız log dosyalarını kontrol edin veya All-Inkl destek ekibine başvurun.
