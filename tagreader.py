import nfc
import threading
from event import Event
from thread import start_new_thread
from time import sleep
from log import log

class TagReader:
    def __init__ (self, connection_string):
        self.clf = nfc.ContactlessFrontend(connection_string)
        self.tag_discovered = Event()
        self.tag_event = threading.Event()
        start_new_thread(self.loop, ())

    def wait_for_tag(self):
        self.tag_event.clear()
        self.tag_event.wait()
        return self.last_tag

    def loop(self):
        while True:
            self.clf.connect(rdwr={'on-connect': self.on_connect})

    def on_connect (self, tag):
        log(f"TagReader: Tag {tag} discovered.")
        self.last_tag = tag
        self.tag_event.set()
        self.tag_discovered.fire(tag.identifier.encode('hex'))
        return True
