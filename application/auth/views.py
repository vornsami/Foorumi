from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm
from application.tasks.functions import actives, inactives

@app.route("/kirjaudu", methods = ["GET", "POST"])
def kirjaudu():

    if request.method == "GET":
        return render_template("auth/kirjaudu.html", form = LoginForm(), 
                               actives = actives(), inactives = inactives())
    
    form = LoginForm(request.form)
    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    
    if not user:
        return render_template("auth/kirjaudu.html", form = form,
                               error = "No such username or password", 
                               actives = actives(), inactives = inactives())
    print("Kayttaja " + user.name + " tunnistettiin")
    
    
    login_user(user)
    return redirect(url_for("aloitus"))    
    

@app.route("/uuskayttaja", methods = ["GET", "POST"])
def uuskayttaja():
    if request.method == "GET":
        return render_template("auth/uuskayttaja.html", form = LoginForm(), 
                               actives = actives(), inactives = inactives())
    
    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/uuskayttaja.html", form = form,
                               error = "Invalid username or password", 
                               actives = actives(), inactives = inactives())

    user = User.query.filter_by(username=form.username.data).first()
    if user:
        return render_template("auth/uuskayttaja.html", form = form,
                               error = "Username already in use", 
                               actives = actives(), inactives = inactives())
							   
    user = User.query.filter_by(name=form.username.data).first()
    if user:
        return render_template("auth/uuskayttaja.html", form = form,
                               error = "Username already in use", 
                               actives = actives(), inactives = inactives())
							   
    u = User(request.form.get("username"),request.form.get("username"),request.form.get("password"))
    u.acc_type = "USER"
    db.session().add(u)
    db.session().commit()
    
    return redirect(url_for("kirjaudu"))
    

@app.route("/kirjaaulos")
@login_required
def kirjaaulos():
    logout_user()
    return redirect(url_for("aloitus"))    
	

    

