from unittest import signals

import keyboard
import threading

from PySide6 import QtCore
from PySide6.QtCore import Qt, QTranslator, QLocale, Signal
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import (QMainWindow, QLabel, QMessageBox, QApplication, QHBoxLayout,
                               QVBoxLayout, QPushButton, QWidget)

import settings as config


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):

        super().__init__()
        self.app = app
        self.settings = config.Settings()
        self.user_prefs = self.settings.get_all_settings()
        self.keys_window = None
        self.setWindowTitle('Simple Mouse Recorder')
        self.setFixedSize(300,200)

        if not self.user_prefs['general']['lang']['en']:
            translator = QTranslator(self.app)
            if translator.load(f'Localisation/lang_{QLocale().name()}'):
                self.app.installTranslator(translator)

        label = QLabel('Hello World')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

        menubar = self.menuBar()
        settings = menubar.addMenu(self.tr('Settings'))

        self.theme_action_group = QActionGroup(self)
        self.theme_action_group.setExclusive(True)
        theme_menu = settings.addMenu(self.tr('Theme'))

        keyboard.add_hotkey(self.user_prefs['key_bindings']['start_recording'], lambda: self.start_recording())
        keyboard.add_hotkey(self.user_prefs['key_bindings']['stop_recording'], lambda: self.stop_recording())

        t_sys = theme_menu.addAction(self.tr('System default'))
        t_sys.setCheckable(True)
        t_sys.setChecked(self.user_prefs['general']['theme']['sys'])
        t_sys.setObjectName('sys')
        t_sys.triggered.connect(self.apply_theme)

        t_dark = theme_menu.addAction(self.tr('Dark'))
        t_dark.setCheckable(True)
        t_dark.setChecked(self.user_prefs['general']['theme']['dark'])
        t_dark.setObjectName('dark')
        t_dark.triggered.connect(self.apply_theme)

        t_light = theme_menu.addAction(self.tr('Light'))
        t_light.setCheckable(True)
        t_light.setChecked(self.user_prefs['general']['theme']['light'])
        t_light.setObjectName('light')
        t_light.triggered.connect(self.apply_theme)

        self.theme_action_group.addAction(t_sys)
        self.theme_action_group.addAction(t_dark)
        self.theme_action_group.addAction(t_light)

        self.lang_action_group = QActionGroup(self)
        self.lang_action_group.setExclusive(True)
        lang_menu = settings.addMenu(self.tr('Language'))

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
        sos = settings.addAction(self.tr('Save recording on stop'))
        sos.setCheckable(True)
        sos.setChecked(self.user_prefs['general']['save_on_stop'])
        sos.triggered.connect(self.save_on_stop)

        key_b = settings.addAction(self.tr('Key bindings'))
        key_b.triggered.connect(self.show_keybindings_window)

        info = menubar.addAction(self.tr('About'))
        info.triggered.connect(lambda: QMessageBox.information(self,self.tr('About'),
                        'Simple Mouse Recorder created by Michał Blachowski.\nVersion: 1.0\nUnder MIT license'))

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
        QMessageBox.information(self,self.tr('Language changed'),self.tr('Restart application to apply changes.'))

    def save_on_stop(self):
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

    def start_recording(self):
        print('Start Recording')

    def stop_recording(self):
        print('Stop Recording')

class KeyConfigWindow(QMainWindow):
    def __init__(self, parent:MainWindow, user_prefs:dict):
        super().__init__(parent, Qt.WindowType.Window)
        self.parent = parent
        self.setWindowTitle('Key bindings')
        self.setFixedSize(300, 200)
        self.show()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.user_prefs = user_prefs

        container = QWidget()
        self.setCentralWidget(container)
        main_vbox = QVBoxLayout(container)

        starthbox = QHBoxLayout()
        stophbox = QHBoxLayout()

        #ToDo Fix Translation
        self.start_keys_label = QLabel(self)
        self.start_keys_label.setText('Start Recording:'+self.user_prefs['key_bindings']['start_recording'])

        self.change_start_button = QPushButton(self)
        self.change_start_button.setText('Change')
        self.change_start_button.clicked.connect(self.change_start_recording_keys)
        self.change_start_button.setObjectName('btt_start')


        starthbox.addWidget(self.start_keys_label)
        starthbox.addWidget(self.change_start_button)

        self.stop_keys_label = QLabel(self)
        self.stop_keys_label.setText('Stop Recording:'+self.user_prefs['key_bindings']['stop_recording'])


        self.change_stop_button = QPushButton(self)
        self.change_stop_button.setText('Change')
        self.change_stop_button.clicked.connect(self.change_stop_recording_keys)
        self.change_stop_button.setObjectName('btt_stop')

        stophbox.addWidget(self.stop_keys_label)
        stophbox.addWidget(self.change_stop_button)

        main_vbox.addLayout(starthbox)
        main_vbox.addLayout(stophbox)

    def change_start_recording_keys(self):
        self.start_keys_label.setText(self.tr('Start Recording:'))
        previous_text = self.start_keys_label.text()

        self.change_stop_button.setEnabled(False)
        self.change_start_button.setEnabled(False)
        thread = threading.Thread(target=lambda: self.record_hotkey(self.start_keys_label, previous_text,
                                                                    self.change_start_button.objectName()))
        thread.start()


    def change_stop_recording_keys(self):
        self.stop_keys_label.setText(self.tr('Stop Recording:'))
        previous_text = self.stop_keys_label.text()

        self.change_stop_button.setEnabled(False)
        self.change_start_button.setEnabled(False)

        thread = threading.Thread(target=lambda: self.record_hotkey(self.stop_keys_label, previous_text,
                                                                    self.change_stop_button.objectName()))
        thread.start()

    def record_hotkey(self, label:QLabel, prev_text:str, clicked_btt:str):
        hotkey = keyboard.read_hotkey(suppress=False)
        label.setText(prev_text+hotkey)

        if clicked_btt == 'btt_start':
            keyboard.remove_hotkey(self.user_prefs['key_bindings']['start_recording'])
            self.user_prefs['key_bindings']['start_recording'] = hotkey
            keyboard.add_hotkey(self.user_prefs['key_bindings']['start_recording'], self.parent.start_recording)
        elif clicked_btt == 'btt_stop':
            keyboard.remove_hotkey(self.user_prefs['key_bindings']['stop_recording'])
            self.user_prefs['key_bindings']['stop_recording'] = hotkey
            keyboard.add_hotkey(self.user_prefs['key_bindings']['stop_recording'], self.parent.stop_recording)

        self.parent.user_prefs = self.user_prefs
        self.parent.settings.save_settings(self.user_prefs)

        self.change_stop_button.setEnabled(True)
        self.change_start_button.setEnabled(True)