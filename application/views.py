from flask import Flask, render_template,request

from application import app, db
from application.tasks.models import Thread
from application.tasks.forms import ThreadForm
from application.tasks.functions import idSort
from application.tasks.functions import actives, inactives

@app.route("/")
def aloitus():
    t = Thread.query.all()
    t.sort(key=idSort,reverse=True)
    
    return render_template("aloitus.html", threads = t, actives = actives(), inactives = inactives())

