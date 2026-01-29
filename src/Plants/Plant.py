import os
import math
import pygame

class Plant:
    """
    植物的父类
    """
    def __init__(self, project_path, screen, hp, atk, x, y, consumption, line):
        self.project_path = project_path
        self.screen = screen
        self.is_alive = True
        self.hp = hp
        self.atk = atk
        self.consumption = consumption
        self.line = line
        self.x = x
        self.y = y
        self.counter = 1

    def hurt(self, attack):
        self.hp -= attack
        if self.hp <= 0:
            self.is_alive = False

    def add_counter(self):
        self.counter += 1

class Peashooter(Plant):
    def __init__(self, project_path, screen, hp, atk, x, y, consumption, line):
        super().__init__(project_path, screen, hp, atk, x, y, consumption, line)
        self.image = pygame.image.load(os.path.join(project_path, "image", "Plants", "peashooter.png"))
        self.bullets = []
        self.frequency = 100
        self.shooting = False

    def shoot(self):
        bullet = Bullet(self.project_path, self.screen, self.atk, self.x + 50, self.y, self.line, 5)
        return bullet

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self, project_path, screen, atk, x, y, line, speed):
        self.project_path = project_path
        self.screen = screen
        self.atk = atk
        self.x = x
        self.y = y
        self.line = line
        self.speed = speed
        self.state = "flying"
        self.is_alive = True
        self.counter = 0
        self.image = pygame.image.load(os.path.join(project_path, "image", "Plants", "bullets.png"))
        self.image_splat = pygame.image.load(os.path.join(project_path, "image", "Plants", "splats.png"))

    def move(self):
        self.x += self.speed

    def splat(self):
        self.state = "splat"
        self.counter = 0

    def alive(self):
        return self.is_alive

    def draw(self):
        if self.state == "flying":
            self.screen.blit(self.image, (self.x, self.y))
        else:
            self.screen.blit(self.image_splat, (self.x, self.y))

    def add_counter(self):
        self.counter += 1

class WallNut(Plant):
    def __init__(self, project_path, screen, hp, atk, x, y, consumption, line):
        super().__init__(project_path, screen, hp, atk, x, y, consumption, line)
        self.original_hp = hp
        self.image = {}
        for i in range(1, 4):
            self.image[i] = pygame.image.load(os.path.join(project_path, "image", "Plants", f"wallnut_{i}.png"))

    def draw(self):
        if self.hp <= 0:
            img = self.image[3]
        else:
            img = self.image[min(self.original_hp // self.hp, 3)]
        self.screen.blit(img , (self.x, self.y))

class SunFlower(Plant):
    def __init__(self, project_path, screen, hp, atk, x, y, consumption, line):
        super().__init__(project_path, screen, hp, atk, x, y, consumption, line)
        self.image = pygame.image.load(os.path.join(project_path, "image", "Plants", "sunflower.png"))

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

class Sunshine:
    def __init__(self, project_path, screen, x, y, target_x, target_y, speed):
        self.project_path = project_path
        self.screen = screen
        self.is_alive = True
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.counter = 0
        self.image = pygame.image.load(os.path.join(project_path, "image", "Plants", "sun.png"))

    def move(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        if self.is_alive:
            factor = 0.008
            self.x += dx * factor
            self.y += dy * factor
            # 如果非常接近目标就停止（避免浮动）
            if abs(dx) < 1 and abs(dy) < 1:
                self.x, self.y = self.target_x, self.target_y
        else:
            # 计算距离
            dist = math.hypot(dx, dy)

            if dist > self.speed:
                # 单位向量移动
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
            else:
                # 如果距离小于一步，则直接到达目标避免抖动
                self.x, self.y = self.target_x, self.target_y

    def alive(self):
        return self.is_alive

    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y

    def set_speed(self, speed):
        self.speed = speed

    def reset_speed(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        self.speed = dist // 30

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

