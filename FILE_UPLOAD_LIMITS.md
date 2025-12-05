# Datei-Upload-Limits / Dosya Yükleme Limitleri

## Problem: 413 Request Entity Too Large

Wenn Sie beim Hochladen von Dateien (Bilder, Dokumente) einen **413-Fehler** erhalten, liegt das an zu restriktiven Upload-Limits.

---

## 🔧 Lösungen / Çözümler

### 1. **Django Settings** (Bereits konfiguriert / Zaten yapılandırılmış)

In `lesezirkel_osnabrueck/settings.py`:

```python
# File Upload Settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
```

**Für größere Dateien / Daha büyük dosyalar için:**
```python
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
```

---

### 2. **Development Server** (Django runserver)

Django's Development Server hat standardmäßig keine Upload-Limits. Wenn trotzdem Probleme auftreten:

1. **Server neu starten:**
   ```bash
   python manage.py runserver
   ```

2. **Prüfen Sie die Dateigröße:**
   - Event-Bilder sollten < 10 MB sein
   - Dokumente sollten < 10 MB sein
   - Bei größeren Dateien: Settings anpassen (siehe oben)

---

### 3. **Production Server** (Nginx/Apache)

#### **Nginx** (nginx.conf.example ist bereits konfiguriert):

```nginx
server {
    # ...
    client_max_body_size 100M;  # Maximale Upload-Größe
    # ...
}
```

**Nach Änderungen Nginx neu starten:**
```bash
sudo systemctl restart nginx
# oder
sudo service nginx restart
```

#### **Apache** (.htaccess oder httpd.conf):

```apache
LimitRequestBody 104857600  # 100 MB in Bytes
```

---

### 4. **Passenger (All-Inkl oder ähnliche Hosts)**

In `passenger_wsgi.py` ist bereits konfiguriert. Bei Problemen:

1. **Überprüfen Sie die Datei-Größe** in der Admin-Oberfläche
2. **Kontaktieren Sie Ihren Hosting-Provider** für Host-spezifische Limits

---

## 📊 Empfohlene Dateigrößen / Önerilen Dosya Boyutları

| Dateityp | Maximale Größe | Empfohlen |
|----------|---------------|-----------|
| **Event-Bilder** | 10 MB | 2-5 MB |
| **News-Bilder** | 10 MB | 2-5 MB |
| **Galerie-Bilder** | 10 MB | 2-5 MB |
| **Team-Fotos** | 10 MB | 1-3 MB |
| **PDF-Dokumente** | 10 MB | < 5 MB |
| **Zertifikate** | 10 MB | < 2 MB |

---

## 🖼️ Bilder vor dem Upload optimieren

### Online-Tools:
- **TinyPNG**: https://tinypng.com/ (PNG/JPG Komprimierung)
- **Squoosh**: https://squoosh.app/ (Google's Bild-Optimizer)
- **CompressJPEG**: https://compressjpeg.com/

### Desktop-Tools:
- **IrfanView** (Windows)
- **GIMP** (Windows/Mac/Linux)
- **XnConvert** (Windows/Mac/Linux)

### Empfohlene Einstellungen:
- **Format**: JPEG für Fotos, PNG für Logos
- **Qualität**: 80-85% (guter Kompromiss)
- **Maximale Breite**: 1920px (Full HD)
- **Maximale Höhe**: 1080px

---

## 🔍 Fehlerdiagnose / Hata Teşhisi

### Problem: 413-Fehler weiterhin vorhanden

**Überprüfen Sie:**

1. **Django Settings:**
   ```bash
   python manage.py shell
   >>> from django.conf import settings
   >>> settings.DATA_UPLOAD_MAX_MEMORY_SIZE
   10485760  # Sollte 10485760 (10 MB) oder höher sein
   ```

2. **Server neu gestartet?**
   - Development: `python manage.py runserver` neu starten
   - Production: Nginx/Apache/Passenger neu starten

3. **Dateigröße prüfen:**
   ```bash
   # Windows PowerShell
   (Get-Item "pfad\zur\datei.jpg").Length / 1MB
   # Sollte < 10 MB sein
   ```

4. **Browser-Cache leeren:**
   - Chrome/Edge: `Ctrl + Shift + Delete`
   - Firefox: `Ctrl + Shift + Delete`

---

## 📝 Notizen

- **Aktuelle Limits**: 10 MB pro Datei
- **Änderungen**: Nach Änderungen in `settings.py` immer Server neu starten
- **Production**: Bei All-Inkl oder ähnlichen Hosts kann es zusätzliche Limits geben
- **Performance**: Kleinere Dateien = schnellere Ladezeiten = bessere User Experience

---

## 🆘 Support

Bei weiteren Problemen:
1. Server-Logs überprüfen
2. Browser-Entwicklertools (F12) → Network → Upload prüfen
3. Hosting-Provider kontaktieren (für Production-Server)

---

**Stand**: Dezember 2025
