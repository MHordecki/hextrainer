
from threading import Thread
from subprocess import Popen, call
from time import sleep
from yaml import load
import os.path
import sys

class MasterHandle(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def terminate(self, reason):
        print 'Terminating because of', reason

        for child in self.children:
            child.terminate()

        self.children = []

    def run(self):
        for child in self.children:
            print 'Launching devserver module', child.name
            child.devserver()

        while True:
            for child in self.children:
                if not child.check_pulse():
                    self.terminate(child.name)
                    return

            sleep(2)

    def deploy(self):
        for child in self.children:
            print 'Launching deploy module', child.name
            child.deploy()

class ChildHandle(object):
    name = 'NoName Handler'

    def __init__(self):
        self.__processes = []

    def register_process(self, process):
        self.__processes.append(process)

    def check_pulse(self):
        for process in self.__processes:

            if process.poll() is not None:
                return False

        return True

    def terminate(self):
        for idx, process in enumerate(self.__processes):
            print 'Terminating', self.name, 'process #%d' % idx
            if process.poll() is None:
                process.terminate()
                process.wait()
        
        self.__processes = []

    def devserver(self):
        pass

    def deploy(self):
        pass

class DevserverHandle(ChildHandle):
    name = 'App Engine Devserver'

    def __init__(self, config):
        super(DevserverHandle, self).__init__()

        self.path = config

    def devserver(self):
        self.register_process(Popen(['python2.5', 'google-appengine/dev_appserver.py', self.path]))

class MediaHandle(ChildHandle):
    name = 'Media Compressor'

    def __init__(self, config):
        super(MediaHandle, self).__init__()

        self.config = config

    def devserver(self):
        self.register_process(Popen(['python', 'watcher.py', '-c', self.config, '-w']))

    def deploy(self):
        call(['python', 'watcher.py', '-c', self.config, '-v'])

class DeployHandle(ChildHandle):
    name = 'Deploy'

    def __init__(self, config):
        super(DeployHandle, self).__init__()

        self.config = config

    def deploy(self):
        call(['python2.5', 'google-appengine/appcfg.py', 'update', self.config], stdin = sys.stdin)

def cmd_help(args):
    "Print this help message."
    print 'BRAINBEAN MANAGEMENT SCRIPT'
    print ''
    print 'Just a thin wrapper around GAE & bb-specific utilities.'
    print ''
    
    cmds = [(x[4:], globals()[x].__doc__) for x in globals() if x.startswith('cmd_')]
    maxlen = max(len(x[0]) for x in cmds)
    
    for cmd, doc in cmds:
        print '\t', cmd.ljust(maxlen+4), doc

def cmd_runserver(args):
    "Runs devserver & utilities."
    handle.start()
    handle.join()

def cmd_deploy(args):
    "Deploys the app to GAE."
    handle.deploy()

if __name__ == '__main__':
    config = load(open('config.yaml'))
    handle = MasterHandle()
    
    if 'media' in config:
        handle.add_child(MediaHandle(config['media']))

    if 'devserver' in config:
        handle.add_child(DevserverHandle(config['devserver']))

    if 'deploy' in config:
        handle.add_child(DeployHandle(config['deploy']))

    args = sys.argv[1:]
    if not args:
        cmd = 'help'
    else:
        cmd, args = args[0], args[1:]

    cmdname = 'cmd_' + cmd
    if cmdname not in globals():
        print 'No command named %s.' % cmdname
        sys.exit(1)

    try:
        globals()[cmdname](args)
    except KeyboardInterrupt:
        pass
    
