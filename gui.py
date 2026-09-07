from email.mime import application

from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, QMessageBox, QHBoxLayout, QVBoxLayout,
                               QGroupBox, QRadioButton, QApplication)
from PySide6.QtCore import Qt, QTranslator
import settings as config

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):

        super().__init__()
        self.app = app
        settings = config.Settings()
        self.user_prefs = settings.get_all_settings()
        self.settings_window = None
        self.setWindowTitle('Mouse recorder')
        self.setFixedSize(300,200)

        label = QLabel('Hello World')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

        menubar = self.menuBar()
        settings = menubar.addMenu('&Settings')

        self.theme_action_group = QActionGroup(self)
        self.theme_action_group.setExclusive(True)
        theme_menu = settings.addMenu('&Theme')

        t_sys = theme_menu.addAction('System default')
        t_sys.setCheckable(True)
        t_sys.setChecked(self.user_prefs['general']['theme']['sys'])
        t_sys.setObjectName('sys')
        t_sys.triggered.connect(self.apply_theme)

        t_dark = theme_menu.addAction('&Dark')
        t_dark.setCheckable(True)
        t_dark.setChecked(self.user_prefs['general']['theme']['dark'])
        t_dark.setObjectName('dark')
        t_dark.triggered.connect(self.apply_theme)

        t_light = theme_menu.addAction('Light')
        t_light.setCheckable(True)
        t_light.setChecked(self.user_prefs['general']['theme']['light'])
        t_light.setObjectName('light')
        t_light.triggered.connect(self.apply_theme)

        self.theme_action_group.addAction(t_sys)
        self.theme_action_group.addAction(t_dark)
        self.theme_action_group.addAction(t_light)

        self.lang_action_group = QActionGroup(self)
        self.lang_action_group.setExclusive(True)
        lang_menu = settings.addMenu('&Language')

        l_en = lang_menu.addAction('&EN')
        l_en.setCheckable(True)
        l_en.setChecked(self.user_prefs['general']['lang']['en'])
        l_en.setObjectName('en')

        l_pl = lang_menu.addAction('&PL')
        l_pl.setCheckable(True)
        l_pl.setChecked(self.user_prefs['general']['lang']['pl'])
        l_pl.setObjectName('pl')

        self.lang_action_group.addAction(l_en)
        self.lang_action_group.addAction(l_pl)

        settings.addSeparator()
        sos = settings.addAction('&Save recording on stop')
        sos.setCheckable(True)
        sos.setChecked(self.user_prefs['general']['save_on_stop'])

        settings.addAction('&Key bindings')

        info = menubar.addAction('&About')
        info.triggered.connect(lambda: QMessageBox.information(self,'About',
                                                               'Simple Mouse Recorder created by Michał Blachowski.'
                                                               '\nVersion: 1.0\nUnder MIT license'))

        self.apply_theme()
        self.apply_language()
        self.show()

    def save_user_preferences(self):
        pass

    def apply_theme(self):
        for item in self.theme_action_group.actions():
            if item.isChecked():
                if item.objectName() == 'sys':
                    self.app.styleHints().setColorScheme(Qt.ColorScheme.Unknown)
                elif item.objectName() == 'dark':
                    self.app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
                elif item.objectName() == 'light':
                    self.app.styleHints().setColorScheme(Qt.ColorScheme.Light)

            self.user_prefs['general']['theme'][item.objectName()] = item.isChecked()
        self.save_user_preferences()

    def apply_language(self):
        for item in self.lang_action_group.actions():
            if item.isChecked():
                if item.objectName() == 'pl':
                    self.app.styleHints().setColorScheme(Qt.ColorScheme.Unknown)
                elif item.objectName() == 'en':
                    self.app.styleHints().setColorScheme(Qt.ColorScheme.Dark)

            self.user_prefs['general']['theme'][item.objectName()] = item.isChecked()
        self.save_user_preferences()

    #def show_settings(self):
    #    if self.settings_window is None:
    #        self.settings_window = SettingsWindow()

    #        self.settings_window.show()


#class SettingsWindow(QMainWindow):
#    def __init__(self):
#        super().__init__()
#        self.setWindowTitle('Settings')
#        self.setFixedSize(640, 480)
#        self.setWindowFlag(Qt.WindowType.SubWindow)
#
#        container = QWidget()
#        self.setCentralWidget(container)
#        layout = QHBoxLayout(container)
#
#
#        group_sys_start = QGroupBox()
#        group_sys_start.setTitle('Open on system start')
#        group_theme = QGroupBox()
#        group_theme.setTitle('Theme')
#        group_record_behavior = QGroupBox()
#        group_record_behavior.setTitle('Recorder behavior')
#        group_keys = QGroupBox()
#        group_keys.setTitle('Key bindings')
#
#        layout.addWidget(group_sys_start)
#        layout.addWidget(group_theme)
#        layout.addWidget(group_record_behavior)
#        layout.addWidget(group_keys)
