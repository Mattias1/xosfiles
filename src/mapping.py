import json

class Mapping:
    def __init__(self, name):
        self.dotfiles_dir = ''
        self.subdirs = []
        self.copies = []
        self.append_prefix = 'append-'

        self.load(name)

    def load(self, name):
        mappingContent = self.loadJson('./mapping-{}.json'.format(name))
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
        self.dotfiles_dir = valOr(mappingContent, 'dotfiles-dir', self.dotfiles_dir)
        self.append_prefix = valOr(mappingContent, 'append-prefix', self.append_prefix)
        copiesVal = valOr(mappingContent, 'copies', [])
        self.copies.extend([MapDir(repo, disk) for (repo, disk) in copiesVal])

    def isAppendsDir(self, directory):
        # TODO
        # return directory.startsWith(self.append_prefix)
        l = len(self.append_prefix)
        return directory[:l] == self.append_prefix


class MapDir:
    def __init__(self, repo, disk):
        self.repo = repo
        self.disk = disk

    def __str__(self):
        return '({}, {})'.format(self.repo, self.disk)

    def repo_is_dir(self):
        return self.repo[-1] == '/'

    def repo_is_file(self):
        return self.repo[-1] != '/'

    def disk_is_dir(self):
        return self.disk[-1] == '/'

    def disk_is_file(self):
        return self.disk[-1] != '/'


def val(content, key):
    try:
        return content[key]
    except (TypeError, KeyError):
        return None

def valOr(content, key, alternative):
    value = val(content, key)
    return alternative if value == None or value == '' or value == [] else value
