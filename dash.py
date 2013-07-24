from StringIO import StringIO
from csv import writer
from flask import request, abort, Response
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
  RecordsLeapDat,
  RecordAny,
  get_field_names,
  )
from login_stuff import require_role
from forms import ProfileForm


studyID_to_record_class = {
  'dat': RecordsDat,
  'meditrain': RecordsMediTrain,
  'traincat':RecordsTrainCat,
  'datpre':RecordsDATPre,
  'datpost':RecordsDATPost,
  'meditrainpre':RecordsMediTrainPre,
  'meditrainpost':RecordsMediTrainPost,
  'meditrainsaliva':RecordsMediTrainSaliva,
  'meditrainsleep':RecordsMediTrainSleep,
  'LeapDAT':RecordsLeapDat,
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
    RecordsLeapDat
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
  page['record_fields'] = get_field_names(rc)
  page['studyID'] = rc.study_ID
  page['title'] = page['page_title'] = \
    page['title'].format(studyID=rc.study_ID)
  return str(base(**page))


def get_fields(record_class):
  try:
    fm = record_class.field_map
  except AttributeError:
    fields = get_field_names(record_class)
  else:
    fields = fm.values()
  if 'subjectID' not in fields:
    fields.append('subjectID')
  
  #add timeStamp/date column to csv  
  # if record_class.study_ID=="meditrain":
  #   if 'date' not in fields:
  #     fields.append('date')
  # else:
  #   if 'timeStamp' not in fields:
  #     fields.append('timeStamp')
      
  return fields
  


def csv_write(record_class):
  f = StringIO()
  w = writer(f)
  ww = w.writerow
  fields = get_fields(record_class)
  fields.sort()
  ww(fields)
  for record in record_class.query.all():
    ww([getattr(record, field) for field in fields])
  return f.getvalue()


@login_required
def csv(studyID):
  rc = studyID_to_record_class.get(studyID.lower())
  if not rc:
    abort(404)
  data = csv_write(rc)
  return Response(response=data, status=200, content_type='text/csv')


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
