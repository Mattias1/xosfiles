import json
from pathlib import Path
from substitutefile import SubstituteFile


class Mapping:
    def __init__(self, name):
        self.dotfiles_dir = ''
        self.subdirs = []
        self.copies = []

        self.substitute_prefix = 'substitute-'
        self.variable_prefix = '${'
        self.variable_suffix = '}'
        self.variable_assignment = '='
        self.multiline_open = '{'
        self.multiline_close = '}'

        self.load(name)

    def load(self, name):
        mappingPath = Path('./mapping-{}.json'.format(name))
        mappingContent = self.loadJson(mappingPath)
        extend = val(mappingContent, 'extend')
        if (extend != None):
            self.load(extend)
        self.parseJson(name, mappingContent)

    def loadJson(self, path):
        try:
            with open(path, 'r') as fd:
                return json.load(fd)
        except:
            print('Could not open or parse the json file (' + path + ').')
            return None

    def parseJson(self, name, mappingContent):
        self.subdirs.append(name)
        self.dotfiles_dir = Path(valOr(mappingContent, 'dotfiles-dir', self.dotfiles_dir))

        self.substitute_prefix = valOr(mappingContent, 'substitute-prefix', self.substitute_prefix)
        self.variable_prefix = valOr(mappingContent, 'variable-prefix', self.variable_prefix)
        self.variable_suffix = valOr(mappingContent, 'variable-suffix', self.variable_suffix)
        self.variable_assignment = valOr(mappingContent, 'variable-assignment', self.variable_assignment)
        self.multiline_open = valOr(mappingContent, 'multiline-open', self.multiline_open)
        self.multiline_close = valOr(mappingContent, 'multiline-close', self.multiline_close)

        copiesVal = valOr(mappingContent, 'copies', [])
        self.copies.extend([MapDir(self.dotfiles_dir, repo, disk) for (repo, disk) in copiesVal])

    def isSubstituteDir(self, directory):
        l = len(self.substitute_prefix)
        return directory[:l] == self.substitute_prefix

    def getSubstituteFile(self, path):
        result = None

        filename = path.name
        parentdir = path.parent
        for subdirname in self.subdirs:
            subsdir = parentdir / (self.substitute_prefix + subdirname)
            subsfile = subsdir / filename
            if subsdir.is_dir() and subsfile.is_file():
                if result == None:
                    result = SubstituteFile(subsfile, self)
                else:
                    result.load(subsfile, self)

        return result


class MapDir:
    def __init__(self, dotfiles_dir, repo, disk):
        self.repo = (dotfiles_dir / repo).expanduser().resolve()
        self.disk = Path(disk).expanduser().resolve()

    def __str__(self):
        return '({}, {})'.format(self.repo, self.disk)


def val(content, key):
    try:
        return content[key]
    except (TypeError, KeyError):
        return None

def valOr(content, key, alternative):
    value = val(content, key)
    return alternative if value == None or value == '' or value == [] else value
