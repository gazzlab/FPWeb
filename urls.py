import json
from server import envey, lo, css, postload, JSON_convert_and_post_to_DB
from pages import home_page, login_page, logout_page, datapost
from site_css import site_default
from login_stuff import oidapp, db, RecordsYo


SITE_CSS_URL = '/static/site.css'


for page in (home_page, login_page, logout_page):
  page.setdefault('stylesheets', []).append(SITE_CSS_URL)


def urls(app):
  app.add('/', GET=envey(PAGE=home_page)(lo))
  post_loader = postload(JSON_convert_and_post_to_DB(RecordsYo, db))(lo)
  app.add('/datapost', POST=envey(PAGE=datapost)(post_loader))
  app.add(SITE_CSS_URL, GET=envey(CSS=site_default)(css))


def logins(app):
  loggy = envey(PAGES=(login_page, logout_page))(oidapp)
  app.add('/log|', GET=loggy, POST=loggy)


everything = [urls, logins]

