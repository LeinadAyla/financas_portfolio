from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configurações de conexão (Psycopg 3)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://dev_user:dev_password@localhost:5432/financas_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'uma_chave_muito_segura_2026'

db = SQLAlchemy(app)

# --- MODELOS DE DADOS (Multi-tenancy) ---

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) # Guardaremos Hash depois
    
    # Um utilizador pode ter várias transações
    transactions = db.relationship('Transaction', backref='owner', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'receita' ou 'despesa'
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # A CHAVE DO ISOLAMENTO (Multi-tenancy)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# --- INICIALIZAÇÃO DO BANCO ---

# Este comando cria as tabelas no Docker se elas não existirem
with app.app_context():
    db.create_all()
    print("🚀 Banco de dados PostgreSQL sincronizado e tabelas criadas!")

@app.route('/')
def home():
    return {
        "status": "online",
        "database": "conectado",
        "tabelas": ["users", "transactions"]
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)