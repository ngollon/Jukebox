import nfc
import threading
from event import Event
from time import sleep
from log import log

class TagReader:
    def __init__ (self, connection_string):
        self.clf = nfc.ContactlessFrontend(connection_string)
        self.tag_discovered = Event()
        self.tag_event = threading.Event()
        self.monitoring_thread = threading.Thread(target=self.loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def wait_for_tag(self):
        self.tag_event.clear()
        self.tag_event.wait()
        return self.last_tag

    def loop(self):
        while True:
            self.clf.connect(rdwr={'on-connect': self.on_connect})

    def on_connect (self, tag):        
        log(f"TagReader: Tag {tag} discovered.")
        try:
            self.last_tag = tag
            self.tag_event.set()
            self.tag_discovered.fire(tag.identifier.encode('hex'))
        except:
            pass
        return True
