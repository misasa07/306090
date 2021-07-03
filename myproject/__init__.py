import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
############################################################################
############ CONFIGURATIONS (CAN BE SEPARATE CONFIG.PY FILE) ###############
###########################################################################

# Remember you need to set your environment variables at the command line
# when you deploy this to a real website.
# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret
app.config['SECRET_KEY'] = 'mysecret'

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

from myproject.core.views import core
from myproject.users.views import users
from myproject.tasks.views import tasks
from myproject.error_pages.handlers import error_pages

# Register the apps
app.register_blueprint(users)
app.register_blueprint(tasks)
app.register_blueprint(core)
app.register_blueprint(error_pages)
