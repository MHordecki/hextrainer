
from system import Url

urls = lambda: [
        Url('/', endpoint = 'app.index'),
        Url('/app', endpoint = 'app.app'),
        ]
