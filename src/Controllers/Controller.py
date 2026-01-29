from .BeforeHome import *
import os

from .Home import *
from .Gaming import Gaming


class Controller:
    def __init__(self, project_path, screen, flag):
        self.project_path = project_path
        self.screen = screen
        self.flag = flag
        self.fader = Fade(screen, 0, True, 3, os.path.join(project_path, "image", "init", "作者logo.png"))
        self.loading = Loading(screen, project_path)
        self.ready2enter = Ready2Enter(screen, project_path)
        self.home = Home(screen, project_path)
        self.gaming = Gaming(screen, project_path, flag)


    def run(self, events):
        if self.flag == "Show Author" :
            self.flag = self.fader.run(self.flag)
        if self.flag == "Loading" :
            self.flag = self.loading.run(self.flag)
        if self.flag == "Ready to Enter" :
            self.flag = self.ready2enter.run(self.flag, events)
        if self.flag == "Home" :
            self.flag = self.home.run(self.flag, events)
        if self.flag == "Gaming" :
            self.flag = self.gaming.run(self.flag, events)
            if self.flag == "Home" :
                pygame.mixer.music.load(os.path.join(self.project_path, "audio", "home.mp3"))
                pygame.mixer.music.play()


    def show_flag(self):
        print(self.flag)
