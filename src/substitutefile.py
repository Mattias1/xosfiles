import json
from pathlib import Path


class SubstituteFile:
    def __init__(self, path, mapping):
        self.subs = {};

        self.load(path, mapping)

    def load(self, path, mapping):
        try:
            with open(path, 'r') as fd:
                self.parseSubsFile(fd, mapping)
        except:
            print('Could not open or parse the substitute file (' + path + ').')
            return None

    def parseSubsFile(self, fd, mapping):
        for line in fd:
            varname, sep, rest = line.partition(mapping.variable_assignment)
            if rest.strip() == mapping.multiline_open:
                innerlines = []
                for l in fd:
                    if l.strip() == mapping.multiline_close:
                        break
                    innerlines.append(l)
                innerlines[-1] = innerlines[-1].rstrip('\r\n')
                content = ''.join(innerlines)
            else:
                content = rest.strip()
            self.subs[varname.strip()] = content

    def alterFile(self, fd):
        result = []
        for line in fd:
            for k, v in self.subs.items():
                line = line.replace(k, v)
            result.append(line)
        return result
