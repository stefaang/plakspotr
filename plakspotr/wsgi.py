import os

from plakspotr import create_app

# Create an application instance that web servers can use. We store it as
# "application" (the wsgi default) and also the much shorter and convenient
# "app".
application = app = create_app(os.environ.get('PLAKSPOTR_CONFIG', 'production'))