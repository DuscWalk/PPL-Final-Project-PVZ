import os.path
import sys
import pygame


class Home:
    def __init__(self, screen, project_path):
        self.screen = screen
        self.project_path = project_path
        self.bg_nonact = pygame.image.load(os.path.join(project_path, 'image\\start\\bg_nonact.png')).convert_alpha()
        self.bg_act = pygame.image.load(os.path.join(project_path, 'image\\start\\bg_act.png')).convert_alpha()
        self.bg_2exit = pygame.image.load(os.path.join(project_path, 'image\\start\\bg_2exit.png')).convert_alpha()

    def run(self, flag, events):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 420 <= mouse_x <= 720 and 90 <= mouse_y <= 200:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag = 'Gaming'
                    pygame.mixer.music.pause()
                    pygame.mixer.Sound(os.path.join(self.project_path, 'audio\\click\\enter.ogg')).play()
            self.screen.blit(self.bg_act, (0, 0))
        elif 715 <= mouse_x <= 775 and 510 <= mouse_y <= 550:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(self.bg_2exit, (0, 0))
        else:
            self.screen.blit(self.bg_nonact, (0, 0))
        return flag