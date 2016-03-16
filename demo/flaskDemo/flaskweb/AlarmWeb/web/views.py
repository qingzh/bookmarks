
from flask import Flask, Blueprint

MAINPATH = "sm"
app = Flask(MAINPATH, static_url_path="/%s/static" % MAINPATH)


from .blueprints import alarm
 
app.register_blueprint(alarm, url_prefix='/%s/alarm' % MAINPATH)

app.debug = True
logger = app.logger
logger.debug(app.url_map)

