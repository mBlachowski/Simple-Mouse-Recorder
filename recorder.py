from PySide6.QtCore import Signal, qtTrId, QDateTime
from PySide6.QtWidgets import QFileDialog
import pickle

class Recorder(object):
    def __init__(self, parent=None):
        self.parent = parent #  Only for File dialogs
        self.is_recording:bool = False
        self.recorded_events:list = []
        self.recording_name:str = ''

    def record(self):
        self.is_recording = True

    def stop_recording(self):
        self.is_recording = False

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

    def start_playback(self):
        pass

    def stop_playback(self):
        pass

    def get_recorded_events(self) -> list:
        return self.recorded_events

    def get_recording_name(self) -> str:
        return self.recording_name
