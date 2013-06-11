'''
This is where all the specific content for pages should go.

Both html.py patterns and content (text) can be specified here. The urls.txt
and the pre-made generic structures will compose it properly. (At least
that's the idea.)
'''
from datetime import datetime
from flask import request
from forms import login_form, logout_form, profile_form


pform_string, pform = profile_form()
pform_string = pform_string.getvalue()


def body(body, title, page_title, form, crumbs, **extra):
  '''
  A simple body renderer.
  '''
  pre = request.environ.get('SCRIPT_NAME', '')
  if 'own_URL' in extra:
    extra['own_URL'] = pre + extra['own_URL']
  body.h1(page_title)
  with body.div as d:
    d(class_='crumbs')
    n = len(crumbs) - 1
    for i, (name, URL) in enumerate(crumbs):
      a = d.a(name, href=pre + URL)
      if i < n:
        d += ' - '
  form(body, **extra)


def do_table(c, title, heads, rows, row_maker, **extra):
  c.h3(title)
  with c.table(border='1') as t:
    with t.thead.tr as head:
      for h in heads:
        head.th(h)
    for row_data in rows:
      with t.tr as row:
        row_maker(row, row_data, **extra)


def dp_html(c, subtitle, POSTDATA, **extra):
  c.h3(subtitle)
  c.pre(POSTDATA)


datapost = dict(
  title = 'Gazzian',
  page_title = 'Data Received',
  subtitle = 'Click here to...',
  body = body,
  form = dp_html,
  crumbs = [],
  )


def home_html(c, subtitle, **extra):
  c.h3(subtitle)
  with c.div(class_='container') as d:
    d('''Welcome to the Gazzian NeuroPost Center!  
    
    Please begin by logging in.  If you do not have an assigned username and password,/
    you may log in with your Google, Yahoo, AOL, Flickr, or MyOpenID account.  /
    Simply click on the account provider (ie: Google) that you would like to use,/
    and follow the instructions to Sign in./
    
    Creating a user profile will allow us to gather your contact and background information,/
    which we can use to let you know about Gazzian research studies in which you might be interested./
    You can also update this later, in case your contact or background information changes.
    
    
    FOR RESEARCHERS: Select the 'dash' module to access study data.''')
    

home_page = dict(
  title = 'Gazzian',
  page_title = 'Brain-O-Scope',
  subtitle = 'Human-Computer Neural Interface',
  body = body,
  form = home_html,
  crumbs = [
    ('neuropost', '/'),
    ('dash', '/dash'),
    ('profile', '/profile'),
    ('login','/login' ),
    ('logout','/logout' ),
    ],
  )


logout_page = dict(
  title = 'Gazzian Logout',
  page_title = 'Logout',
  body = body,
  form = logout_form,
  own_URL = '/logout',
  crumbs = [
    ('neuropost', '/'),
    ('dash', '/dash'),
    ('profile', '/profile'),
    ('logout','/logout' ),
    ],
)


login_page = dict(
  title = 'Gazzian Login',
  page_title = 'Login',
  body = body,
  form = login_form,
  own_URL = '/login',
  crumbs = [
    ('neuropost', '/'),
    ('login','/login' ),
    ],
  )


def main_dash(c, user, db, record_classes, ra, **extra):
  html = c.root
  title_h1 = html.find('h1')
  title_h1.text = title_h1.text.format(UserName=user.fullname)

  def r(row, rc, **extra):
    row.td.a(rc.study_ID, href='study/' + rc.study_ID) # TODO fix the SCCRIPT_thingy....
    row.td(str(rc.query.count()))
    row.td.a('download CSV', href='csv/' + rc.study_ID)

  do_table(
    c.div,
    "Studies",
    ('Study', 'Total Records'),
    record_classes,
    r,
    )

  def r(row, (stid, records), **extra):
    row.td.a(stid, href='study/' + stid)
    row.td(str(len(list(records))))

  do_table(
    c.div,
    'Additional Studies',
    ('Study', 'Total Records'),
    ra.by_studyID(),
    r,
    )


main_page = dict(
  title = 'Gazzian Main',
  page_title = 'Hi {UserName}',
  body = body,
  form = main_dash,
  own_URL = '/dash',
  crumbs = [
    ('neuropost', '/'),
    ('dash', '/dash'),
    ('profile', '/profile'),
    ('logout','/logout' ),
    ],
  )


def study(c, user, db, record_class, **extra):
  studyID = record_class.study_ID

  def r(row, record, **extra):
    #t = datetime.utcfromtimestamp(record.timeStamp)
    t = datetime.fromtimestamp(record.timeStamp) #replaces UTC with local time    
    row.td(t.isoformat(' '))

  do_table(
    c.div,
    "Records",
    #Headers should be defined by record_class (ie: studyID-specific)
    #Would like to have Headers here for *all* fields in that rec
    ('Timestamp', 'SubjectID', 'Laa', 'La'), #new column headers added
    record_class.query.all(),
    r,
    )


study_page = dict(
  title = 'Gazzian Study {studyID}',
  body = body,
  form = study,
  own_URL = '/study/',
  crumbs = [
    ('neuropost', '/'),
    ('dash', '/dash'),
    ('profile', '/profile'),
    ('logout','/logout' ),
    ],
  )


def profile(c, user, db, own_URL, **extra):
  f = c.form('{form_content}', action=own_URL, method='POST')
  f.input(value='Create | Update', type_='submit')


profile_page = dict(
  title = 'Profile',
  page_title = 'Profile',
  body = body,
  form = profile,
  form_content=pform_string,
  own_URL = '/profile',
  crumbs = [
    ('neuropost', '/'),
    ('dash', '/dash'),
    ('logout','/logout' ),
    ],
  )
