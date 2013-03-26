'''
This is where all the specific content for pages should go.

(Notice that this file/module imports nothing?  Is that significant?)

Both html.py patterns and content (text) can be specified here. The urls.txt
and the pre-made generic structures will compose it properly. (At least
that's the idea.)
'''

#: I'm using this content distribution network.
CDN = 'http://cdnjs.cloudflare.com/ajax/libs/'


def body(body, title, page_title, form, **extra):
  '''
  A simple body renderer.
  '''
  body.h1(page_title)
  form(body, **extra)


def dp_html(c, subtitle, POSTDATA, **extra):
  c.h3(subtitle)
  c.pre(POSTDATA)


datapost = dict(
  title = 'Gazzian',
  page_title = 'Data Received',
  subtitle = 'Click here to...',
  body = body,
  form = dp_html,
  )


def home_html(c, subtitle, **extra):
  c.h3(subtitle)
  with c.div(class_='container') as d:
    d('Some content!')


home_page = dict(
  title = 'Gazzian',
  page_title = 'Brain-O-Scope',
  subtitle = 'Human-Computer Neural Interface',
  body = body,
  form = home_html,
  )


def logout_form(c, own_URL, **extra):
  with c.div(class_='container').form as f:
    f(action=own_URL, method='POST')
    f.input(value='Logout', type_='submit')
    return f


logout_page = dict(
  title = 'Gazzian Logout',
  page_title = 'Logout',
  body = body,
  form = logout_form,
  own_URL = '/log/out',
)


def login_form(c, own_URL, **extra):
  with c.form as f:

    f(action=own_URL, method='POST')

    with f.div(class_='container') as d:
      d.h3('Login with your username')
      d.input(id_='user', name='user', type_='text')
      d.input(id_='pasw', name='pasw', type_='password')
      d.input(value='Login', type_='submit')

    with f.div(class_='container') as d:
      d.h3('Login with OpenID')
      d += 'OpenID: '
      d.input(name='openid', type_='text', size='30')
      d.input(value='Sign in', type_='submit')

    return f


login_page = dict(
  title = 'Gazzian Login',
  page_title = 'Login',
  body = body,
  form = login_form,
  own_URL = '/log/in',
  )













##page = dict(
##
##  scripts = [CDN + js_lib for js_lib in (
##    'd3/3.0.1/d3.v3.min.js',
##    'underscore.js/1.4.3/underscore-min.js',
##    'jquery/1.8.3/jquery.min.js',
##    'jqueryui/1.9.2/jquery-ui.min.js',
##    )],
##
##  stylesheets = ('http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css',),
##
##  body = xerblin_body,
##
##  # The stuff above is used by base() template function, while this stuff
##  # is passed into the body (i.e. xerblin_body above.)
##  title = 'Xerblin',
##  subtitle = 'a Human-Computer Interface',
##  UL = my_ul,
##  things = {
##    'stack': 'a place to put objects for user manipulation. This is similar to a Clipboard but it can hold more than one item at a time. Commands operate on the items on the Stack.',
##    'dictionary': 'a place to keep commands. Any command that is inscribed in the Dictionary can be run from the user interface.',
##    'interpreter': 'a very simple command interpreter that takes care of running commands with the Stack. ',
##    },
##
##)

