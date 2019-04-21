from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, validators

class ThreadForm(FlaskForm):
    id = IntegerField("id")
    title = StringField("title", [validators.Length(min=5,max=144)])
    content = StringField("content", [validators.Length(min=5,max=1000)])
 
    class Meta:
        csrf = False

class CommentForm(FlaskForm):
    thread_id = StringField("thread_id")
    content = StringField("content", [validators.Length(min=1,max=1000)])
    class Meta:
        csrf = False