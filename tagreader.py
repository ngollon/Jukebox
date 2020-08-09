import nfc
import threading
from event import Event
from time import sleep
from log import log
from datetime import datetime, timedelta
from binascii import hexlify

class TagReader:
    def __init__ (self, connection_string):
        self.clf = nfc.ContactlessFrontend(connection_string)

        self.last_tag = ""
        self.last_tag_time = datetime.now()

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
        identifier = hexlify(tag.identifier).decode('utf-8')
        tag_time = datetime.now()

        if (tag_time - self.last_tag_time > timedelta(seconds=5)) or identifier != self.last_tag:
            log(f"TagReader: Tag {tag} discovered.")
            self.last_tag = identifier
            self.tag_event.set()        
            self.tag_discovered.fire(identifier)

        self.last_tag_time = tag_time
        return True
