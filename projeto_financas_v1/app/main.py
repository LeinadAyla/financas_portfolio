from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração com o novo driver Psycopg 3
# Note o '+psycopg' na string de conexão
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://dev_user:dev_password@localhost:5432/financas_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def home():
    return {
        "status": "online",
        "message": "Sistema de Finanças Pronto",
        "tecnologia": "Python 3.13 + Psycopg 3"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)