from os import listdir
from os.path import isdir, isfile, join
from natsort import natsorted
from urllib import parse

def get_files(path):
    return natsorted(listdir(path))

albums = [(name, get_files(join("/srv/library/files", name))) for name in listdir("/srv/library/files")]
for (album, files) in albums:
    with open(join("/srv/library/index", album), 'w') as f:
        f.write(f"Files/{album}\n")
