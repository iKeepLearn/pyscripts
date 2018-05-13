# -*- coding:utf-8 -*-
from flask import render_template,flash,url_for
from app import app
from app.forms import urlForm

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
    form = urlForm()
    return render_template('index.html',title='htaccess Online Spider Demo',form=form)
