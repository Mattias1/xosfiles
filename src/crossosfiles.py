import os
import mapping
import shutil

class CrossOsFiles:
    def setup(self, name):
        mapping = self.loadMapping(name)
        dfdir = mapping.dotfiles_dir
        for m in mapping.copies:
            if m.repo_is_dir() and m.disk_is_dir():
                self.copyDirTo(dfdir + m.repo, m.disk, mapping)
            elif m.repo_is_file() and m.disk_is_file():
                self.copyFileTo(dfdir + m.repo, m.disk)
            elif m.repo_is_file() and m.disk_is_dir():
                filename = m.repo.split('/')[-1]
                self.copyFileTo(dfdir + m.repo, m.disk + filename)
            else:
                print("Can't copy a dir to a file {}. Maybe add a '/' in the json mapping?".format(m))
        print('Done')


    def copyDirTo(self, src, dst, mapping):
        print('Copying dir  {}  to  {}'.format(src, dst))
        correctedSource = self.correctpath(src)
        correctedDestination = self.correctpath(dst)

        self.makeDirs(correctedDestination)

        filenames = os.listdir(correctedSource)
        for f in filenames:
            source = correctedSource + f
            destination = correctedDestination + f

            if os.path.isdir(source):
                if not mapping.isAppendsDir(f):
                    self.copyDirTo(src + f + '/', dst + f + '/', mapping)
            elif os.path.isfile(source):
                shutil.copy(source, destination)
            else:
                print('Skipping {}, as it\'s not a file or directory.'.format(f))
        # Note: error for files that already exist ?

    def makeDirs(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        # TODO: Doesn't work with harlequin colors

    def copyFileTo(self, src, dst):
        print('Copying file {}  to  {}'.format(src, dst))
        source = self.correctpath(src)
        destination = self.correctpath(dst)
        shutil.copy(source, destination)
        # Note: probably error for files that already exist

    def loadMapping(self, name):
        return mapping.Mapping(name)

    def correctpath(self, path):
        if path[0] == '~':
            path = os.path.expanduser('~') + path[1:]
        path = path.replace('\\\\', '\\')
        path = path.replace('\\', '/')
        # path = path.replace(' ', '\ ') # Breaks things in windows, but maybe needed in linux? Maybe just don't use spaces there? :P
        return path


    # Backup
    def bup(self, name):
        self.loadMapping(name)
        print('Backup: ' + name)


# dir structure:
# - home/
#   - .fate/
#   - append-windows/
# - rest/
# - setup
#   - scripts/
#   - setup.sh          (calling python script)
#   - bup.sh            (calling python script)
#   - mapping-linux.json
#   - mapping-windows.json
#   - mapping-personal.json
#   - mapping-topicus.json
#   - autoparam.txt
