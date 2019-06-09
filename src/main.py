import crossosfiles
import sys
from pathlib import Path


class Main:
    def start(self, args):
        if self.help(args): return
        if self.version(args): return
        args = self.addAutoParamName(args)
        if self.setupOrBup(args): return
        print('Invalid arguments, why not try the --help flag?')

    def version(self, args):
        if '--version' in args:
            print('dotfiles setup script v alpha')
            return True
        return False

    def help(self, args):
        if '--help' in args:
            print('call /xosfiles/src/main.py --setup [name] or /xosfiles/src/main.py --bup [name]')
            return True
        return False

    def addAutoParamName(self, args):
        if len(args) == 1 and args[0] in ['--setup', '--bup']:
            path = Path('./autoparam.txt')
            with open(path, 'r') as fd:
                name = fd.read().strip()
                print('Using autoparam: ' + name)
                args.append(name)
        return args

    def setupOrBup(self, args):
        try:
            method, name = args[:2]
        except:
            return False

        xosfiles = crossosfiles.CrossOsFiles()
        if method == '--setup':
            xosfiles.setup(name)
            return True
        elif method == '--bup':
            xosfiles.bup(name)
            return True
        return False


main = Main()
main.start(sys.argv[1:])
