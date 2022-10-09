import datetime
from flask import Flask
from flask import render_template


app = Flask(__name__)

# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

# New functions
@app.route("/Relatorios/")
def reports():
    return render_template("reports.html")

@app.route("/tartarugometro/")
def tartarugometro():
    return render_template("tartarugometro.html")

@app.route("/controle-usuario/")
def users_control():
    return render_template("users_control.html")