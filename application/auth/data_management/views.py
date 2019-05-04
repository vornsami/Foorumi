from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.auth.models import User
from application.auth.forms import NameForm, PasswordForm
from application.tasks.models import Thread
from application.tasks.functions import actives, inactives
      
@app.route("/userpage")
@login_required
def userpage():
    t = Thread.query.filter_by(account_id = current_user.id)
    
    return render_template("auth/userpage.html", threads = t, user = current_user, 
                               actives = actives(), inactives = inactives())

@app.route("/newname", methods = ["GET", "POST"])
@login_required
def newname():
    if request.method == "GET":
        return render_template("auth/newname.html", form = NameForm(), 
                               actives = actives(), inactives = inactives())
        
    form = NameForm(request.form)
    
    if not form.validate():
        return render_template("auth/newname.html", form = form,
                               error = "Invalid name", 
                               actives = actives(), inactives = inactives())
    
    user = User.query.filter_by(username=form.username.data).first()
    if user and not form.username.data == current_user.username:
        return render_template("auth/newname.html", form = form,
                               error = "Name already in use", 
                               actives = actives(), inactives = inactives())
                               
    user = User.query.filter_by(name=form.username.data).first()
    if user:
        return render_template("auth/newname.html", form = form,
                               error = "Name already in use", 
                               actives = actives(), inactives = inactives())
    
    current_user.name = form.username.data;
    db.session().commit()
    
    return redirect(url_for("userpage"))
    
@app.route("/newpassword", methods = ["GET", "POST"])
@login_required
def newpassword():
    if request.method == "GET":
        return render_template("auth/newpassword.html", form = PasswordForm(), 
                               actives = actives(), inactives = inactives())
        
    form = PasswordForm(request.form)
    
    if not form.validate():
        return render_template("auth/newpassword.html", form = form,
                               error = "Invalid password", 
                               actives = actives(), inactives = inactives())
                               
    current_user.password = form.password.data;
    db.session().commit()
    
    return redirect(url_for("userpage"))
    
@app.route("/deleteUser", methods = ["POST"])
@login_required
def deleteUser():
    
    t = Thread.query.filter_by(account_id = current_user.id)
    
    for thread in t:
        thread.account_id = 1
    db.session().commit()
    
    c = Thread.query.filter_by(account_id = current_user.id)
    
    for comment in c:
        comment.account_id = 1
    db.session().commit()
    
    db.session().delete(current_user)
    db.session().commit()
    
    return redirect(url_for("aloitus"))
    

    

