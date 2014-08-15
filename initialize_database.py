import sys
from main import app
from login_stuff import db, User

app.test_request_context().push()

if len(sys.argv) > 1 and raw_input('Drop tables? [yes/N] ') == 'yes':
  db.drop_all()

db.create_all()
ed_user = User('ed', 'Ed Jones', 'ed@example.com', 'password')
ed_user.role = u'admin'
db.session.add(ed_user)
db.session.commit()
print User.query.all()
