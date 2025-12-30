#!/bin/bash

# =================================================================
# Script de Setup Automatizado - Sistema de Finanças Multi-tenancy
# Autor: Seu Nome (Candidato a Eng. de Software)
# Objetivo: Padronizar o ambiente de desenvolvimento e deploy.
# =================================================================

PROJECT_DIR="projeto_financas_v1"

echo "----------------------------------------------------------"
echo "🚀 Iniciando Deploy do Ambiente de Desenvolvimento"
echo "----------------------------------------------------------"

# 1. Criação da Estrutura de Pastas (Padrão MVC simples)
mkdir -p $PROJECT_DIR/{app,templates,static,docker,docs}

# 2. Criação do Ambiente Virtual (Virtualenv)
echo "📦 Configurando isolamento de dependências (venv)..."
python3 -m venv $PROJECT_DIR/venv

# 3. Criação do Docker Compose (Infraestrutura como Código)
echo "🐳 Configurando Docker para PostgreSQL..."
cat <<EOF > $PROJECT_DIR/docker-compose.yml
version: '3.8'
services:
    db:
        image: postgres:15
        container_name: fin_db_prod
        environment:
            - POSTGRES_DB=financas_db
            - POSTGRES_USER=dev_user
            - POSTGRES_PASSWORD=dev_password
        ports:
            - "5432:5432"
        volumes:
            - ./docker/db_data:/var/lib/postgresql/data
EOF

# 4. Criação do arquivo de dependências (Crucial para recrutadores)
echo "📝 Gerando requirements.txt..."
cat <<EOF > $PROJECT_DIR/requirements.txt
flask==3.0.0
flask-sqlalchemy==3.1.1
flask-login==0.6.3
psycopg2-binary==2.9.9
EOF

# 5. Código Inicial da Aplicação (Tab Size 4)
echo "🐍 Gerando boilerplate da aplicação..."
cat <<EOF > $PROJECT_DIR/app/main.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dev_user:dev_password@localhost:5432/financas_db'

@app.route('/')
def home():
    return {"status": "online", "message": "Sistema de Finanças Pronto"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF

echo "----------------------------------------------------------"
echo "✅ Setup concluído com sucesso!"
echo "Instruções para o Recrutador:"
echo "1. Entre na pasta: cd $PROJECT_DIR"
echo "2. Suba o banco: docker-compose up -d"
echo "3. Instale dependências: pip install -r requirements.txt"
echo "4. Rode o app: python app/main.py"
echo "----------------------------------------------------------"