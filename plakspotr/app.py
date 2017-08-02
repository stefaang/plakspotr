import os
import json
from flask import Flask, current_app, render_template, request, session, redirect, url_for, jsonify, Blueprint
from flask_mongoengine import MongoEngine
from flask_oauthlib.client import OAuth
from flask_login import login_required

from .models import User, Spot
from . import db, oauth, lm

main = Blueprint('main', __name__)

#########


@lm.user_loader
def load_user(user_id):
    """ Login manager needs this to load users """
    return User.objects.get(id=user_id)


@main.route('/spot', methods=['POST'])
@login_required
def analyze_pic():
    url = data = analysis = None
    if 'image' in request.form:
        data = request.form['image']
        current_app.logger.info('Loaded image of %s bytes', len(data)*8);
    if 'analysis' in request.form and 'url' in request.form:
        analysis = request.form['analysis']
        current_app.logger.info('Got analysis: %s', analysis)
        url = request.form['url']
        current_app.logger.info('Got image url: %s', url)
    else:
        current_app.logger.info('No useful stuff in post :(')
        return
    # store the analysis in the db
    spot = Spot(user=session.get('user_id'), url=url, data=analysis)
    if spot.load_details():
        # analyze the score..
        prizes = spot.get_score_v1()
        spot.save()
        # todo: convert prices to score
        ret = json.dumps({'score': spot.score, 'prizes': prizes})
        current_app.logger.info('Spot loaded, returning %s', ret)
        return ret
    else:
        return 'NOK, no results found'


@main.route('/spots')
@login_required
def search_spots():
    return ''


@main.route('/spots/<code>')
@login_required
def view_spots(code):
    return redirect(url_for('main.view_spots_page', code=code, page=0))


@main.route('/spots/<code>/<page>')
@login_required
def view_spots_page(code, page=0):
    if not code.isalnum() or len(code) < 3:
        return 'Code should be alpha-numeric and at least 3 symbols'

    spots = Spot.objects(plate__icontains=code)
    current_app.logger.info('Found %s spots', spots.count())
    spots = reversed([spot.get_info() for spot in spots])

    return render_template('spots.html', username=session['username'], spots=spots)




if __name__ == "__main__":
    main.run()
