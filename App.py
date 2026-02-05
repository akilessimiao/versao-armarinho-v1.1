from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
# Para hashes de senha: from werkzeug.security import generate_password_hash, check_password_hash
# Para PDF: from reportlab.pdfgen import canvas (instale reportlab)
# Para scheduler backups: import schedule, time (instale schedule)

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ccf821e9fb74b2a8e4e5e1c4e8f9a2b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_vendas.db'
db = SQLAlchemy(app)

# Models
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))  # Hasheada
    role = db.Column(db.String(20))  # 'admin' ou 'operador'

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    documento = db.Column(db.String(20))  # CPF/CNPJ
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    preco = db.Column(db.Float)
    estoque = db.Column(db.Integer)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Número de cupom
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    itens = db.Column(db.Text)  # JSON de itens
    total = db.Column(db.Float)
    status = db.Column(db.String(20), default='emitido')  # 'emitido' ou 'cancelado'

# Config Empresa (salva em BD ou arquivo)
class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_empresa = db.Column(db.String(100))
    documento_empresa = db.Column(db.String(20))  # CPF/CNPJ
    numero_admin_whatsapp = db.Column(db.String(20))
    api_pagamento = db.Column(db.Text)  # JSON com chaves API

# Criar BD
with app.app_context():
    db.create_all()
    # Usuários default (hasheie as senhas em produção)
    if not Usuario.query.first():
        db.session.add(Usuario(username='admin', password='admin', role='admin'))
        db.session.add(Usuario(username='operador', password='operador123', role='operador'))
        db.session.add(Config(id=1, nome_empresa='Sua Empresa', documento_empresa='00.000.000/0001-00', numero_admin_whatsapp='+5511999999999'))
        db.session.commit()

# Rotas
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:  # Use check_password_hash em prod
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        flash('Login inválido')
    return render_template('login.html')  # Crie HTML simples

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('dashboard.html', role=session['role'])  # Telas de vendas/admin

# Exemplo: Finalizar Venda e Gerar Cupom
@app.route('/venda/finalizar', methods=['POST'])
def finalizar_venda():
    # Lógica: Salvar venda, gerar cupom PDF/HTML com nome empresa só
    nova_venda = Venda(cliente_id=request.form['cliente_id'], itens=json.dumps(request.form['itens']), total=float(request.form['total']))
    db.session.add(nova_venda)
    db.session.commit()
    cupom_id = nova_venda.id
    # Gerar cupom (ex: texto simples por agora)
    config = Config.query.first()
    cupom_texto = f"Cupom {cupom_id} - {config.nome_empresa} ({config.documento_empresa})\nData: {nova_venda.data_hora}\nItens: {nova_venda.itens}\nTotal: R${nova_venda.total}"
    # Envio WhatsApp (integre Twilio aqui)
    # Sempre envia ao admin
    # Se cliente quiser: envie ao telefone do cliente
    # Opção impressão: Retorne HTML com print JS
    flash('Venda finalizada! Cupom enviado ao admin.')
    return redirect(url_for('dashboard'))

# Pesquisa Vendas
@app.route('/venda/pesquisar')
def pesquisar_venda():
    query = request.args.get('query')  # Por cupom, cliente ou data
    vendas = Venda.query.filter(  # Lógica de filtro: like para nome, == para id, between para data
        db.or_(Venda.id == query, Cliente.nome.like(f'%{query}%'), Venda.data_hora.like(f'%{query}%'))
    ).join(Cliente).all()
    return render_template('pesquisa.html', vendas=vendas)  # Exiba segunda via

# Cancelar Cupom
@app.route('/venda/cancelar/<int:id>', methods=['POST'])
def cancelar_venda(id):
    if session['role'] != 'admin' or request.form['senha'] != 'admin':  # Valide senha
        flash('Acesso negado')
        return redirect(url_for('dashboard'))
    venda = Venda.query.get(id)
    venda.status = 'cancelado'
    db.session.commit()
    # Re-gerar cupom com "CANCELADO" e reenviar ao admin via WhatsApp
    flash('Cupom cancelado e reenviado ao admin.')
    return redirect(url_for('dashboard'))

# Admin: Ajustar API Pagamentos
@app.route('/admin/ajustar_api', methods=['GET', 'POST'])
def ajustar_api():
    if session['role'] != 'admin': return redirect(url_for('login'))
    config = Config.query.first()
    if request.method == 'POST':
        api_data = json.dumps({
    'mercado_pago_token':   request.form.get('token', ''),
    'mercado_pago_public_key': request.form.get('public_key', ''),
    'pagseguro_token':      request.form.get('pagseguro_token', ''),
    # adicione mais campos aqui no futuro
})
        config.api_pagamento = api_data
        db.session.commit()
        flash('API ajustada!')
    return render_template('ajustar_api.html', config=config)

# Backup (exemplo manual)
@app.route('/admin/backup')
def backup():
    data = [row.__dict__ for row in Venda.query.all()]  # Expanda para todas tabelas
    with open('backup.json', 'w') as f:
        json.dump(data, f)
    flash('Backup criado!')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()  # Limpa tudo da sessão
    flash('Você saiu do sistema.', 'message')
    return redirect(url_for('login'))
# Para backups automáticos: Use schedule in a thread
# def run_scheduler():
#     schedule.every().day.at("23:00").do(backup)
#     while True: schedule.run_pending(); time.sleep(1)
# Inicie em thread no app.run

if __name__ == '__main__':
    app.run(debug=True)