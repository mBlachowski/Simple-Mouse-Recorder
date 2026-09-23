import threading
from threading import Thread

import keyboard
from PySide6.QtCore import Qt, QTranslator, qtTrId
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import (QMainWindow, QLabel, QMessageBox, QApplication, QHBoxLayout,
                               QVBoxLayout, QPushButton, QWidget, QCheckBox, QTimeEdit)

import settings as config
from recorder import Recorder


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):

        super().__init__()
        self.app = app
        self.settings = config.Settings()
        self.recorder = Recorder()
        self.user_prefs = self.settings.get_all_settings()
        self.keys_window = None
        self.setWindowTitle('Simple Mouse Recorder')
        self.setFixedSize(320,200)

        translator = QTranslator(self.app)

        if self.user_prefs['general']['lang']['pl']:
            translator.load('Localisation/lang_pl_PL')
        else:
            translator.load('Localisation/lang_en_US')
        self.app.installTranslator(translator)

        menubar = self.menuBar()
        file = menubar.addMenu(qtTrId('FILE_MENUBAR'))
        settings = menubar.addMenu(qtTrId('SETTINGS_MENUBAR'))


        self.theme_action_group = QActionGroup(self)
        self.theme_action_group.setExclusive(True)
        theme_menu = settings.addMenu(qtTrId('THEME_MENUBAR'))

        keyboard.add_hotkey(self.user_prefs['key_bindings']['start_recording'], lambda: self.start_recording_button())
        keyboard.add_hotkey(self.user_prefs['key_bindings']['stop_recording'], lambda: self.stop_recording_button())
        keyboard.add_hotkey(self.user_prefs['key_bindings']['stop_replay'], lambda: self.stop_playback_button())

        save = file.addAction(qtTrId('SAVE_MENUBAR'))
        save.triggered.connect(self.recorder.save_recording)

        load = file.addAction(qtTrId('LOAD_MENUBAR'))
        load.triggered.connect(self.load_menubar_button)

        t_sys = theme_menu.addAction(qtTrId('THEME_SYS_DEFAULT'))
        t_sys.setCheckable(True)
        t_sys.setChecked(self.user_prefs['general']['theme']['sys'])
        t_sys.setObjectName('sys')
        t_sys.triggered.connect(self.apply_theme)

        t_dark = theme_menu.addAction(qtTrId('THEME_DARK'))
        t_dark.setCheckable(True)
        t_dark.setChecked(self.user_prefs['general']['theme']['dark'])
        t_dark.setObjectName('dark')
        t_dark.triggered.connect(self.apply_theme)

        t_light = theme_menu.addAction(qtTrId('THEME_LIGHT'))
        t_light.setCheckable(True)
        t_light.setChecked(self.user_prefs['general']['theme']['light'])
        t_light.setObjectName('light')
        t_light.triggered.connect(self.apply_theme)

        self.theme_action_group.addAction(t_sys)
        self.theme_action_group.addAction(t_dark)
        self.theme_action_group.addAction(t_light)

        self.lang_action_group = QActionGroup(self)
        self.lang_action_group.setExclusive(True)
        lang_menu = settings.addMenu(qtTrId('LANG_MENUBAR'))

        l_en = lang_menu.addAction('&EN')
        l_en.setCheckable(True)
        l_en.setChecked(self.user_prefs['general']['lang']['en'])
        l_en.triggered.connect(self.apply_language)
        l_en.setObjectName('en')

        l_pl = lang_menu.addAction('&PL')
        l_pl.setCheckable(True)
        l_pl.setChecked(self.user_prefs['general']['lang']['pl'])
        l_pl.triggered.connect(self.apply_language)
        l_pl.setObjectName('pl')

        self.lang_action_group.addAction(l_en)
        self.lang_action_group.addAction(l_pl)

        settings.addSeparator()


        sos = settings.addAction(qtTrId('SOS_MENUBAR'))
        sos.setCheckable(True)
        sos.setChecked(self.user_prefs['general']['save_on_stop'])
        sos.triggered.connect(self.save_on_stop_checkbox)

        settings.addSeparator()

        key_b = settings.addAction(qtTrId('KEY_BINDINGS_MENUBAR'))
        key_b.triggered.connect(self.show_keybindings_window)

        info = menubar.addAction(qtTrId('ABOUT_MENUBAR'))
        info.triggered.connect(lambda: QMessageBox.information(self,qtTrId('ABOUT_MENUBAR'),
                        qtTrId('ABOUT_MESSAGE')))

        container = QWidget()
        self.setCentralWidget(container)
        self.main_vbox = QVBoxLayout(container)
        self.main_vbox.addStretch()

        self.misc_configurationHbox = QHBoxLayout()

        self.loop_checkbox = QCheckBox()
        self.loop_checkbox.setText(qtTrId('LOOP_CHECKBOX'))

        self.timeedit = QTimeEdit()
        self.timeedit.setDisplayFormat('hh:mm:ss')
        self.delay_label = QLabel()
        self.delay_label.setText(qtTrId('DELAY_LABEL_STRING'))

        self.misc_configurationHbox.addWidget(self.loop_checkbox)
        self.misc_configurationHbox.addWidget(self.delay_label)
        self.misc_configurationHbox.addWidget(self.timeedit)
        self.misc_configurationHbox.setStretch(0, True)

        self.record_btt_hbox = QHBoxLayout()
        self.start_recording_btt = QPushButton(qtTrId('START_RECORDING_BTT'))
        self.start_recording_btt.clicked.connect(self.start_recording_button)
        self.stop_recording_btt = QPushButton(qtTrId('STOP_RECORDING_BTT'))
        self.stop_recording_btt.clicked.connect(self.stop_recording_button)
        self.stop_recording_btt.setEnabled(False)

        self.record_btt_hbox.addWidget(self.start_recording_btt)
        self.record_btt_hbox.addWidget(self.stop_recording_btt)

        self.play_button_hbox = QHBoxLayout()
        self.play_button = QPushButton(qtTrId('REPLAY_BTT'))
        self.play_button.clicked.connect(self.play_recording_button)
        self.play_button_hbox.addWidget(self.play_button)

        self.stop_button_hbox = QHBoxLayout()
        self.stop_button = QPushButton(qtTrId('STOP_REPLAYING_BTT'))
        self.stop_button.clicked.connect(self.stop_playback_button)
        self.stop_button_hbox.addWidget(self.stop_button)

        self.curr_rt_hbox = QHBoxLayout()
        self.recording_title_label = QLabel()
        self.recording_title_label.setText(qtTrId('CURR_RECORDING_LABEL'))
        self.curr_rt_hbox.addWidget(self.recording_title_label)

        self.main_vbox.addLayout(self.misc_configurationHbox)
        self.main_vbox.addLayout(self.record_btt_hbox)
        self.main_vbox.addLayout(self.play_button_hbox)
        self.main_vbox.addLayout(self.stop_button_hbox)
        self.main_vbox.addLayout(self.curr_rt_hbox)

        self.apply_theme(save_prefs=False)
        self.show()


    def apply_theme(self, save_prefs: bool = True):
        for item in self.theme_action_group.actions():
            if item.isChecked():
                if item.objectName() == 'sys':
                    self.app.styleHints().setColorScheme(Qt.ColorScheme.Unknown)
                elif item.objectName() == 'dark':
                    self.app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
                elif item.objectName() == 'light':
                    self.app.styleHints().setColorScheme(Qt.ColorScheme.Light)

            self.user_prefs['general']['theme'][item.objectName()] = item.isChecked()
        if save_prefs:
            self.settings.save_settings(self.user_prefs)

    def apply_language(self, save_prefs: bool = True):
        for item in self.lang_action_group.actions():
            self.user_prefs['general']['lang'][item.objectName()] = item.isChecked()
        if save_prefs:
            self.settings.save_settings(self.user_prefs)
        QMessageBox.information(self,qtTrId('LANG_CHANGED_TITLE'),qtTrId('LANG_CHANGED_DESCRIPTION'))

    def save_on_stop_checkbox(self):
        self.user_prefs['general']['save_on_stop'] = False
        self.settings.save_settings(self.user_prefs)

    def show_keybindings_window(self):
        if not self.keys_window:
            self.keys_window = KeyConfigWindow(self, self.user_prefs)
            self.keys_window.destroyed.connect(self._clear_key_window_reference)
            # X position = keybind window initial x pos + main window width + 10px padding
            x_pos = self.keys_window.geometry().x() + (self.geometry().width() + 10)
            y_pos = self.keys_window.geometry().y()
            self.keys_window.setGeometry(x_pos, y_pos, self.keys_window.geometry().width(),
                                         self.keys_window.geometry().height()) # Set keybind window position
            self.keys_window.show()

    def _clear_key_window_reference(self):
        self.keys_window = None

    def start_recording_button(self):
        if not self.recorder.get_is_recording():
            self.recorder.record()
            self.start_recording_btt.setEnabled(False)
            self.stop_recording_btt.setEnabled(True)
            self.play_button.setEnabled(False)


    def stop_recording_button(self):
        if self.recorder.get_is_recording():
            self.play_button.setEnabled(True)
            self.start_recording_btt.setEnabled(True)
            self.stop_recording_btt.setEnabled(False)
            self.recorder.stop_recording()
            self.recording_title_label.setText(qtTrId('CURR_RECORDING_LABEL')+self.recorder.get_recording_name())
            if self.user_prefs['general']['save_on_stop']:
                self.recorder.save_recording()

    def play_recording_button(self):
        if not self.recorder.get_is_playing() or not self.recorder.get_is_recording():
            self.recorder.start_playback(self.timeedit.time().msecsSinceStartOfDay(), self.loop_checkbox.isChecked())

    def stop_playback_button(self):
        if self.recorder.get_is_playing():
            self.recorder.stop_playback()

    def load_menubar_button(self):
        self.recorder.load_recording()
        self.recording_title_label.setText(qtTrId('CURR_RECORDING_LABEL') + self.recorder.get_recording_name())

class KeyConfigWindow(QMainWindow):
    def __init__(self, parent:MainWindow, user_prefs:dict):
        super().__init__(parent, Qt.WindowType.Window)
        self.parent = parent
        self.setWindowTitle(qtTrId('KEY_BINDINGS_MENUBAR'))
        self.setFixedSize(350, 100)
        self.show()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.user_prefs = user_prefs

        container = QWidget()
        self.setCentralWidget(container)
        main_vbox = QVBoxLayout(container)
        main_vbox.addStretch()

        starthbox = QHBoxLayout()
        stophbox = QHBoxLayout()
        stopreplayhbox = QHBoxLayout()

        self.start_keys_label = QLabel(self)
        self.start_keys_label.setText(qtTrId('START_RECORDING_KEY_DESC')+self.user_prefs['key_bindings']['start_recording'])

        self.change_start_button = QPushButton(self)
        self.change_start_button.setText(qtTrId('CHANGE_HOTKEY_BTT'))
        self.change_start_button.clicked.connect(self.change_start_recording_keys)
        self.change_start_button.setObjectName('btt_start')
        self.change_start_button.setFixedWidth(130)

        starthbox.addWidget(self.start_keys_label)
        starthbox.addWidget(self.change_start_button)

        self.stop_keys_label = QLabel(self)
        self.stop_keys_label.setText(qtTrId('STOP_RECORDING_DESC')+self.user_prefs['key_bindings']['stop_recording'])


        self.change_stop_button = QPushButton(self)
        self.change_stop_button.setText(qtTrId('CHANGE_HOTKEY_BTT'))
        self.change_stop_button.clicked.connect(self.change_stop_recording_keys)
        self.change_stop_button.setObjectName('btt_stop')
        self.change_stop_button.setFixedWidth(130)


        stophbox.addWidget(self.stop_keys_label)
        stophbox.addWidget(self.change_stop_button)

        self.stop_replay_keys_label = QLabel(self)
        self.stop_replay_keys_label.setText(qtTrId('STOP_REPLAY_RECORDING_DESC') + self.user_prefs['key_bindings']['stop_replay'])

        self.change_stop_replay_button = QPushButton(self)
        self.change_stop_replay_button.setText(qtTrId('CHANGE_HOTKEY_BTT'))
        self.change_stop_replay_button.clicked.connect(self.change_stop_replay_keys)
        self.change_stop_replay_button.setObjectName('btt_stop_replay')
        self.change_stop_replay_button.setFixedWidth(130)

        stopreplayhbox.addWidget(self.stop_replay_keys_label)
        stopreplayhbox.addWidget(self.change_stop_replay_button)

        main_vbox.addLayout(starthbox)
        main_vbox.addLayout(stophbox)
        main_vbox.addLayout(stopreplayhbox)

    def change_start_recording_keys(self):
        self.start_keys_label.setText(qtTrId('START_RECORDING_KEY_DESC'))
        previous_text = self.start_keys_label.text()
        self.change_stop_button.setEnabled(False)
        self.change_start_button.setEnabled(False)
        self.change_stop_replay_button.setEnabled(False)
        keyboard.remove_hotkey(self.user_prefs['key_bindings']['start_recording'])
        thread = threading.Thread(target=lambda: self.record_hotkey(self.start_keys_label, previous_text,
                                                                    self.change_start_button.objectName()))
        thread.start()


    def change_stop_recording_keys(self):
        self.stop_keys_label.setText(qtTrId('STOP_RECORDING_DESC'))
        previous_text = self.stop_keys_label.text()
        self.change_stop_button.setEnabled(False)
        self.change_start_button.setEnabled(False)
        self.change_stop_replay_button.setEnabled(False)
        keyboard.remove_hotkey(self.user_prefs['key_bindings']['stop_recording'])
        thread = Thread(target=lambda: self.record_hotkey(self.stop_keys_label, previous_text,
                                                                    self.change_stop_button.objectName()))
        thread.start()

    def change_stop_replay_keys(self):
        self.stop_replay_keys_label.setText(qtTrId('STOP_REPLAY_RECORDING_DESC'))
        previous_text = self.stop_replay_keys_label.text()
        self.change_stop_button.setEnabled(False)
        self.change_start_button.setEnabled(False)
        self.change_stop_replay_button.setEnabled(False)
        keyboard.remove_hotkey(self.user_prefs['key_bindings']['stop_replay'])
        thread = Thread(target=lambda: self.record_hotkey(self.stop_replay_keys_label, previous_text,
                                                                    self.change_stop_replay_button.objectName()))
        thread.start()

    def record_hotkey(self, label:QLabel, prev_text:str, clicked_btt:str):
        hotkey = keyboard.read_hotkey(suppress=False)
        label.setText(prev_text+hotkey)

        if clicked_btt == 'btt_start':
            self.user_prefs['key_bindings']['start_recording'] = hotkey
            keyboard.add_hotkey(self.user_prefs['key_bindings']['start_recording'], lambda: self.parent.start_recording_button())
        elif clicked_btt == 'btt_stop':
            self.user_prefs['key_bindings']['stop_recording'] = hotkey
            keyboard.add_hotkey(self.user_prefs['key_bindings']['stop_recording'], lambda: self.parent.stop_recording_button())
        elif clicked_btt == 'btt_stop_replay':
            self.user_prefs['key_bindings']['stop_replay'] = hotkey
            keyboard.add_hotkey(self.user_prefs['key_bindings']['stop_replay'], lambda: self.parent.stop_playback_button())

        self.parent.user_prefs = self.user_prefs
        self.parent.settings.save_settings(self.user_prefs)

        self.change_stop_button.setEnabled(True)
        self.change_start_button.setEnabled(True)
        self.change_stop_replay_button.setEnabled(True)