from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.tasks.models import Thread, Comment
from application.tasks.forms import ThreadForm, CommentForm
from application.tasks.functions import actives, inactives, idSort
from application.auth.models import User

@app.route("/newthread", methods = ["GET", "POST"])
@login_required
def newthread():
    if request.method == "GET":
        return render_template("newthread.html", form = ThreadForm(request.form), 
                               actives = actives(), inactives = inactives())
    
    form = ThreadForm(request.form)
    
    if not form.validate():
        return render_template("newthread.html", form = form,
                               error = "Title or content is invalid", 
                               actives = actives(), inactives = inactives())
    
    thread = Thread(request.form.get("title"), request.form.get("content"))
    thread.account_id = current_user.id
    db.session().add(thread)
    db.session().commit()
    
    return redirect(url_for("aloitus"))
    
@app.route("/thread", methods = ["POST"])
def lanka():
    t = Thread.query.filter_by(id=request.form.get("thread_id")).first()
    c = Comment.query.filter_by(thread_id=request.form.get("thread_id"))
    return render_template("thread.html", thread = t, comments = c, User = User, 
                               actives = actives(), inactives = inactives())
    
@app.route("/comment", methods = ["POST"])
def kommentoi():
    
    form = CommentForm(request.form)
    
    if not form.validate():
        return redirect(url_for("aloitus"))
    
    t = Thread.query.filter_by(id=request.form.get("thread_id")).first()
    comment = Comment(request.form.get("content"))
    comment.thread_id = t.id
    comment.account_id = current_user.id
    
    db.session().add(comment)
    db.session().commit()
    return redirect(url_for("aloitus"))
   
    
@app.route("/search", methods = ["POST"])
def etsi():

    t = Thread.query.filter(Thread.title.contains(request.form.get("search"))).all()
    
    if request.form.get("order") == "descending":
        t.sort(key=idSort,reverse=True)
    else:
	    t.sort(key=idSort,reverse=False)
    
    return render_template("search.html", threads = t, term = request.form.get("search"), 
                               actives = actives(), inactives = inactives())
    
    
    