'''
Pythonic HTML "Templates" made from html.py patterns.

Generic stuff goes in here, to form a library of "functional" HTML.
'''
from html import HTML


#: Identity function.
I = lambda foo, *a, **b: foo


def base(title, extra_head=I, scripts=(), stylesheets=(), body=I, html=None, **body_args):
  '''
  Base template for creating HTML pages.

  TODO: Document the parameters, etc...

  '''
  if html is None:
    html = HTML()

  with html.head as head:
    head.title(title)
    head.meta(charset='utf-8')
    extra_head(head)
    for script in scripts:
      head.script('', src=script)
    for stylesheet in stylesheets:
      head.link(rel='stylesheet', href=stylesheet)

  body(html.body, title, **body_args)

  return html


if __name__ == '__main__':
  from pages import logout_page
  print '<!DOCTYPE html>'
  print base(**logout_page)
