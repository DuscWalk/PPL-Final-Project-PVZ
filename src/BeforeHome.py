import os.path
import pygame

class Fade:
    def __init__(self, screen, alpha, fade_in, fade_speed, image):
        self.running = True
        self.screen = screen
        self.alpha = alpha
        self.fade_in = fade_in
        self.fade_speed = fade_speed
        self.img = pygame.image.load(image).convert_alpha()
        self.img.set_alpha(self.alpha)
        self.counter = 0

    def change_alpha(self):
        if self.fade_in:
            self.alpha += self.fade_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.fade_in = False
        else:
            if self.alpha == 255 and self.counter <= 80:
                self.counter += 1
            else:
                self.alpha -= self.fade_speed
                if self.alpha <= 0:
                    self.alpha = 0
                    self.running = False
        # print(self.alpha)
        self.img.set_alpha(self.alpha)

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.img.set_alpha(alpha)

    def is_running(self):
        return self.running

    def draw(self):
        self.screen.blit(self.img, (0, 30))

    def run(self, flag):
        self.change_alpha()
        self.draw()
        if not self.is_running():
            flag = 'Loading'
        return flag



class Loading:
    def __init__(self, screen, project_path):
        self.running = True
        self.screen = screen
        self.project_path = project_path
        self.counter = 0
        self.img_no = 1
        self.bar_images = {}
        self.scene = pygame.image.load(os.path.join(project_path,'image\\init\\load_scene.png')).convert_alpha()
        for i in range(1, 41):
            self.bar_images[i] = pygame.image.load(os.path.join(project_path,f'image\\init\loadbar\\{i}.png')).convert_alpha()

    def add(self):
        self.counter += 10
        self.img_no = self.counter // 20 + 1
        if self.img_no > 40:
            self.running = False

    def is_running(self):
        return self.running

    def draw(self):
        self.screen.blit(self.scene, (0, 0))
        self.screen.blit(self.bar_images[self.img_no if self.img_no < 41 else 40], (163, 353))

    def run(self, flag):
        self.draw()
        self.add()
        if not self.is_running():
            flag = 'Ready to Enter'
        return flag



class Ready2Enter:
    def __init__(self, screen, project_path):
        self.running = True
        self.screen = screen
        self.project_path = project_path
        self.scene_nonact = pygame.image.load(os.path.join(project_path,'image\\init\\ready2enter.png')).convert_alpha()
        self.scene_act = pygame.image.load(os.path.join(project_path,'image\\init\\ready2enter_act.png')).convert_alpha()

    def run(self, flag, events):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 245 <= mouse_x <= 540 and 455 <= mouse_y <= 485:
            self.screen.blit(self.scene_act, (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag = 'Home'
                    pygame.mixer.Sound(os.path.join(self.project_path,'audio\\click\\enter.ogg')).play()
        else:
            self.screen.blit(self.scene_nonact, (0, 0))
        return flag

