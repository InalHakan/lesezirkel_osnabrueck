# 🚀 ADIM 3: Django Projesini Hazırlama

## ✅ ŞU ANDA DURUM
- FTP bağlantısı başarılı ✅
- Eski site backup alınıyor ✅
- Veritabanı oluşturuldu (d0457c29) ✅

---

## 📝 ŞİMDİ YAPACAĞIMIZ

### 1. SECRET KEY OLUŞTURALIM

Terminalinizde (PowerShell) şu komutu çalıştırın:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Bu size 50+ karakterlik güvenli bir key verecek. **Kaydedin!**

---

### 2. .env DOSYASI OLUŞTURALIM

Proje dizininizde `.env` dosyası oluşturacağız.

**Bu dosyayı sunucuya yükleyeceğiz (FTP ile değil, SSH ile).**

---

### 3. MYSQL İÇİN PROJE AYARLARI

Django'nun MySQL ile çalışması için `mysqlclient` paketine ihtiyacımız var.

Local'de test etmek için (isteğe bağlı):
```powershell
pip install mysqlclient
```

**NOT:** Windows'ta `mysqlclient` kurulumu zor olabilir. Sunucuda kuracağız.

---

### 4. YÜKLENMEYECEKLERİ BELİRLEYELİM

FTP ile şunları **YÜKLEMEYECEĞIZ:**
- `.venv/` 
- `__pycache__/`
- `*.pyc`
- `.git/`
- `lesezirkel_osnabrueck.sqlite3`
- `logs/`

---

## 🎯 SONRAKI ADIMLAR (Backup bitince)

1. [ ] Sunucudaki eski dosyaları sil
2. [ ] Django dosyalarını FTP ile yükle
3. [ ] SSH ile bağlan (veya alternatif yöntem)
4. [ ] `.env` dosyası oluştur
5. [ ] Virtual environment kur
6. [ ] Paketleri yükle
7. [ ] Migration yap
8. [ ] Test et

---

**Şimdi SECRET KEY oluşturalım!**
