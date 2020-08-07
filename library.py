from os import listdir
from os.path import isdir, isfile, join
from natsort import natsorted
import re

class Library:

# Index File Format:
# Index file name for folders is "<folder name> <tag>"
# MPD Uris for items to add to playlist in order, seperated by newlines

    def __init__(self, path):
        self.library_path =  path
        self.files_path = join(path, "files")
        self.index_path = join(path, "index")    
    
    def find_tag(self, tag):
        try:
            index_file = next(f for f in self.index_files() if bool(re.search(tag + "$", f, re.I)))
            return self.get_uris(index_file)
        except:
            return []

    def add_to_index(self, tag, folder):
        filename = f"{folder} {tag}"
        songs = natsorted([ join(self.files_path, folder, f) for f in listdir(join(self.files_path, folder))] )
        with (open(join(self.index_path, filename, 'w'))) as file:
            for song in songs:
                file.write(f"file:{song}\n")
    
    def unindexed_folders(self):
        all_albums = [ name for name in listdir(self.files_path) if isdir(join(self.files_path, name)) ]
        indexed_albums = [ name.rsplit(" ", 1)[0] for name in self.index_files() ]
        return [ name for name in all_albums if name not in indexed_albums ] 
        
    def index_files(self):
        return [ name for name in listdir(self.index_path) if isfile(join(self.index_path, name)) ]

    def get_uris(self, name):
        with open(join(self.index_path, name), 'r') as file:
            return file.readlines()
    
    def parse(self, content):
        return content.split(':', 1)