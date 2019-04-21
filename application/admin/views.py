from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.tasks.models import Thread, Comment


@app.route("/removethread", methods = ["POST"])
@login_required(role="ADMIN")
def removethread():

    t = Thread.query.filter_by(id=request.form.get("thread_id")).first()
    
    db.session().delete(t)
    db.session().commit()
    
    comments = Comment.query.filter_by(thread_id=request.form.get("thread_id"))
    
    for comment in comments:
        db.session().delete(comment)
    db.session().commit()
    
    return redirect(url_for("aloitus"))