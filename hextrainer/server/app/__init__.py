
from system import expose

@expose('get')
def index(ctrl):
    return ctrl.render('index.html')

@expose('get')
def app(ctrl):
    return ctrl.render('app.html')
