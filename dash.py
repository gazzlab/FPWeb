from flask import request, abort
from flask.ext.login import login_required, current_user
from templates import base
from database import (
  db,
  RecordsDat,
  RecordsMediTrain,
  RecordsTrainCat,
  RecordsMediTrainPre,
  RecordsMediTrainPost,
  RecordsMediTrainSleep,
  RecordsMediTrainSaliva,
  RecordsDATPre,
  RecordsDATPost,
  RecordAny,
  )
from login_stuff import require_role
from forms import ProfileForm


studyID_to_record_class = {
  'dat': RecordsDat,
  'meditrain': RecordsMediTrain,
  'traincat':RecordsTrainCat,
  'datpre':RecordsDATPre,
#  'datpost':RecordsDATPost,
  'meditrainpre':RecordsMediTrainPre,
  'meditrainpost':RecordsMediTrainPost,
  'meditrainsaliva':RecordsMediTrainSaliva,
  'meditrainsleep':RecordsMediTrainSleep,
  }


@login_required
@require_role('admin')
def dash():
  page = request.environ.get('PAGE', {})
  page['user'] = current_user
  page['db'] = db
  page['record_classes'] = [
    RecordsDat,
    RecordsMediTrain,
    RecordsTrainCat,
    RecordsDATPre,
    RecordsDATPost,
    RecordsMediTrainPre,
    RecordsMediTrainPost,
    RecordsMediTrainSleep,
    RecordsMediTrainSaliva,
    ]
  page['ra'] = RecordAny
  return str(base(**page))


@login_required
def study(studyID):
  rc = studyID_to_record_class.get(studyID.lower())
  if not rc:
    abort(404)
  page = request.environ.get('PAGE', {}).copy()
  page['user'] = current_user
  page['db'] = db
  page['record_class'] = rc
  page['studyID'] = rc.study_ID
  page['title'] = page['page_title'] = \
    page['title'].format(studyID=rc.study_ID)
  return str(base(**page))


@login_required
def profile():
  page = request.environ.get('PAGE', {})
  page['user'] = current_user
  page['db'] = db
  form_content = page['form_content']

  if request.method == 'POST':
    form = ProfileForm()
    if form.validate_on_submit():
      print 'Whooo!!'
    else:
      print 'Booo!!'
    form_content = str(form)

  html = str(base(**page))
  html = html.format(form_content=page['form_content'])
  return html
