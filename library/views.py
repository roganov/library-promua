from flask import render_template, url_for, redirect, request
from flask.ext.login import login_user, logout_user, login_required

from app import app, login_manager

from .forms import LoginForm


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user, remember=form.remember.data)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(request.args.get('next') or url_for('index'))
