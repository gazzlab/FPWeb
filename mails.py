from flask import Flask
from flask.ext.mail import Mail, Message


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = 'test.account'
app.config['MAIL_PASSWORD'] = open('/home/sforman/GazAd').read().strip()

# MAIL_DEBUG = default app.debug
# MAIL_SUPPRESS_SEND 

mail = Mail(app)

msg = Message(
  'Yo, testing email, DONOTREPLY Yo',
  body='''
"The history of mankind for the last four centuries is rather like that of
an imprisoned sleeper, stirring clumsily and uneasily while the prison that
restrains and shelters him catches fire, not waking but incorporating the
crackling and warmth of the fire with ancient and incongruous dreams, than
like that of a man consciously awake to danger and opportunity."
--H. P. Wells, "A Short History of the World"
''',
  sender="test.account@gazzaleylab.ucsf.edu",
  recipients=[
    'forman.simon@gmail.com',
    'morgan.hough@gmail.com',
    ],
  )
