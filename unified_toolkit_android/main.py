"""
Unified Security Toolkit — Android APK
Entry point: Kivy App + ScreenManager
"""

import os
# Disable Kivy logging verbosity
os.environ.setdefault('KIVY_LOG_LEVEL', 'warning')
os.environ.setdefault('KIVY_NO_ENV_CONFIG', '1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.utils import platform

# Set dark background
Window.clearcolor = (0.05, 0.05, 0.08, 1)

# Import screens
from screens.home_screen import HomeScreen
from screens.category_screen import CategoryScreen
from screens.tool_screen import ToolScreen
from screens.output_screen import OutputScreen
from screens.history_screen import HistoryScreen

# Initialize DB on startup
from utils.storage import init_db


class SecurityToolkitApp(App):
    title = "Security Toolkit"
    icon = "assets/icon.png"

    def build(self):
        init_db()

        self.sm = ScreenManager(transition=SlideTransition())

        # Register all screens
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(CategoryScreen(name='category'))
        self.sm.add_widget(ToolScreen(name='tool'))
        self.sm.add_widget(OutputScreen(name='output'))
        self.sm.add_widget(HistoryScreen(name='history'))

        return self.sm

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    SecurityToolkitApp().run()
