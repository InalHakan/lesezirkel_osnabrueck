import shutil
import os
import zipfile
from pathlib import Path

# Kaynak ve hedef
source = Path('.')
deploy_dir = Path('deploy_package')
zip_name = 'lesezirkel_deployment.zip'

# Kopyalanmayacak dosya/klasörler
exclude = {
    '__pycache__', '.git', '.gitignore', '.venv', 'venv', 'env',
    '.env', '.env.local', '.env.production',
    'deploy_package', 'lesezirkel_deployment.zip',
    '.vscode', '.idea', 'logs',
    '.htaccess.fixed', 'check_deployment.py', 'create_deployment_zip.py',
    'lesezirkel_osnabrueck.sqlite3', 'db.sqlite3'
}

exclude_extensions = {'.pyc', '.pyo', '.pyd', '.sqlite3', '.db', '.log'}
exclude_startswith = {'ADIM_', '.'}

def should_exclude(path):
    name = path.name
    # Exclude listesi
    if name in exclude:
        return True
    # __pycache__ klasörleri
    if '__pycache__' in str(path):
        return True
    # Uzantılar
    if path.suffix in exclude_extensions:
        return True
    # Başlangıç kontrolleri (dosya kök dizinde ise)
    if path.parent == source:
        for prefix in exclude_startswith:
            if name.startswith(prefix) and name not in {'.htaccess'}:
                return True
    return False

print("🚀 Deployment paketi hazırlanıyor...")

# Deploy klasörünü temizle/oluştur
if deploy_dir.exists():
    shutil.rmtree(deploy_dir)
deploy_dir.mkdir()

# Dosyaları kopyala
copied_files = []
for item in source.rglob('*'):
    if item.is_file() and not should_exclude(item):
        rel_path = item.relative_to(source)
        dest_path = deploy_dir / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dest_path)
        copied_files.append(str(rel_path))

print(f"✅ {len(copied_files)} dosya kopyalandı")

# Boş klasörleri oluştur
for folder in ['media', 'logs', 'static']:
    (deploy_dir / folder).mkdir(exist_ok=True)
    
# .env.example oluştur
env_example = deploy_dir / '.env.example'
env_example.write_text("""DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DB_ENGINE=mysql
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306
DJANGO_SETTINGS_MODULE=lesezirkel_osnabrueck.settings_production
""", encoding='utf-8')

print("✅ .env.example oluşturuldu")

# ZIP oluştur
if os.path.exists(zip_name):
    os.remove(zip_name)
    
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for item in deploy_dir.rglob('*'):
        if item.is_file():
            arcname = item.relative_to(deploy_dir)
            zipf.write(item, arcname)

zip_size = os.path.getsize(zip_name) / 1024 / 1024
print(f"✅ ZIP oluşturuldu: {zip_name} ({zip_size:.2f} MB)")
print(f"✅ Klasör oluşturuldu: deploy_package/")
print("\n📦 Deployment paketi hazır!")
