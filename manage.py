import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0].strip()] = var[1].strip()



from plakspotr import create_app, db
from plakspotr.models import User, Spot
from flask_script import Manager, Shell


app = create_app(os.getenv('PLAKSPOTR_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def cleandb():
    # db.drop_collection('user')
    User.objects.delete()

if __name__ == "__main__":
    manager.run()
