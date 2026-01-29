import pygame
import os

class Zombie:
    def __init__(self, project_path, screen, hp, atk, speed, x, y, line):
        self.project_path = project_path
        self.screen = screen
        self.is_alive = True
        self.hp = hp
        self.atk = atk
        self.speed = speed
        self.x = x
        self.y = y
        self.line = line
        self.image_walk = {}
        self.image_eat = {}
        self.state = 'walk'
        self.counter = 0
        for i in range(1, 6):
            self.image_walk[i] = pygame.image.load(os.path.join(project_path, f'image\\Zombies\\walk\\zombie_move{i}.png')).convert_alpha()
        for i in range(1, 8):
            self.image_eat[i] = pygame.image.load(os.path.join(project_path, f'image\\Zombies\\eat\\zombie_eat{i}.png')).convert_alpha()
        self.cur_image = self.image_walk[1]
        self.eating_obj = None

    def eat(self, plant):
        self.state = 'eat'
        self.counter = 0
        self.eating_obj = plant

    def walk(self):
        self.state = 'walk'
        self.counter = 0
        self.eating_obj = None

    def hurt(self, attack):
        self.hp -= attack
        if self.hp <= 0:
            self.is_alive = False

    def die(self):
        self.is_alive = False

    def alive(self):
        return self.is_alive

    def add_counter(self):
        self.counter += 1

    def draw(self):
        self.screen.blit(self.cur_image, (self.x, self.y))