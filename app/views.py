from flask import render_template, flash, redirect, request, session
from app import app
from .forms import LoginForm
from flask import request
import requests


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
        title='Check VK Friends',
        form=form)


def user_id_input():
    return request.args.get('text')#id may be in text format


def get_id_in_number_format():
    user_ids = user_id_input()
    param = {'user_ids': user_ids}
    id = requests.get('https://api.vk.com/method/users.get', params=param).json()
    if 'error' in id:
        error_code = id['error']['error_code']
        error = errors(error_code)
        return render_template('index.html', error=error)
    id = requests.get('https://api.vk.com/method/users.get', params=param).json()['response'][0]['uid']
    return id


@app.route('/friends_online')
def check_online_friends():
    user_ids = user_id_input()
    param = {'user_ids': user_ids}
    id = requests.get('https://api.vk.com/method/users.get', params=param).json()
    if 'error' in id:
        error_code = id['error']['error_code']
        error = errors(error_code)
        return render_template('login.html', error=error)
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
        return 'Too many requests'
    if error_code == 113:
        return 'Invalid input'
    if error_code == 15:
        return 'Access closed'
    if error_code == 200:
        return 'Access closed'




