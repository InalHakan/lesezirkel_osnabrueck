# 🚀 All-Inkl'e Deployment Yapılacak Değişiklikler

Bu dosya, projenizin All-Inkl hosting'e yayınlanması için yapılan değişiklikleri özetler.

## ✅ Eklenen Dosyalar

### 1. `.env.example` - Çevre Değişkenleri Şablonu
- Production ortamı için gerekli environment variables
- Veritabanı, secret key, domain ayarları
- **ÖNEMLİ:** Sunucuda `.env` dosyası oluşturup bu şablonu doldurun

### 2. `DEPLOYMENT_ALLINKL.md` - Detaylı Deployment Rehberi
- Adım adım All-Inkl kurulum talimatları
- FTP, SSH, veritabanı kurulumu
- Sorun giderme ve test adımları
- Güvenlik kontrolleri

### 3. `QUICKSTART_ALLINKL.md` - Hızlı Başlangıç
- 5 adımda yayınlama özeti
- En önemli komutlar
- Hızlı referans

### 4. `deploy_allinkl.sh` - Otomatik Deployment Script
- SSH üzerinden çalıştırılacak bash script
- Virtual environment kurulumu
- Migration, collectstatic, compilemessages
- Dosya izinleri

### 5. `passenger_wsgi.py` - WSGI Entry Point
- All-Inkl'in Passenger sistemi için WSGI dosyası
- Python path ve environment ayarları
- Production settings yükleme

### 6. `.htaccess` - Apache Yapılandırması
- Passenger yapılandırması
- Static ve media dosya aliasları
- Güvenlik header'ları
- Gzip compression

## 🔧 Güncellenen Dosyalar

### 1. `lesezirkel_osnabrueck/settings_production.py`
**Değişiklikler:**
- ✅ Domain güncellendi: `lz-os.de`, `www.lz-os.de`
- ✅ Veritabanı ayarları All-Inkl için düzenlendi
- ✅ `python-decouple` ile `.env` dosyası desteği eklendi
- ✅ SQLite alternatifi yorum satırı olarak eklendi
- ✅ Log dosya yolları düzeltildi (göreceli yollar)
- ✅ Email ayarları eklendi (All-Inkl SMTP)
- ✅ WhiteNoise static file storage
- ✅ Admin email adresi: `info@lz-os.de`

**Eski:**
```python
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
DB_NAME = 'kulturbrucke'
```

**Yeni:**
```python
ALLOWED_HOSTS = ['lz-os.de', 'www.lz-os.de']
DB_NAME = os.environ.get('DB_NAME', 'db_XXXXX')
```

### 2. `requirements.txt`
**Eklenen:**
- ✅ `python-decouple>=3.8` - Environment variable yönetimi için

### 3. `.gitignore`
Zaten mevcuttu, kontrol edildi:
- ✅ `.env` dosyaları ignore ediliyor
- ✅ `venv/`, `__pycache__/` ignore ediliyor
- ✅ SQLite veritabanı ignore ediliyor
- ✅ `logs/`, `staticfiles/` ignore ediliyor

## 📋 Yapılması Gerekenler (Checklist)

### All-Inkl KAS Panelinde:
- [ ] PostgreSQL/MySQL veritabanı oluştur
- [ ] Veritabanı kullanıcısı ve şifre not et
- [ ] Python app yapılandırması yap
- [ ] Domain'i bağla
- [ ] SSL sertifikası aktifleştir (Let's Encrypt)

### FTP ile:
- [ ] Proje dosyalarını yükle (`.venv`, `__pycache__` hariç)
- [ ] `media/` ve `logs/` dizinlerinin yazılabilir olduğundan emin ol

### SSH ile Sunucuda:
- [ ] `.env` dosyası oluştur ve doldur
- [ ] Secret key oluştur
- [ ] Virtual environment kur: `python3 -m venv venv`
- [ ] Paketleri yükle: `pip install -r requirements.txt`
- [ ] Migration'ları çalıştır
- [ ] Static dosyaları topla
- [ ] Superuser oluştur
- [ ] Dosya izinlerini ayarla

### Test:
- [ ] `https://lz-os.de` - Ana sayfa çalışıyor mu?
- [ ] `https://lz-os.de/admin/` - Admin panel erişilebiliyor mu?
- [ ] CSS/JS yükleniyor mu?
- [ ] Resimler görünüyor mu?
- [ ] Veritabanı bağlantısı çalışıyor mu?

## 🔑 Önemli Notlar

### 1. Environment Variables (`.env` dosyası)
Sunucuda mutlaka `.env` dosyası oluşturun:
```bash
cd /www/htdocs/lesezirkel/
nano .env
```

Şu değerleri doldurun:
- `DJANGO_SECRET_KEY` - Güvenli bir key (50+ karakter)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD` - All-Inkl'den aldığınız değerler
- `DJANGO_ALLOWED_HOSTS` - Domain adlarınız

### 2. Secret Key Oluşturma
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Veritabanı
All-Inkl'de PostgreSQL veya MySQL kullanabilirsiniz:
- **PostgreSQL:** Port 5432, `psycopg2-binary` paketi
- **MySQL:** Port 3306, `mysqlclient` paketi gerekir

Küçük projeler için SQLite de kullanılabilir.

### 4. Static Files
Production'da statik dosyalar `collectstatic` ile toplanmalı:
```bash
python manage.py collectstatic --noinput --settings=lesezirkel_osnabrueck.settings_production
```

### 5. Media Files
Kullanıcı yüklemeleri `media/` dizinine kaydedilir. Yazma izni olmalı:
```bash
chmod -R 755 media/
```

### 6. Logs
Log dosyaları `logs/` dizininde saklanır:
```bash
mkdir -p logs
chmod -R 755 logs/
```

### 7. HTTPS/SSL
All-Inkl'de ücretsiz Let's Encrypt SSL:
- KAS panelinden kolayca aktifleştirilebilir
- Otomatik yenilenir

## 🆘 Sorun Giderme

### Static dosyalar yüklenmiyor
```bash
python manage.py collectstatic --clear --noinput --settings=lesezirkel_osnabrueck.settings_production
```

### 500 Internal Server Error
```bash
# Log dosyalarını kontrol edin
tail -f logs/production.log
tail -f logs/error.log
```

### Veritabanı bağlantı hatası
- `.env` dosyasındaki DB bilgilerini kontrol edin
- All-Inkl'de veritabanının aktif olduğunu doğrulayın

### Import hatası
```bash
pip install -r requirements.txt --force-reinstall
```

### Uygulama yeniden başlatma (Passenger)
```bash
mkdir -p tmp
touch tmp/restart.txt
```

## 📚 Daha Fazla Bilgi

- **Detaylı Rehber:** `DEPLOYMENT_ALLINKL.md`
- **Hızlı Başlangıç:** `QUICKSTART_ALLINKL.md`
- **Django Production:** https://docs.djangoproject.com/en/stable/howto/deployment/
- **All-Inkl Destek:** https://all-inkl.com/support/

## 🎯 Sonuç

Projeniz All-Inkl'de yayınlanmaya hazır! 

**Sıradaki adımlar:**
1. `QUICKSTART_ALLINKL.md` dosyasını okuyun (5 adımda deployment)
2. Sorun yaşarsanız `DEPLOYMENT_ALLINKL.md` detaylı rehbere bakın
3. `.env.example` dosyasını `.env` olarak kopyalayıp doldurun

**Başarılar! 🎉**
