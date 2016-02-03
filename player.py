import vlc
from os import listdir
from os.path import isfile, join
from natsort import natsorted, ns
from time import sleep
from event import Event
import threading


class Player:
    def __init__ (self):
        self.media_player = vlc.MediaPlayer()
        self.media_player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.on_song_finished, 0)
        self.playlist = []
        self.playlist_index = -1
        self.playlist_thread = threading.Thread(target=self.run_playlist_thread)
        self.playlist_thread.daemon = True
        self.playlist_thread.start()
        self.next_track_event = threading.Event()

        self.track_changed = Event()
        self.stopped = Event()

    def run_playlist_thread(self):
        try:
            while(True):
                self.next_track_event.wait()
                self.next_track_event.clear()
                if len(self.playlist) > self.playlist_index:
                    self.play_track()
                else:
                    self.stopped.fire()
        except (KeyboardInterrupt, SystemExit):
            pass

    def play_album(self, album):
        self.playlist = natsorted([join(album, f) for f in listdir(album) if isfile(join(album, f))], alg=ns.IGNORECASE)
        self.playlist_index = 0
        self.play_track()


    def play_track(self):
        self.media_player.set_mrl(self.playlist[self.playlist_index])
        self.media_player.play()
        self.track_changed.fire(self.playlist_index + 1)

    def on_song_finished(self, *args, **kwds):
        self.playlist_index += 1
        self.next_track_event.set()
