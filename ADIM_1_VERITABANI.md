# 🚀 All-Inkl KAS - İlk Kurulum Adımları

## ✅ ADIM 1: VERİTABANI OLUŞTUR (ŞU AN YAPACAĞINIZ)

### KAS Panelinde:

1. **Sol menüden "Datenbanken" (Veritabanları) tıklayın**

2. **"Neue Datenbank anlegen" (Yeni veritabanı oluştur) butonuna tıklayın**

3. **Veritabanı tipini seçin:**
   - ✅ **MySQL/MariaDB** (Önerilen - daha yaygın)
   - ⚠️ PostgreSQL (Django ile uyumlu ama All-Inkl'de nadiren kullanılır)

4. **Veritabanı bilgilerini kaydedin:**
   ```
   Veritabanı Adı: db_____  (otomatik oluşturulacak)
   Kullanıcı Adı: db_____   (otomatik oluşturulacak)
   Şifre: __________        (siz belirleyeceksiniz)
   Host: localhost
   Port: 3306 (MySQL için)
   ```

5. **ÖNEMLİ:** Bu bilgileri bir yere not edin! Daha sonra `.env` dosyasına yazacağız.

---

## ⏭️ ADIM 2: FTP BİLGİLERİNİ BULUN (Sonraki adım)

Veritabanını oluşturduktan sonra:

1. Sol menüden **"FTP"** bölümüne gidin
2. FTP kullanıcınız zaten var: `w016e54c`
3. FTP şifrenizi kontrol edin (unuttuysanız sıfırlayın)
4. Bu bilgileri kaydedin:
   ```
   FTP Host: ftp.kasserver.com veya lz-os.de
   FTP Kullanıcı: w016e54c
   FTP Şifre: [şifreniz]
   FTP Dizin: /www/htdocs/w016e54c/
   ```

---

## 📝 SONRAKİ ADIMLAR (Henüz yapmayın)

- [ ] Adım 3: Projeyi MySQL için yapılandır
- [ ] Adım 4: FTP ile dosyaları yükle
- [ ] Adım 5: SSH erişimi kontrol et
- [ ] Adım 6: Python/Django yapılandırması

---

## 🎯 ŞİMDİ NE YAPALIM?

**1. Veritabanı oluşturun (yukarıdaki Adım 1)**
**2. Veritabanı bilgilerini bana bildirin, sonraki adıma geçelim**

Ben projenizi MySQL/MariaDB için hazırlayacağım (PostgreSQL yerine).

---

**Veritabanını oluşturduktan sonra bana şunu söyleyin:**
- ✅ Veritabanı adı: `db_....`
- ✅ Kullanıcı adı: `db_....`
- ✅ Şifreyi belirlediniz mi? (güvenli bir şifre)

Hazır olduğunuzda bir sonraki adıma geçeceğiz! 🚀
