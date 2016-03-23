#! -*- coding:utf8 -*-)

from .views import app
import flask_admin as admin

from models import db, User, Group, RelGroupUser
from modelviews import *

SQLITE_ADDR = "sqlite:////home/monitor/db/"

# Create database
app.config[
    'SQLALCHEMY_DATABASE_URI'] = SQLITE_ADDR + 'monitor.db'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

# Create admin
admin = admin.Admin(
    app, url='/admin', name='Monitor后台管理', template_mode='bootstrap3')

admin.add_view(UserView(User, db.session))
admin.add_view(GroupView(Group, db.session))
admin.add_view(RelGroupUserView(RelGroupUser, db.session))


def init_db():
    # Create DB
    with app.app_context():
        db.create_all()

