Functional Programming for Web Sites
=====================================

Using WSGI I am playing with composing web sites using vaguely Functional-style
methods.  So far the results are encouraging.  A lot of people have created
software that makes this relatively straightforward.


What's going on:

    basket/  Dependencies stored for offline installation.

    debug_server.py  Run this locally to serve pages.

    INSTALL  Basically the script for setting up a working environment.

    main.py  Set URLS_FILE to point to urls.txt and fire up twistd (or whatever.)


The generic parts:

    server.py - WSGI parts to serve pages.
    templates.py - "Templates" for HTML in Python.


The specific parts:

    pages.py - Page content is in here.
    urls.txt - This drives the whole system,
               mapping URLs, methods, handlers, policy and content to define
               the web site.



If you install Twisted ("pip install twisted") you should be able to run the app with:

    export URLS_FILE=urls.txt
    twistd web --wsgi main.app --port 5000

