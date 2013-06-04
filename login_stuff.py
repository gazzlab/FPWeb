from flask import Flask, render_template, Response, request, redirect, abort
from flask.ext.login import (
  LoginManager,
  login_user,
  current_user,
  logout_user,
  )
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from templates import base
from database import db, User, RecordsDat


OPENID_STORE = '/tmp/oid.store'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/[username]'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/[username]'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'},
    ]


oid = OpenID(app=None, fs_store_path=OPENID_STORE)


login_manager = LoginManager()
login_manager.login_view = "login"


def require_role(role, error_response=lambda: abort(401)):
  def wrapper(f):
    def wrapped(*args, **kwargs):
      if current_user.is_authenticated() and current_user.role == role:
        return f(*args, **kwargs)
      return error_response()
    return wrapped
  return wrapper


@login_manager.user_loader
def load_user(uid):
  try:
    uid = int(uid)
  except ValueError:
    return None
  return User.query.filter_by(id=uid).first()


@oid.loginhandler
def login():
  pre = request.environ.get('SCRIPT_NAME', '')
  if request.method == 'GET':
    if current_user.is_anonymous():
      page_data = request.environ.get('PAGE', {})
      page_data['next'] = oid.get_next_url()
      page_data['error'] = oid.fetch_error()
      page_data['OPENID_PROVIDERS'] = OPENID_PROVIDERS
      return str(base(**page_data))
    return redirect(pre + LOGOUT_URL)

  open_id = request.form.get('openid')
  if open_id:
    return oid.try_login(open_id, ask_for=['email', 'fullname', 'nickname'])

  username = request.form['user']
  pw = request.form['pasw']
  user = User.query.filter_by(name=username, password=pw).first()

  if user:
    login_user(user)
    return redirect(oid.get_next_url() or pre)
  return redirect('Bah')


def logout():
  if not current_user.is_anonymous():
    if request.method == 'GET':
      page_data = request.environ.get('PAGE', {})
      return str(base(**page_data))
    logout_user()
  return redirect(request.environ.get('SCRIPT_NAME', '') + LOGIN_URL)


@oid.after_login
def after_login(response):
  pre = request.environ.get('SCRIPT_NAME', '')
  email_address = response.email
  if not email_address:
    flash('Invalid login. Please try again.')
    return redirect(pre + LOGIN_URL)

  user = User.query.filter_by(email=email_address).first()
  if not user:
    nickname = response.nickname or email_address.split('@', 1)[0]
    user = User(
      name=nickname,
      fullname=response.fullname,
      email=email_address,
      password="",
      )
    db.session.add(user)
    db.session.commit()
    redirect_to = '/profile'
  else:
    redirect_to = '/dash' if user.role == 'admin' else '/profile'

  login_user(user)
  return redirect(pre + redirect_to)


