import logging
import sys
import json
from datetime import datetime as dt
from flask_login import UserMixin

from constants import *


logger = logging.getLogger('root')

# in the application context, the db is already defined by flask_mongoengine
if 'db' in globals():
    logger.info('Database connection in application context')
# outside of the application, use mongoengine right away
else:
    import mongoengine
    logger.info('Connecting to database outside of application context')
    mongoengine.connect('plakspotr')
    db = mongoengine


class User(db.Document, UserMixin):
    name = db.StringField()
    email = db.StringField()
    gender = db.StringField()
    picture = db.StringField()
    google_id = db.StringField()

    date_created = db.DateTimeField(default=dt.now)
    date_modified = db.DateTimeField(default=dt.now)
    blacklist = db.ListField()
    whitelist = db.ListField()

    def load_data(self, data):
        self.name = data['name']
        self.google_id = data['id']
        self.email = data['email']
        self.picture = data.get('picture')
        self.gender = data.get('gender')
        self.save()


class Spot(db.Document):
    date_created = db.DateTimeField(default=dt.now)
    url = db.StringField()
    data = db.StringField()
    user = db.ReferenceField(User)
    plate = db.StringField()
    make = db.StringField()
    model = db.StringField()
    prizes = db.ListField()
    score = db.IntField(default=0)

    def get_info(self):
        d = json.loads(self.to_json())
        d['username'] = self.user.name
        d['date_created'] = self.date_created.strftime("%Y-%m-%d %H:%M:%S")
        logger.info('convert to mongo: %s', d)
        return d

    def load_details(self):
        try:
            data = json.loads(self.data)
        except ValueError:
            logger.warn('failed to load json data')
            return False
        results = data.get('results')
        if not results:
            logger.info('no results in data')
            return False
        result = results[0]
        self.plate = result.get('plate')
        vehicle = result.get('vehicle')
        if vehicle:
            self.make = vehicle.get('make')[0]['name']
            self.model = vehicle.get('make_model')[0]['name']
            self.color = vehicle.get('color')[0]['name']
        return True

    def get_score_v1(self):
        """ a new spot gets a list of prices, used to determine the score """
        prizes = ['BASE']

        # get other spots of this plate
        same_spots = Spot.objects(plate=self.plate)
        if same_spots:
            # check how many time we show up in the result
            my_same_spots = same_spots.filter(user=self.user)
            if my_same_spots:
                # this ain't the first time...
                # check cooldown to prevent boring cheaters
                prev_spot = my_same_spots[0]
                if self.date_created - prev_spot.date_created < COOLDOWN_PERIOD:
                    prizes = ['YOU_ARE_BORING']
                    return prizes
                if len(my_same_spots) == 1:
                    prizes += ['MY_SECOND_TIME']
                elif len(my_same_spots) == 2:
                    prizes += ['MY_THIRD_TIME']
            else:
                prizes.append('MY_FIRST_TIME')
        else:
            prizes.append('FIRST_TIME_EVER')

        my_spots = Spot.objects(user=self.user)

        return prizes