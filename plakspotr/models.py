import logging
import sys
from datetime import datetime as dt
from flask_login import UserMixin

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


    is_authenticated = db.BooleanField()
        # """
        # This property should return True if the user is authenticated, i.e. they have provided valid credentials.
        #  (Only authenticated users will fulfill the criteria of login_required.)
        # """

    def is_active(self):
        """
        This property should return True if this is an active user - in addition to being authenticated,
        they also have activated their account, not been suspended, or any condition your application has for rejecting
        an account. Inactive accounts may not log in (without being forced of course).
        """

    @property
    def is_anonymous(self):
        """
        This property should return True if this is an anonymous user. (Actual users should return False instead.)

        :return: boolean
        """
        return True

    def get_id(self):
        """
        This method must return a unicode that uniquely identifies this user, and can be used to load the user from the
        user_loader callback. Note that this must be a unicode - if the ID is natively an int or some other type,
        you will need to convert it to unicode.
        """
        return unicode(self.id)


class Spot(db.Document):
    date_created = db.DateTimeField(default=dt.now)
    url = db.StringField()
    data = db.StringField()
    user = db.ReferenceField(User)