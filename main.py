import os
import logging
import logging.handlers


LOG_FILENAME = '/var/log/neuropost/neuropost.log'


handler = logging.handlers.RotatingFileHandler(
  LOG_FILENAME,
  maxBytes=10 * 1024 * 1024,
  backupCount=25,
  )


formatter = logging.Formatter(fmt='%(asctime)-15s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)


log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(handler)


log = logging.getLogger('neuropost')
log.info('Starting neuropost')


from flask import Flask
from database import db
from login_stuff import login_manager, oid
from urls import everything
from database import MYSQL_CONN
from sooper_sekrit import MYSQL_CONN_INFO, sekrit


TESTING = True


app = Flask(__name__)
app.secret_key = sekrit
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_CONN % MYSQL_CONN_INFO
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 60 * 60 # Once an hour.
app.debug = TESTING

db.init_app(app)
login_manager.setup_app(app)
oid.init_app(app)


for urls in everything:
  log.info('Mapping URLs')
  urls(app)
  log.info('Mapping URLs finished.')
