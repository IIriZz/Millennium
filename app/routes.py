# -*- coding: utf-8 -*-
# app.py

from time import localtime, strftime
from werkzeug.security import generate_password_hash, check_password_hash

from flask import render_template, redirect, flash
from flask_socketio import send, join_room, leave_room
from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user
)

from app.forms import RegisterForm, LoginForm, EditForm
from app.models import User
from app import app, db, login_manager, ROOMS, socketio


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/main')
@login_required
def main_page():
    return render_template('base.html', username=current_user.username, rooms=ROOMS)


@app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.r_password.data:
            return render_template('register.html', form=form, message='Пароли не совпадают!')
        if db.session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message='Пользователь с таким '
                                                                       'электронным ящиком уже существует!')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(user)
        db.session.flush()
        db.session.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login/', methods=['post', 'get'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/main')
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/main')
        return render_template('login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect('/edit')
    else:
        form.about_me.data = current_user.about_me
    return render_template('edit.html',
        form=form)


@app.route('/user/<username>')
@login_required
def settings_page(username):
    user = db.session.query(User).filter(User.username == username).first()
    if current_user.username != username:
        return redirect('/main')
    if user == None:
        flash('User ' + username + ' not found.')
        return redirect('/main')
    posts = [
        { 'author': user, 'body': 'Test post #1' },
        { 'author': user, 'body': 'Test post #2' }
    ]
    return render_template('settings.html',
        user=user,
        posts=posts)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@socketio.on('incoming-msg')
def on_message(data):
    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    timestamp = strftime('%b-%d %H:%M', localtime())
    send({
        'msg': msg,
        'username': username,
        'time_stamp': timestamp,
    }, room=room)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send({'msg': f'{username} присоеденился к комнате {room}'}, room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send({'msg': f'{username} вышел из комнаты {room}'}, room=room)