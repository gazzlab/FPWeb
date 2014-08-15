from StringIO import StringIO
from flask.ext.wtf import Form
from wtforms import (
  DateField,
  TextField,
  TextAreaField,
  RadioField,
  SelectField,
  validators,
  widgets,
  HiddenField,
  )
from wtforms.widgets.core import html_params


def login_form(c, own_URL, OPENID_PROVIDERS, **extra):
  c.script(' '.join('''
function set_openid(openid, pr)
{
    u = openid.indexOf('[username]');
    if (u != -1) {
        /* openid requires username */
        user = prompt('Enter your ' + pr + ' username:');
        openid = openid.substr(0, u) + user;
    }
    form = document.forms['login'];
    form.elements['openid'].value = openid;
}
'''.split()), type_="text/javascript")
  with c.form(id_='login') as f:

    f(action=own_URL, method='POST')

    with f.div(class_='container') as d:
      d.h3('Login with your username')
      d.input(id_='user', name='user', type_='text')
      d.input(id_='pasw', name='pasw', type_='password')
      d.input(value='Login', type_='submit')

    with f.div(class_='container') as d:
      d.h3('Login with OpenID')
      prov = d.div
      for i, provider in enumerate(OPENID_PROVIDERS):
        a = prov.a(
          provider['name'],
          href="javascript:set_openid('%(url)s', '%(name)s');" % provider,
          )
        if i < len(OPENID_PROVIDERS) - 1:
          prov += ' | '
      d += 'OpenID: '
      d.input(name='openid', id_='openid', type_='text', size='30')
      d.input(value='Sign in', type_='submit')

    return f


def logout_form(c, own_URL, **extra):
  with c.div(class_='container').form as f:
    f(action=own_URL, method='POST')
    f.input(value='Logout', type_='submit')
    return f


def select_multi_checkbox(field, ul_class='', **kwargs):
  kwargs.setdefault('type', 'checkbox')
  field_id = kwargs.pop('id', field.id)
  html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
  for value, label, checked in field.iter_choices():
    choice_id = u'%s-%s' % (field_id, value)
    options = dict(kwargs, name=field.name, value=value, id=choice_id)
    if checked:
      options['checked'] = 'checked'
    html.append(u'<li><input %s /> ' % html_params(**options))
    html.append(u'<label for="%s">%s</label></li>' % (choice_id, label))
  html.append(u'</ul>')
  return u''.join(html)


class ProfileForm(Form):
  fname = TextField('First Name:', [validators.required()])
  lname = TextField('Last Name:', [validators.required()])
  sex = RadioField('Sex', coerce=int, choices=[
    (1, 'Male'),
    (2, 'Female'),
    ], validators=[validators.required()])
  birthdate = DateField("Your date of birth:", [validators.required()])
  subject_id = TextField('Subject ID', [validators.required()])
  phone = TextField('Phone Number')
  email = TextField('Email', [validators.Email()])
  language = TextField('What is your native language?')
  language_additional = TextAreaField('What other languages do you speak,'
                                      ' not including your native language?')
  meditation = TextField('Have you ever or do you currently practice any form of meditation?')
  mediatation_description = TextAreaField('Please describe the type of meditation, frequency'
                                          ' of practice, and how long ago you last practiced.')
  other_studies = SelectField('I would be interested in participating in the following types of studies',
    coerce=int,
    choices=[
      (0, 'Other behavioral studies'),
      (1, 'fMRI studies (at UCSF Mission Bay in SF)'),
      (2, 'EEG studies (at UCSF Mission Bay in SF)'),
      (3, '6-12 week cognitive training studies (computerized training is done at home)'),
      ],
    widget=select_multi_checkbox,
    )
##  Please check ALL that apply

  history = SelectField('Do you have a history of:',
    coerce=int,
    choices = [
      (0, 'color blindness'),
      (1, 'cardiac problems'),
      (2, 'bypass surgery'),
      (3, 'pacemaker or heart valve'),
      (4, 'stroke'),
      (5, 'respiratory conditions'),
      (6, 'head trauma with loss of consciousness (for a few seconds)'),
      (7, 'severe head trauma (loss of consciousness for more than a few minutes)'),
      (8, 'high/low blood pressure'),
      (9, 'kidney failure'),
      (10, 'electroconvulsive therapy (ECT)'),
      (11, 'seizures'),
      (12, 'implanted electrodes'),
      (13, 'cancer/chemotherapy/radiation'),
      (14, 'diabetes'),
      (15, 'irritable bowel syndrome'),
      (16, 'back problems'),
      (17, 'claustrophobia'),
      (18, 'dentures'),
      (19, 'major dental work (not including fillings)'),
      (20, 'hearing loss (hearing aids)'),
      ],
    widget=select_multi_checkbox,
    )
##  Please check ALL that apply

  history_explanation = TextAreaField('Please explain any checked boxes from above.')
  glasses = 'Do you normally wear prescription glasses or contact lenses?'
  psychiatric = RadioField(
    'Have you ever been diagnosed with a psychiatric or neurological disorder?',
    choices = [(0, 'Yes'), (1, 'No')],
    )
  psychiatric_describe = TextAreaField('Please describe')
  learning_disabilities = TextAreaField('Do you have any learning disabilities?')
  medications = TextAreaField('What medications are you currently taking?')
##    Please include over the counter medications and supplements.
  handedness = RadioField('What is your handedness', coerce=int, choices=[
    (0, 'right handed'),
    (1, 'left handed'),
    (2, 'ambidextrous'),
    ])
  school = TextField('How many years of education have you completed?')
##    High School = 12 + 1 for each year of undergraduate or graduate study
  alcohol = TextField('How many alcoholic drinks do you consume on average per week?')
  smoke = RadioField('Do you smoke? If so, how often?', coerce=int, choices=[
    (0, 'No'),
    (1, 'Daily'),
    (2, 'a few times per week'),
    (3, 'a few times per month'),
    (4, 'a few times per year'),
    ])
  exercise = RadioField('How often do you exercise?', coerce=int, choices=[
    (0, 'Daily'),
    (1, '4-6 times per week'),
    (2, '1-3 times per week'),
    (3, 'a few times a month'),
    (4, 'rarely/never'),
    ])
  type_exercises = TextField('What type of exercises do you do?')
  hours_sleep = TextField('How many hours of sleep do you typically get each night?')
#  participant_id type="hidden"


def profile_form(f=None, csrf_enabled=False, **kw):
  if f is None:
    f = StringIO()
  form = ProfileForm(csrf_enabled=csrf_enabled, **kw)
  for field in form:
    print >> f, field.label
    print >> f, field
    print >> f, '<br>'
  return f, form
  


##if __name__ == '__main__':
##  dummy_page = 'doobiedoobiedoo.html'
##  open(dummy_page, 'w')


