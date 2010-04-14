
from google.appengine.ext.webapp.util import run_wsgi_app

import sys
import os.path

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
sys.path = sys.path[:]

from system import Front
from urls import urls

def main():
    app = Front(urls(), os.path.join(os.path.dirname(__file__), '../templates'))

    run_wsgi_app(app)

if __name__ == '__main__':
  main()
