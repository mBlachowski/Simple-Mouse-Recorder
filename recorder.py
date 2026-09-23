
import multiprocessing as mp
import mouse
import pickle
from PySide6.QtCore import Signal, qtTrId, QDateTime, QTimer,QObject
from PySide6.QtWidgets import QFileDialog

class Recorder(QObject):
    replay_stopped = Signal()
    def __init__(self,):
        super().__init__()
        self.recorded_events:list = []
        self.recording_name:str = ''
        self.is_recording = False
        self.is_playing = False
        self._current_playback_process:mp.Process = None

    def record(self):
        mouse.hook(self._get_recorded_event)
        self.is_recording = True

    def stop_recording(self):
        mouse.unhook(self._get_recorded_event)
        self.recording_name = 'Recording ' + QDateTime.currentDateTime().toString()
        self.is_recording = False

    def _get_recorded_event(self, event):
        self.recorded_events.append(event)

    def save_recording(self):
        if self.recorded_events:
            filename = QFileDialog.getSaveFileName(None, qtTrId('SAVE_AS_DIALOG_TITLE'),
                                                   self.recording_name.replace(':', ';'), '*.smrrec')
            if not filename[0] == '':
                with open(filename[0], 'wb') as record_file:
                    pickle.dump(self.recorded_events, record_file)

    def load_recording(self):
        filename = QFileDialog.getOpenFileName(None, qtTrId('OPEN_DIALOG_TITLE'), '', '*.smrrec')
        if not filename[0] == '':
            with open(filename[0], 'rb') as record_file:
                self.recorded_events = pickle.load(record_file)
                self.recording_name = filename[0].split('/')[-1]


    def start_playback(self, delay:int = 0, loop:bool = False):
        process = mp.Process(target= mouse.play, args=[self.recorded_events])
        self._current_playback_process = process
        timer = QTimer()
        timer.setSingleShot(not loop)
        timer.setInterval(delay)
        timer.timeout.connect(lambda: self._current_playback_process.start())
        self.replay_stopped.connect(lambda: timer.stop)
        timer.start()
        self.is_playing = True

    def stop_playback(self):
        if self._current_playback_process.is_alive():
            self._current_playback_process.terminate()
        else:
            self.replay_stopped.emit()
        self.is_playing = False

    def get_recorded_events(self) -> list:
        return self.recorded_events

    def get_recording_name(self) -> str:
        return self.recording_name

    def get_is_playing(self) -> bool:
        return self.is_playing

    def get_is_recording(self) -> bool:
        return self.is_recording