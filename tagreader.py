import nfc
from event import Event
from thread import start_new_thread
from log import log

class TagReader:
    def __init__ (self, connection_string):
        self.clf = nfc.ContactlessFrontend(connection_string)
        self.tag_discovered = Event()
        start_new_thread(self.loop, ())

    def loop(self):
        while True:
            self.clf.connect(rdwr={'on-connect': self.on_connect})

    def on_connect (self, tag):
        log(f"TagReader: Tag {tag} discovered.")
        self.tag_discovered.fire(tag.identifier.encode('hex'))
        return True
