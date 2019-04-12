import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    with open('.env') as fp:
        for line in fp
            if line.startswith('#'):
                continue
            k,v = line.strip().split('=', 1)
            os.environ[k.strip()] = v.strip()

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
