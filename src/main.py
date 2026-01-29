import sys

from Controller import *
import pygame
import os


project_path = "D:\\!NJU\\ppl\\final_project"
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('Plants vs Zombies')


flag = 'Show Author'
pygame.mixer.music.load(os.path.join(project_path, 'audio\\home.mp3'))
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