import threading
import time

from flask import Flask
from flask import render_template, request, redirect, session
from service import service
import pandas as pd
from util import data_eclosao

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
@app.route("/Relatorios/", methods=['POST','GET'])
def reports():
    if request.method == "POST":
        data = request.form.get('report')
        all_reports = service.db.child('ninhos-localizações').get().val()
        reports = all_reports.values()

        for report in reports:
            if data == report['nomeMarcador']:
                return render_template("reports.html", values=[report])

        return render_template("reports.html", values=None)

    else:
        reports = service.db.child('ninhos-localizações').order_by_key().limit_to_last(6).get()
        report = reports.val()

        return render_template("reports.html", values=report.values())

@app.route("/generate/<string:id>/", methods=['POST', 'GET'])
def generate_csv(id):
    idtoken = service.db.child('ninhos-localizações').get()

    for id_reports in idtoken.val().values():
        if id_reports['id'] == id:
            id_report = id_reports

            df = pd.DataFrame(list(id_report.items()),columns = ['Dados Gerais', 'Valores coletados'])
            print(df)
            print(type(df))

            writer = pd.ExcelWriter(f'reports/{id_report["id"].replace(":","_")}.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', index=False)

            worksheet = writer.sheets['Sheet1']  # pull worksheet object
            for idx, col in enumerate(df):  # loop through all columns
                series = df[col]
                max_len = max((
                    series.astype(str).map(len).max(),  # len of largest item
                    len(str(series.name))  # len of column name/header
                )) + 1  # adding a little extra space
                worksheet.set_column(idx, idx, max_len)

            writer.close()

        else:
            print('next report')

    return redirect('/Relatorios')


@app.route("/tartarugometro/")
def tartarugometro():
    return render_template("tartarugometro.html")


@app.route("/controle-usuario/", methods=['POST', 'GET'])
def users_control():
    if 'user' in session:
        if request.method == 'POST':
            nome = request.form.get('nome')
            email = request.form.get('email')
            password = request.form.get(str('password'))
            try:
                user = service.auth.create_user_with_email_and_password(email, password)
                service.db.child('users').child(user['localId']).set({'email': email, 'nome': nome, 'id': user['localId'], 'idtoken': user['idToken']})
            except:
                return 'Falha ao cadastrar novo usuario'
    else:
        return redirect('/login')

    users = service.db.child('users').get()
    read_user = users.val()

    if read_user is not None:
        return render_template("users_control.html", values=read_user.values())
    else:
        return render_template('users_control.html')

@app.route("/delete/<string:id>/", methods=['POST', 'GET'])
def delete_user(id):
    idToken = service.db.child('users').child(id).get()
    token = idToken.val()

    service.db.child('users').child(id).remove()
    service.auth.delete_user_account(token['idtoken'])

    return redirect('/controle-usuario/')

def web():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    threading.Thread(target=web, daemon=True).start()
    threading.Thread(target=data_eclosao.readingDates(),daemon=True).start()

