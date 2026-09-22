import mouse
import pickle
from threading import Thread

from PySide6.QtCore import Signal, qtTrId, QDateTime, QTimer
from PySide6.QtWidgets import QFileDialog

import settings as config


class Recorder(object):
    def __init__(self, parent=None):
        self.parent = parent #  Only for File dialogs
        self.recorded_events:list = []
        self.recording_name:str = ''
        self.replay_stopped:Signal = Signal()
        self.is_recording = False
        self.is_playing = False

    def record(self):
        pass

    def stop_recording(self):
        pass

    def save_recording(self):
        if self.recorded_events:
            filename = QFileDialog.getSaveFileName(self.parent, qtTrId('SAVE_AS_DIALOG_TITLE'),
                                                   self.recording_name.replace(':', ';'), '*.smrrec')
            if not filename[0] == '':
                with open(filename[0], 'wb') as record_file:
                    pickle.dump(self.recorded_events, record_file)

    def load_recording(self):
        filename = QFileDialog.getOpenFileName(self.parent, qtTrId('OPEN_DIALOG_TITLE'), '', '*.smrrec')
        if not filename[0] == '':
            with open(filename[0], 'rb') as record_file:
                self.recorded_events = pickle.load(record_file)
                self.recording_name = filename[0].split('/')[-1]


    def start_playback(self, delay:int = 0, loop:bool = False):
        timer = QTimer()
        timer.setSingleShot(not loop)
        timer.setInterval(delay)
        timer.timeout.connect(lambda: Thread(mouse.play(self.recorded_events)).start())
        timer.start()
        self.is_playing = True

    def stop_playback(self):
        self.replay_stopped.emit()

    def get_recorded_events(self) -> list:
        return self.recorded_events

    def get_recording_name(self) -> str:
        return self.recording_name

    def get_is_playing(self) -> bool:
        return self.is_playing

    def get_is_recording(self) -> bool:
        return self.is_recording