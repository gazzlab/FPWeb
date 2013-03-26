#!/usr/bin/env python
import json
import requests


r = requests.post('http://localhost:5000/datapost', data=json.dumps({'bats': 'Tuesday'}))


assert r.status_code == 200, r.status_code
assert r.headers['content-type'] == 'text/html', r.headers['content-type']
assert r.text == (
  u'<html><head><title>Gazzian</title><meta charset="utf-8"></meta></head>'
  u'<body><h1>Data Received</h1><h3>Click here to...</h3>'
  u"<pre>{u'bats': u'Tuesday'}</pre></body></html>"
  ), r.text
print 'Okay!'