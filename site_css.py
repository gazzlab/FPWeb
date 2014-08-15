from scss import Scss


#: Define some CSS variables.
params = dict(('$' + k, v) for k, v in dict(

  body_font = "'Oxygen', serif",
  title_font = "'Cutive', sans-serif",

  foreground = '#333333',

  padding = '2em',

  ).iteritems())


rules = '''\
/* from Foundation CSS */
input[type="text"], input[type="password"], input[type="date"], input[type="datetime"], input[type="email"], input[type="number"], input[type="search"], input[type="tel"], input[type="time"], input[type="url"], textarea { background-color: white; font-family: inherit; border: 1px solid #cccccc; -webkit-border-radius: 2px; -moz-border-radius: 2px; -ms-border-radius: 2px; -o-border-radius: 2px; border-radius: 2px; -webkit-box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1); -moz-box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1); box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1); color: rgba(0, 0, 0, 0.75); display: block; font-size: 14px; margin: 0 0 12px 0; padding: 6px; height: 32px; width: 100%; -webkit-transition: all 0.15s linear; -moz-transition: all 0.15s linear; -o-transition: all 0.15s linear; transition: all 0.15s linear; }
input[type="text"].oversize, input[type="password"].oversize, input[type="date"].oversize, input[type="datetime"].oversize, input[type="email"].oversize, input[type="number"].oversize, input[type="search"].oversize, input[type="tel"].oversize, input[type="time"].oversize, input[type="url"].oversize, textarea.oversize { font-size: 17px; padding: 4px 6px; }
input[type="text"]:focus, input[type="password"]:focus, input[type="date"]:focus, input[type="datetime"]:focus, input[type="email"]:focus, input[type="number"]:focus, input[type="search"]:focus, input[type="tel"]:focus, input[type="time"]:focus, input[type="url"]:focus, textarea:focus { background: #fafafa; border-color: #b3b3b3; }
input[type="text"][disabled], input[type="password"][disabled], input[type="date"][disabled], input[type="datetime"][disabled], input[type="email"][disabled], input[type="number"][disabled], input[type="search"][disabled], input[type="tel"][disabled], input[type="time"][disabled], input[type="url"][disabled], textarea[disabled] { background-color: #ddd; }
textarea { height: auto; }
select { width: 100%; }

/* Some bits of miscellaneous CSS */

@import url(http://fonts.googleapis.com/css?family=Cutive|Oxygen:400,700);

body {
  line-height: 1.5;
  font-family: $body_font;
  color: $foreground;
}

h1, h2, h3, h4, h5, h6, .heavy {
  font-family: $title_font;
  font-weight: bold;
}

#container {
  border: 1px dashed gray;
  padding-left: 2em;
}

#commande, #meta_controls {
  display: inline;
}

#commande {
  width: 38%;
}

form {
  padding: 1em;
  margin: 0.5em;
}

#docs {
/*
  font-family: 'Cutive',sans-serif;
  max-width: 33em;
  margin-left: 5em;
*/
}
#docs ul {
  border: none;
  margin-left: 2em;
}

#container ul {
  border: 1px dashed gray;
  padding: 3px;
  margin: 3px;
}
'''


site_default = Scss(scss_vars=params).compile(rules)


if __name__ == '__main__':
  print site_default
