from flask import render_template, flash, redirect, request, session
from app import app
from .forms import LoginForm
from flask import request
import requests


def input():
    return request.args.get('text')


@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
        title = 'Sign In',
        form = form)


@app.route('/friends_online')
def check_online_friends():
    user_ids = input()
    if user_ids == None:
        return render_template('login.html')
    param = {'user_ids': user_ids}
    id = requests.get('https://api.vk.com/method/users.get', params=param).json()
    if 'error' in id:
        return 'Ошибка'
    id = requests.get('https://api.vk.com/method/users.get', params=param).json()['response'][0]['uid']
    params = {'user_id': id, 'fields': 'online', 'version': '5.62'}
    friends = requests.get('https://api.vk.com/method/friends.get', params=params).json()['response']
    friends_online = []
    for friend in friends:
        if friend['online'] == 1:
            friends_online.append(friend)
    return render_template('friends_online.html', friends=friends_online)


def errors(error_code):
    if error_code == 6:
        return 'Слишком много запросов'
    if error_code == 8:
        return 'Неверный запрос'
    if error_code == 15:
        return 'Доступ запрещен'
    if error_code == 200:
        return 'Доступ запрещен'



