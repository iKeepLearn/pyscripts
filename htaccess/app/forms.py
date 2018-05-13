# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField
from wtforms.validators import DataRequired,URL

class urlForm(FlaskForm):
    url = TextField('',validators=[DataRequired(),URL(require_tld=True,message="请输入正确的网页地址")])
    submit = SubmitField('抓取')
