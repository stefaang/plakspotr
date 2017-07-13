import os
from flask import Flask, current_app, render_template, request, session, redirect, url_for, jsonify, Blueprint
from flask_mongoengine import MongoEngine
from flask_oauthlib.client import OAuth

from .models import User
from . import db, oauth, lm

main = Blueprint('main', __name__)

#########


@lm.user_loader
def load_user(user_id):
    """ Login manager needs this to load users """
    return User.get(user_id)



# @app.route('/')
# def hello_world():
#     return render_template('index.html')


@main.route('/spot', methods=['POST'])
def analyze_pic():
    if 'data' in request.form:
        data = request.form['data']
        main.logger.info(data)
    elif 'url' in request.form:
        url = request.form['url']
        main.logger.info('Got imgur url: %s', url)
    else:
        main.logger.info('No data, no url in post :(')
    return 'OK'


@main.route('/spots/<code>')
def show_spots(code):
    return render_template('index.html')

if __name__ == "__main__":
    main.run()


