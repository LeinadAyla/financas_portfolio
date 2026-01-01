from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# --- FILTRO PERSONALIZADO PARA MOEDA BRASILEIRA (BRL) ---
@app.template_filter('format_brl')
def format_brl(value):
    try:
        # Formata: 1234.5 -> 1.234,50
        # O replace garante a inversão de padrões americanos para brasileiros
        return "{:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "0,00"

# Configurações
app.config['SECRET_KEY'] = 'uma_chave_muito_segura_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://dev_user:dev_password@localhost:5432/financas_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELOS ---
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    transactions = db.relationship('Transaction', backref='owner', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'entrada' ou 'saida'
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Budget(db.Model):
    __tablename__ = 'budgets'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    limit_value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- ROTAS ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if 'description' in request.form:
            desc = request.form.get('description')
            val = float(request.form.get('value') or 0)
            t_type = request.form.get('type')
            new_t = Transaction(description=desc, value=val, type=t_type, owner=current_user)
            db.session.add(new_t)
        elif 'limit_value' in request.form:
            limit = float(request.form.get('limit_value') or 0)
            existing_budget = Budget.query.filter_by(user_id=current_user.id).first()
            if existing_budget:
                existing_budget.limit_value = limit
            else:
                new_budget = Budget(category='Geral', limit_value=limit, user_id=current_user.id)
                db.session.add(new_budget)
        
        db.session.commit()
        return redirect(url_for('home'))

    # Lógica de Busca e Filtro
    search_query = request.args.get('search', '')
    filter_month = request.args.get('month', '')

    query = Transaction.query.filter_by(user_id=current_user.id)

    if search_query:
        query = query.filter(Transaction.description.ilike(f'%{search_query}%'))
    
    if filter_month == 'current':
        curr_month = datetime.utcnow().month
        curr_year = datetime.utcnow().year
        query = query.filter(db.extract('month', Transaction.date) == curr_month,
                             db.extract('year', Transaction.date) == curr_year)

    user_transactions = query.order_by(Transaction.date.desc()).all()
    budget = Budget.query.filter_by(user_id=current_user.id).first()
    
    total_entrada = sum(t.value for t in user_transactions if t.type == 'entrada')
    total_saida = sum(t.value for t in user_transactions if t.type == 'saida')
    saldo = total_entrada - total_saida

    progresso = 0
    if budget and budget.limit_value > 0:
        progresso = (total_saida / budget.limit_value) * 100

    return render_template('dashboard.html', 
                           transactions=user_transactions, 
                           saldo=saldo, 
                           budget=budget, 
                           total_entrada=total_entrada,
                           total_saida=total_saida,
                           progresso=progresso,
                           search_query=search_query)

@app.route('/delete/<int:id>')
@login_required
def delete_transaction(id):
    t = db.session.get(Transaction, id)
    if t and t.user_id == current_user.id:
        db.session.delete(t)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_input = request.form['username']
        pwd_input = request.form['password']
        hash_pwd = generate_password_hash(pwd_input)
        new_user = User(username=user_input, password=hash_pwd)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash("Erro: Usuário já existe!")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form['username']
        pwd_input = request.form['password']
        user = User.query.filter_by(username=user_input).first()
        if user and check_password_hash(user.password, pwd_input):
            login_user(user)
            return redirect(url_for('home'))
        flash('Credenciais inválidas!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- TRATAMENTO DE ERROS ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)