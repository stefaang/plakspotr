import os
from flask import Flask, current_app, render_template, request, session, redirect, url_for, jsonify
from flask_mongoengine import MongoEngine
from flask_oauthlib.client import OAuth
from flask_login import LoginManager, login_required, login_user, logout_user

from config import cfgs


db = MongoEngine()
oauth = OAuth()
lm = LoginManager()


def create_app(config_name):
    from models import User

    app = Flask(__name__)
    app.config.from_object(cfgs[config_name])

    db.init_app(app)
    oauth.init_app(app)
    lm.init_app(app)
    lm.login_view = 'login'

    # TODO: refactor login to a blueprint
    google = oauth.remote_app(
        'google',
        consumer_key=app.config.get('GOOGLE_ID'),
        consumer_secret=app.config.get('GOOGLE_SECRET'),
        request_token_params={
            'scope': 'email'
        },
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
    )

    @google.tokengetter
    def get_google_oauth_token():
        return session.get('google_token')

    @app.route('/')
    def index():
        if 'google_token' in session:
            me = google.get('userinfo')
            if u'error' in me.data:
                return redirect(url_for('.logout'))
            #return jsonify({"data": me.data})
            app.logger.info('User login: %s', me.data)
            user = User.objects(email=me.data[u'email'])
            if not user:
                user = User()
                user.load_data(me.data)
            else:
                user = user.first()
            login_user(user)
            session['username'] = user.name
            return render_template('home.html', username=user.name)
        # TODO: proper login page
        return render_template('index.html')

    @app.route('/login')
    def login():
        return google.authorize(callback=url_for('.authorized', _external=True))

    @app.route('/logout')
    #@login_required
    def logout():
        session.pop('google_token', None)
        session.pop('username', None)
        logout_user()
        return redirect(url_for('.index'))

    @app.route('/login/authorized')
    def authorized():
        resp = google.authorized_response()
        app.logger.info('Auth resp: %s', resp)
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        session['google_token'] = (resp['access_token'], '')
        return redirect(url_for('.index'))

    # add the other functions as in a blueprint

    from .app import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app