from abc import ABC, abstractmethod
from os import listdir
from os.path import isdir, isfile, join

class Library(ABC):

    @abstractmethod
    def find_tag(self, tag):
        pass

class FileLibrary(Library):
    def __init__(self, path):
        self.path =  path
    
    def find_tag(self, tag):
        try:
            selected_album = next(f for f in listdir(self.path) if isdir(join(library_path, f)) and bool(re.search(tag + "$", f, re.I)))
            return "file:" + selected_album
        except:
            return None                    

class UriLibrary(Library):
    def __init__(self, path):
        self.path =  path
    
    def find_tag(self, tag):
        try:
            selected_file = next(f for f in listdir(self.path) if isfile(join(library_path, f)) and bool(re.search(tag + "$", f, re.I)))
            with open(join(library_path, selected_file), 'r') as file:
                return file.read().trim()
        except:
            return None        