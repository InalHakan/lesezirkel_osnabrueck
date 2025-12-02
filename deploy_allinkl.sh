#!/bin/bash

# Deployment script for Lesezirkel Osnabrück on All-Inkl
# Bu script'i All-Inkl sunucusunda çalıştırın (SSH erişimi gerekli)

echo "🚀 Starting deployment for Lesezirkel Osnabrück..."

# Renklendirme
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Proje dizini
PROJECT_DIR="/www/htdocs/lesezirkel"  # All-Inkl'deki proje dizininizi buraya yazın
VENV_DIR="$PROJECT_DIR/venv"

# Proje dizinine git
cd $PROJECT_DIR || exit

echo -e "${YELLOW}1. Virtual environment kontrol ediliyor...${NC}"
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment oluşturuluyor..."
    python3 -m venv venv
fi

# Virtual environment'ı aktif et
source venv/bin/activate

echo -e "${YELLOW}2. Python paketleri kuruluyor...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${YELLOW}3. Veritabanı migration'ları çalıştırılıyor...${NC}"
python manage.py migrate --settings=lesezirkel_osnabrueck.settings_production

echo -e "${YELLOW}4. Static dosyalar toplanıyor...${NC}"
python manage.py collectstatic --noinput --settings=lesezirkel_osnabrueck.settings_production

echo -e "${YELLOW}5. Çeviri dosyaları derleniyor...${NC}"
python manage.py compilemessages --settings=lesezirkel_osnabrueck.settings_production

# Superuser oluştur (ilk deployment için)
echo -e "${YELLOW}6. Admin kullanıcısı kontrolü...${NC}"
echo "Admin kullanıcısı oluşturmak ister misiniz? (y/n)"
read -r create_admin
if [ "$create_admin" = "y" ]; then
    python manage.py createsuperuser --settings=lesezirkel_osnabrueck.settings_production
fi

# Log dizini oluştur
mkdir -p logs

# Dosya izinleri (All-Inkl için)
echo -e "${YELLOW}7. Dosya izinleri ayarlanıyor...${NC}"
chmod -R 755 media/
chmod -R 755 static/
chmod -R 755 logs/

echo -e "${GREEN}✅ Deployment tamamlandı!${NC}"
echo ""
echo "Sıradaki adımlar:"
echo "1. .env dosyasını kontrol edin"
echo "2. All-Inkl KAS panelinden Python uygulamanızı yapılandırın"
echo "3. Domain'i projeye bağlayın"
echo "4. SSL sertifikasını aktifleştirin"
echo ""
echo "Admin paneli: https://lz-os.de/admin/"
