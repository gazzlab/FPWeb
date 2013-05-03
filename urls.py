import json
from server import envey, lo, css, postload, JSON_convert_and_process
from pages import (
  home_page,
  login_page,
  logout_page,
  datapost,
  main_page,
  study_page,
  profile_page,
  )
from site_css import site_default
from database import (
  db,
  RecordAny,
  RecordsDat,
  RecordsMediTrain,
  RecordsTrainCat,
  )
from login_stuff import login, logout
from dash import dash, study, studyID_to_record_class, profile


SITE_CSS_URL = '/static/site.css'


for page in (home_page, login_page, logout_page, main_page, study_page,
             profile_page):
  page.setdefault('stylesheets', []).append(SITE_CSS_URL)


def process_batch(data):
  studyID = data['studyID']
  record_class = studyID_to_record_class.get(studyID.lower())
  if record_class is None:
    def record_class(subjectID=data['subjectID'], **e):
      return RecordAny(
        studyID=studyID,
        subjectID=subjectID,
        raw_data=repr(e),
        )
  for record in data['data']:
    record = record_class(**record)
    db.session.add(record)
  db.session.commit()
  return repr(data)


def urls(app):
  app.add_url_rule(SITE_CSS_URL, 'css', envey(CSS=site_default)(css))
  app.add_url_rule('/', 'index', (envey(PAGE=home_page)(lo)))

  post_loader = postload(JSON_convert_and_process(process_batch))(lo)
  post_loader = envey(PAGE=datapost)(post_loader)
  post_loader.methods = ['POST']
  app.add_url_rule('/datapost', 'datapost', post_loader)

  app.add_url_rule('/dash', 'dash', envey(PAGE=main_page)(dash))

  app.add_url_rule('/study/<studyID>', 'study', envey(PAGE=study_page)(study))

  pro = envey(PAGE=profile_page)(profile)
  pro.methods = ['GET', 'POST']
  app.add_url_rule('/profile', 'profile', pro)


def logins(app):
  logy = envey(PAGE=login_page)(login)
  logy.methods = ['GET', 'POST']
  app.add_url_rule('/login', 'login', logy)
  logy = envey(PAGE=logout_page)(logout)
  logy.methods = ['GET', 'POST']
  app.add_url_rule('/logout', 'logout', logy)


everything = [urls, logins]
