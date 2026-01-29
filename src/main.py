from Controllers.Controller import *
import pygame
import os
import sys


# 获取项目路径
if getattr(sys, "frozen", False):
    # PyInstaller EXE
    project_path = sys._MEIPASS
else:
    # Python 开发阶段
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Plants vs Zombies")


flag = "Show Author"
pygame.mixer.music.load(os.path.join(project_path, "audio", "home.mp3"))
pygame.mixer.music.play(-1)

controller = Controller(project_path, screen, flag)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    print(f"鼠标位置: ({mouse_x}, {mouse_y})")

    screen.fill((0, 0, 0))
    controller.run(events)


    pygame.display.update()
    clock.tick(60)