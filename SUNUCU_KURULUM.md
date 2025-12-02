# 🚀 Lesezirkel Osnabrück - Sunucu Kurulum Rehberi

## Sunucu Bilgileri
- **Domain:** lesezirkel-os.de, www.lesezirkel-os.de
- **Sunucu Dizini:** `/var/www/lesezirkel-os.de/app/`
- **Python:** 3.10.12
- **Veritabanı:** SQLite (dosya tabanlı, kolay)

---

## 📋 Kurulum Adımları

### 1️⃣ Dosyaları Sunucuya Yükle (WinSCP ile)

**WinSCP'de:**
- Sol taraf (local): `D:\Programmieren\Lesezirkel_Osna`
- Sağ taraf (sunucu): `/var/www/lesezirkel-os.de/app/`

**Yüklenecek dosyalar:**
- ✅ `lesezirkel_osnabrueck/` (klasör)
- ✅ `main/` (klasör)
- ✅ `templates/` (klasör)
- ✅ `static/` (klasör)
- ✅ `locale/` (klasör)
- ✅ `manage.py`
- ✅ `requirements.txt`
- ✅ `.env.example`

**Yüklemeyecek dosyalar:**
- ❌ `.venv/` (klasör)
- ❌ `__pycache__/` (klasörler)
- ❌ `*.pyc` (dosyalar)
- ❌ `db.sqlite3` (local veritabanı)
- ❌ `.git/` (klasör)

---

### 2️⃣ SSH'da Klasörleri Oluştur

```bash
cd /var/www/lesezirkel-os.de/app

# Boş klasörler oluştur
mkdir -p media/certificates media/documents media/events media/gallery media/news media/team
mkdir -p logs
mkdir -p staticfiles

# İzinleri ayarla
chmod 755 media logs staticfiles
```

---

### 3️⃣ .env Dosyasını Oluştur

```bash
cd /var/www/lesezirkel-os.de/app

# .env.example'dan kopyala
cp .env.example .env

# Düzenle
nano .env
```

**`.env` içeriği:**
```bash
# Secret Key oluştur (aşağıdaki komutu local'de çalıştır)
DJANGO_SECRET_KEY=buraya-yeni-secret-key-yaz

DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=lesezirkel-os.de,www.lesezirkel-os.de

DB_ENGINE=sqlite

DJANGO_SETTINGS_MODULE=lesezirkel_osnabrueck.settings_production
```

**Secret Key oluşturmak için (local bilgisayarda):**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### 4️⃣ Virtual Environment Oluştur

```bash
cd /var/www/lesezirkel-os.de/app

# Virtual environment oluştur
python3 -m venv venv

# Aktifleştir
source venv/bin/activate

# Paketleri yükle
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 5️⃣ Veritabanını Oluştur

```bash
# Hala venv içindesiniz
cd /var/www/lesezirkel-os.de/app
source venv/bin/activate  # Eğer kapatmışsanız tekrar aktifleştirin

# Migrations oluştur
python manage.py makemigrations

# Veritabanını oluştur
python manage.py migrate

# Superuser (admin) oluştur
python manage.py createsuperuser
# Kullanıcı adı: admin (veya istediğiniz)
# Email: info@lesezirkel-os.de
# Şifre: güçlü bir şifre
```

---

### 6️⃣ Static Dosyaları Topla

```bash
python manage.py collectstatic --noinput
```

---

### 7️⃣ Test Et

```bash
# Test sunucusu başlat
python manage.py runserver 0.0.0.0:8000
```

**Tarayıcıda test et:**
- `http://SUNUCU-IP:8000` (çalışıyor mu?)

Çalışıyorsa `Ctrl+C` ile durdur.

---

### 8️⃣ Gunicorn ile Production Başlat

```bash
# Gunicorn'i başlat
gunicorn lesezirkel_osnabrueck.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --daemon \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --pid /tmp/gunicorn.pid
```

**Kontrol et:**
```bash
ps aux | grep gunicorn  # Çalışıyor mu?
```

**Durdur:**
```bash
kill $(cat /tmp/gunicorn.pid)
```

---

### 9️⃣ Nginx/Apache Yapılandırması

Sunucu sahibinden **reverse proxy** ayarı yapmasını isteyin:
- Domain: `lesezirkel-os.de`, `www.lesezirkel-os.de`
- Backend: `127.0.0.1:8000` (Gunicorn)
- Static: `/var/www/lesezirkel-os.de/app/staticfiles/`
- Media: `/var/www/lesezirkel-os.de/app/media/`

---

## 🔧 Yararlı Komutlar

```bash
# Virtual environment aktifleştir
source /var/www/lesezirkel-os.de/app/venv/bin/activate

# Gunicorn durumu kontrol et
ps aux | grep gunicorn

# Gunicorn'i yeniden başlat
kill $(cat /tmp/gunicorn.pid)
gunicorn lesezirkel_osnabrueck.wsgi:application --bind 0.0.0.0:8000 --workers 3 --daemon

# Logları kontrol et
tail -f logs/error.log
tail -f logs/access.log

# Django shell
python manage.py shell

# Yeni migration oluştur
python manage.py makemigrations
python manage.py migrate
```

---

## ✅ Son Kontroller

- [ ] `.env` dosyası oluşturuldu ve SECRET_KEY ayarlandı
- [ ] Virtual environment oluşturuldu
- [ ] Paketler yüklendi (`pip install -r requirements.txt`)
- [ ] Veritabanı migrate edildi
- [ ] Superuser oluşturuldu
- [ ] Static dosyalar toplandı
- [ ] Gunicorn çalışıyor
- [ ] Domain yönlendirmesi yapıldı
- [ ] `https://lesezirkel-os.de` çalışıyor ✨

---

## 📞 Sorun mu var?

1. **Gunicorn çalışmıyor:**
   ```bash
   tail -f logs/error.log
   ```

2. **Static dosyalar görünmüyor:**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Database hatası:**
   ```bash
   python manage.py migrate
   ```

4. **DEBUG modda test et:**
   `.env` dosyasında `DJANGO_DEBUG=True` yap ve `python manage.py runserver 0.0.0.0:8000`
