# Dosya Yükleme Listesi - All-Inkl FTP

## ✅ YÜKLENECEK DOSYALAR

### Django Uygulamaları
- [ ] lesezirkel_osnabrueck/ (tüm klasör)
- [ ] main/ (tüm klasör)
- [ ] locale/ (tüm klasör)

### Templates ve Static
- [ ] templates/ (tüm klasör)
- [ ] static/ (tüm klasör)

### Boş Klasörler (oluşturulacak)
- [ ] media/ (boş klasör oluştur)
- [ ] logs/ (boş klasör oluştur)

### Kök Dizin Dosyaları
- [ ] manage.py
- [ ] requirements.txt
- [ ] passenger_wsgi.py
- [ ] .htaccess
- [ ] deploy_allinkl.sh
- [ ] README.md
- [ ] LICENSE

### Özel Dosyalar
- [ ] gunicorn.conf.py (isteğe bağlı)

---

## ❌ YÜKLENMEYECEK DOSYALAR

- ❌ .venv/ (virtual environment - sunucuda oluşturulacak)
- ❌ __pycache__/ (derlenmiş Python dosyaları)
- ❌ *.pyc (Python bytecode)
- ❌ .git/ (git deposu)
- ❌ .gitignore
- ❌ lesezirkel_osnabrueck.sqlite3 (local veritabanı)
- ❌ .env (local environment - sunucuda oluşturulacak)
- ❌ .env.example
- ❌ .env.production (şablon - içeriğini sunucuda .env olarak oluşturacağız)
- ❌ logs/*.log (local loglar)
- ❌ tests/ (test dosyaları - isteğe bağlı)
- ❌ *.md (dokümantasyon - isteğe bağlı)
- ❌ check_deployment.py (local script)
- ❌ save_logo.py (local script)

---

## 📦 YÜKLEME STRATEJİSİ

### Seçenek A: Klasör Klasör (Önerilen - İlk Kez)
1. lesezirkel_osnabrueck/ → Sürükle bırak
2. main/ → Sürükle bırak
3. templates/ → Sürükle bırak
4. static/ → Sürükle bırak
5. locale/ → Sürükle bırak
6. Tekil dosyalar → Sürükle bırak

### Seçenek B: Toplu Seçim
1. Sol panelde (Windows):
   - Ctrl+tıkla ile yukarıdaki klasörleri seç
2. Sağ panele (sunucu) sürükle
3. Transfer başlayacak

---

## ⏱️ TAHMİNİ SÜRE

- Toplam boyut: ~50-100 MB
- Süre: 5-15 dakika (internet hızına bağlı)

---

**Backup bitince bu listeyi kullanarak yükleyeceğiz!**
