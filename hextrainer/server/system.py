
from inspect import isclass

from werkzeug import Request, Response, ClosingIterator
from werkzeug.local import Local, LocalManager
from werkzeug.routing import Map, Rule as Url
from werkzeug.exceptions import HTTPException, MethodNotAllowed
from jinja2 import Environment, FileSystemLoader

local = Local()
local_manager = LocalManager([local])

class ViewNotFoundError(Exception):
    pass

def url_for(endpoint, _external = False, **values):
    return local.mapper.build(endpoint, values, force_external = _external)

class Front(object):
    def __init__(self, urls, template_dir):
        self.urls = urls

        self.master_mapper = Map(urls)

        self.jinja = Environment(loader=FileSystemLoader(template_dir))
        self.jinja.globals['url_for'] = url_for

    def get_view(self, name):
        try:
            modname, objname = name.rsplit('.', 1)
            module = __import__(modname, globals(), locals())
            obj = getattr(module, objname)
            return obj() if isclass(obj) else obj

        except ImportError:
            raise ViewNotFoundError(name)

    def __call__(self, environ, start_response):
        local.front = self
        local.mapper = mapper = self.master_mapper.bind_to_environ(environ)

        local.request = request = Request(environ)

        try:
            endpoint, values = mapper.match()
            view = self.get_view(endpoint)

            response = view()

        except HTTPException, e:
            response = e

        return ClosingIterator(response(environ, start_response),
                [
                    local_manager.cleanup
                    ])

class ControllerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['controller_name'] = name
        return super(ControllerMetaclass, cls).__new__(cls, name, bases, attrs)

class Controller(object):
    __metaclass__ = ControllerMetaclass

    def get(self):
        raise MethodNotAllowed()
    def post(self):
        raise MethodNotAllowed()
    def put(self):
        raise MethodNotAllowed()
    def delete(self):
        raise MethodNotAllowed()
    
    def __call__(self):
        self.request = local.request

        method = self.request.method.lower()
        if not hasattr(self, method):
            raise MethodNotAllowed()

        return getattr(self, method)()

    def render(self, template, **values):
        return Response(local.front.jinja.get_template(template).render(**values),
                mimetype = 'text/html')

def expose(method):
    def decorator(fun):
        c = fun.func_globals.get(fun.__name__, Controller())

        setattr(c, method, lambda: fun(c))
        setattr(c, 'controller_name', fun.__name__)
        return c

    return decorator
