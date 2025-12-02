#!/usr/bin/env python3
"""
All-Inkl Deployment Kontrol Script'i
Bu script deployment öncesi kontrolleri yapar
"""

import os
import sys
from pathlib import Path

# Renkli çıktı için
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def check_file_exists(file_path, description):
    """Dosya varlığını kontrol eder"""
    if os.path.exists(file_path):
        print_success(f"{description}: {file_path}")
        return True
    else:
        print_error(f"{description} bulunamadı: {file_path}")
        return False

def check_env_example():
    """Environment example dosyasını kontrol eder"""
    print_header("Environment Dosyaları Kontrolü")
    
    if check_file_exists('.env.example', '.env.example şablon dosyası'):
        print_warning("Sunucuda .env dosyası oluşturmayı unutmayın!")
    
    if os.path.exists('.env'):
        print_warning(".env dosyası mevcut - Git'e eklenmemiş olmalı")
        # .gitignore kontrolü
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                if '.env' in f.read():
                    print_success(".env dosyası .gitignore'da")
                else:
                    print_error(".env dosyası .gitignore'a eklenmeli!")

def check_required_files():
    """Gerekli dosyaları kontrol eder"""
    print_header("Gerekli Dosyalar Kontrolü")
    
    required_files = {
        'manage.py': 'Django management script',
        'requirements.txt': 'Python dependencies',
        'passenger_wsgi.py': 'WSGI entry point (All-Inkl)',
        '.htaccess': 'Apache config (All-Inkl)',
        'deploy_allinkl.sh': 'Deployment script',
        'lesezirkel_osnabrueck/settings.py': 'Django settings',
        'lesezirkel_osnabrueck/settings_production.py': 'Production settings',
        'lesezirkel_osnabrueck/wsgi.py': 'WSGI application',
    }
    
    all_exist = True
    for file_path, description in required_files.items():
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_documentation():
    """Dokümantasyon dosyalarını kontrol eder"""
    print_header("Dokümantasyon Kontrolü")
    
    docs = {
        'DEPLOYMENT_ALLINKL.md': 'Detaylı deployment rehberi',
        'QUICKSTART_ALLINKL.md': 'Hızlı başlangıç rehberi',
        'CHANGES_FOR_ALLINKL.md': 'Değişiklik özeti',
        'README.md': 'Proje README',
    }
    
    for doc, description in docs.items():
        check_file_exists(doc, description)

def check_requirements():
    """requirements.txt içeriğini kontrol eder"""
    print_header("Python Paketleri Kontrolü")
    
    if not os.path.exists('requirements.txt'):
        print_error("requirements.txt bulunamadı!")
        return
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
        
    required_packages = [
        'Django',
        'psycopg2-binary',
        'gunicorn',
        'whitenoise',
        'python-decouple',
        'Pillow',
    ]
    
    for package in required_packages:
        if package.lower() in content.lower():
            print_success(f"{package} paket listesinde")
        else:
            print_warning(f"{package} paket listesinde YOK")

def check_settings_production():
    """Production settings dosyasını kontrol eder"""
    print_header("Production Settings Kontrolü")
    
    settings_file = 'lesezirkel_osnabrueck/settings_production.py'
    if not os.path.exists(settings_file):
        print_error(f"{settings_file} bulunamadı!")
        return
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    checks = {
        'DEBUG = False': 'DEBUG kapalı',
        'lesezirkel-os.de': 'Domain ayarlanmış',
        'decouple': 'Environment variable desteği',
        'ALLOWED_HOSTS': 'Allowed hosts tanımlı',
        'DATABASES': 'Veritabanı ayarları',
    }
    
    for check, description in checks.items():
        if check in content:
            print_success(description)
        else:
            print_warning(f"{description} bulunamadı")

def check_gitignore():
    """gitignore dosyasını kontrol eder"""
    print_header(".gitignore Kontrolü")
    
    if not os.path.exists('.gitignore'):
        print_error(".gitignore bulunamadı!")
        return
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    important_ignores = [
        '.env',
        '__pycache__',
        '*.pyc',
        'venv/',
        '*.sqlite3',
        'staticfiles/',
        '*.log',
    ]
    
    for item in important_ignores:
        if item in content:
            print_success(f"{item} ignore ediliyor")
        else:
            print_warning(f"{item} ignore listesinde YOK")

def print_deployment_checklist():
    """Deployment checklist'i yazdırır"""
    print_header("Deployment Checklist")
    
    checklist = [
        "All-Inkl KAS panelinde PostgreSQL/MySQL veritabanı oluştur",
        "Veritabanı bilgilerini not et (DB_NAME, DB_USER, DB_PASSWORD)",
        "FTP ile dosyaları sunucuya yükle (.venv ve __pycache__ hariç)",
        "SSH ile sunucuya bağlan",
        ".env dosyası oluştur ve doldur",
        "Secret key oluştur ve .env'e ekle",
        "Virtual environment kur: python3 -m venv venv",
        "source venv/bin/activate",
        "pip install -r requirements.txt",
        "python manage.py migrate --settings=lesezirkel_osnabrueck.settings_production",
        "python manage.py collectstatic --noinput --settings=lesezirkel_osnabrueck.settings_production",
        "python manage.py createsuperuser --settings=lesezirkel_osnabrueck.settings_production",
        "chmod -R 755 media/ static/ logs/",
        "All-Inkl KAS panelinde Python app yapılandır",
        "Domain bağla",
        "SSL sertifikası aktifleştir",
        "https://lesezirkel-os.de test et",
        "https://lesezirkel-os.de/admin/ test et",
    ]
    
    for i, item in enumerate(checklist, 1):
        print(f"{Colors.YELLOW}{i:2d}.{Colors.END} [ ] {item}")
    
    print(f"\n{Colors.BOLD}Detaylar için:{Colors.END}")
    print(f"  - Hızlı başlangıç: {Colors.GREEN}QUICKSTART_ALLINKL.md{Colors.END}")
    print(f"  - Detaylı rehber:  {Colors.GREEN}DEPLOYMENT_ALLINKL.md{Colors.END}")
    print(f"  - Değişiklikler:   {Colors.GREEN}CHANGES_FOR_ALLINKL.md{Colors.END}")

def main():
    """Ana fonksiyon"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║       All-Inkl Deployment Ön Kontrol Script'i            ║")
    print("║       Lesezirkel Osnabrück e.V.                          ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    # Proje kök dizininde mi kontrol et
    if not os.path.exists('manage.py'):
        print_error("Bu script proje kök dizininde çalıştırılmalı!")
        sys.exit(1)
    
    # Kontroller
    check_required_files()
    check_documentation()
    check_env_example()
    check_requirements()
    check_settings_production()
    check_gitignore()
    print_deployment_checklist()
    
    print_header("Sonuç")
    print(f"{Colors.GREEN}Projeniz All-Inkl'de yayınlanmaya hazır!{Colors.END}")
    print(f"\n{Colors.YELLOW}Sonraki adım:{Colors.END} QUICKSTART_ALLINKL.md dosyasını okuyun\n")

if __name__ == '__main__':
    main()
