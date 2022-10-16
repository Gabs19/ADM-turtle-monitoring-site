import email
from webbrowser import get
from flask import Flask, session
from flask import render_template, request, redirect, session
import service

app = Flask(__name__)

app.secret_key = 'secret'

# Replace the existing home function with the one below
@app.route("/")
def home():
    if('user' in session):
        return render_template("home.html")
    else:
        return redirect('/login')


@app.route("/login/", methods=['POST', 'GET'])
def login():
    if('user' in session):
        return 'Hi, {}'.format(session['user'])
    if request.method == 'POST':
        email = request.form.get('email')
        password = str(request.form.get('password'))
        try:
            user = service.auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect('/')
        except:
            return 'Falha ao tentar entrar...'
    return render_template("login.html")


@app.route("/logout/")
def logout():
    session.pop('user')
    return redirect('/login')


# New functions
@app.route("/Relatorios/")
def reports():
    reports = service.db.child('names').get()
    report = reports.val()
    return render_template("reports.html", values=report.values())

@app.route("/tartarugometro/")
def tartarugometro():
    return render_template("tartarugometro.html")

@app.route("/controle-usuario/", methods=['POST', 'GET'] )
def users_control():
    if('user' in session):
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get(str('password'))
            try:
                user = service.auth.create_user_with_email_and_password(email,password)
                service.db.child('users').generate_key(service.auth.get_account_info(user['idToken'])).push({"email" : email})
                return redirect('/')
            except:
                return 'Falha ao cadastrar novo usuario'
    else:
        return redirect('/login')
    return render_template("users_control.html")