"""
Formats media files according to the config.
The config file should be a YAML file representing
a dictionary with target file names as keys, and
lists of source files as values.
"""

import sys
import os
from optparse import OptionParser
from threading import Timer
from subprocess import Popen, PIPE
import time
import yaml

bundles = {}

class Bundle(object):
    def __init__(self, target, sources):
        self.target = target
        self.paths = sources
    
    def __call__(self):
        raise NotImplementedError()

class JoinBundle(Bundle):
    def __call__(self):
        print 'Processing', self.target
        data = []
        for path in self.paths:
            if os.path.exists(path):
                data.append(open(path).read())
            else:
                print 'WARNING: File', path, 'not found!'

        open(self.target, 'w').write('\n'.join(data))

class CoffeeBundle(Bundle):
    def __call__(self):
        print 'Processing', self.target
        data = []
        for path in self.paths:
            out, err = Popen(['coffee', '-p', path], stdout = PIPE, stderr = PIPE, stdin = PIPE).communicate()        
            if err:
                print 'Processing of', self.target, 'failed:'
                print err
                return

            data.append(out)

        open(self.target, 'w').write('\n'.join(data))

bundles['js->js'] = JoinBundle
bundles['css->css'] = JoinBundle
bundles['coffee->js'] = CoffeeBundle

def interpret_config(configpath):
    def interpret_bundle(target, sources):
        if len(set(os.path.splitext(source)[1] for source in sources)) > 1:
            print 'Need homogenic extensions in media.yaml !'
            sys.exit(1)

        factory = bundles['%s->%s' %
                (os.path.splitext(sources[0])[1][1:],
                    os.path.splitext(target)[1][1:])]

        return factory(os.path.join(os.path.dirname(configpath), target), [os.path.join(os.path.dirname(configpath), source) for source in sources])
        
    #if not os.path.exists(options.config): There is no error handling anyway, so why bother?
    #    print 'WARNING: Cannot open config file at', options.config, 'assuming empty one!'

    config = yaml.load(open(configpath))

    return [interpret_bundle(target, sources) for target, sources in config.items()]

watcher = None

def rerun_watcher(configpath):
    global watcher

    if watcher:
        watcher.cancel()
        mtimes = watcher.mtimes
    else:
        mtimes = {}

    watcher = Watcher()
    watcher.mtimes = mtimes
    bundles = interpret_config(configpath)
    
    watcher.add(configpath, lambda: rerun_watcher(configpath))
    for bundle in bundles:
        watcher.add(bundle.paths, bundle)

    watcher()

class Watcher(object):
    def __init__(self):
        self.paths = []
        self.mtimes = {}
        self.timer = None
        self._cancel = False

    def cancel(self):
        self._cancel = True
    
    def add(self, path, callback):
        paths = [path] if isinstance(path, basestring) else path
        self.paths.append((paths, callback))

    def __call__(self):
        for paths, callback in self.paths:
            todo = False
            for path in paths:
                if os.stat(path).st_mtime > self.mtimes.get(path, -1):
                    print 'Detected change in', path
                    todo = True
                    self.mtimes[path] = os.stat(path).st_mtime
            if todo:
                callback()

        if not self._cancel:
            self.timer = Timer(2.0, self).start()

if __name__ == '__main__':
    parser = OptionParser(description = __doc__)

    parser.add_option('-c', '--config', dest = 'config',
            help = 'Config file.')
    parser.add_option('-w', '--watch', action = 'store_true', default = False, dest = 'watch',
            help = '"Watch for changes" mode.')
    parser.add_option('-v', '--verbose', action = 'store_true', default = False, dest = 'verbosity',
            help = 'Be verbose.')

    options, args = parser.parse_args()

    if options.config is None:
        print 'Thou shalt provide a config file!'
        sys.exit(1)

    if options.watch:
        print 'MEDIA: Starting watch mode.'
        rerun_watcher(options.config)
    else:
        for bundle in interpret_config(options.config):
            bundle()

