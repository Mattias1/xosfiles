import mapping
import shutil
from pathlib import Path

class CrossOsFiles:
    def setup(self, name):
        mapping = self.loadMapping(name)
        for m in mapping.copies:
            if m.repo.is_dir() and m.disk.is_dir():
                self.copyDirTo(m.repo, m.disk, mapping)
            elif m.repo.is_file() and m.disk.is_file():
                self.copyFileTo(m.repo, m.disk)
            elif m.repo.is_file() and m.disk.is_dir():
                self.copyFileTo(m.repo, m.disk / m.repo.name)
            else:
                print("Can't copy a dir to a file {}. Maybe add a '/' in the json mapping?".format(m))
        print('Done')


    def copyDirTo(self, src, dst, mapping):
        print('Copying dir  {}  to  {}'.format(src, dst))
        self.makeDirs(dst)

        for source in src.iterdir():
            filename = source.name
            destination = dst / filename

            if source.is_dir():
                if not mapping.isAppendsDir(filename):
                    self.copyDirTo(source, destination, mapping)
            elif source.is_file():
                shutil.copy(source, destination)
            else:
                print('Skipping {}, as it\'s not a file or directory.'.format(filename))

    def copyFileTo(self, src, dst):
        print('Copying file {}  to  {}'.format(src, dst))
        self.makeDirs(dst.parent)

        shutil.copy(src, dst)

    def makeDirs(self, directory):
        directory.mkdir(parents = True, exist_ok = True)

    def loadMapping(self, name):
        return mapping.Mapping(name)


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
#   - xosfiles/
#   - setup.sh          (calling python script)
#   - bup.sh            (calling python script)
#   - mapping-linux.json
#   - mapping-windows.json
#   - mapping-personal.json
#   - mapping-topicus.json
#   - autoparam.txt
