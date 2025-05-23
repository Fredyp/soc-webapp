#!/bin/bash

echo "✅ Paso 1: Actualizando el sistema..."
sudo apt update && sudo apt upgrade -y

echo "📦 Paso 2: Instalando dependencias del sistema..."
sudo apt install -y python3 python3-venv python3-pip git curl build-essential libssl-dev libffi-dev \
                    libxrender1 libfontconfig1 libx11-dev libjpeg-dev libpng-dev

echo "📥 Paso 3: Descargando wkhtmltopdf..."
cd /tmp
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb

echo "📦 Paso 4: Instalando wkhtmltopdf..."
sudo apt install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb

echo "📁 Paso 5: Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Paso 6: Instalando requerimientos de Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗃️ Paso 7: Creando base de datos..."
python3 -c \"from app import db; db.create_all()\"

echo "🚀 Paso 8: Ejecutando servidor Flask..."
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000