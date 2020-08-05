from os import listdir
from os.path import isdir, isfile, join

class Library:

    def __init__(self, path):
        self.library_path =  path
        self.files_path = join(path, "files")
        self.index_path = join(path, "index")
    
    def find_tag(self, tag):
        try:
            selected_file = next(f for f in self.index_files() if bool(re.search(tag + "$", f, re.I)))
            return index_content(selected_file)
        except:
            return None

    def index(tag, name):
        filename = f"{name} - {tag}"
        with (open(join(self.index_path, filename, 'w'))) as file:
            file.write(f"file:{name}")
    
    def untagged_albums(self):
        all_albums = [ name for name in listdir(self.library_path) if isdir(join(self.library_path, name)) ]
        indexed_albums = [ c[1] for c in [ parse(index_content(f)) for f in self.index_files ] if c[0] == 'file' ]
        return [ name for name in all_albums if name not in indexed_albums ] 
        
    def index_files(self):
        return [ name for name in listdir(self.index_path) if isfile(join(self.index_path, name) ]

    def index_content(self, name)
        with open(join(self.index_path, name), 'r') as file:
            return file.read().trim()
    
    def parse_index(self, content):
        return content.split(':', 1)