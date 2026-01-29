import pygame
import sys
import random
from Zombies.Zombie import *
from Plants.Plant import *

class PlantManager:
    def __init__(self, project_path, screen):
        self.project_path = project_path
        self.screen = screen
        self.plants = []
        self.peashooters = []
        self.sunflowers = []
        self.bullets = []
        self.suns = []
        self.next_plant = "None"
        self.for_moving = {
            "peashooter": pygame.image.load(os.path.join(project_path, "image", "Plants", "peashooter.png")),
            "wallnut": pygame.image.load(os.path.join(project_path, "image", "Plants", "wallnut_1.png")),
            "sunflower": pygame.image.load(os.path.join(project_path, "image", "Plants", "sunflower.png")),
            "sun": pygame.image.load(os.path.join(project_path, "image", "Plants", "sun.png")),
        }
        self.counter = 0
        self.sunshine = 50

    def gen_sun(self):
        if self.counter % 600 == 0:
            x = random.randint(60, self.screen.get_width() - 60)
            y = 80
            target_x = x
            target_y = random.randint(120, self.screen.get_height() - 60)
            sun = Sunshine(self.project_path, self.screen, x, y, target_x, target_y, 8)
            self.suns.append(sun)
        if self.sunflowers:
            for flower in self.sunflowers:
                flower.add_counter()
                if flower.counter % 1600 == 0:
                    x = flower.x + 15
                    y = flower.y + 30
                    target_x = x + 30
                    target_y = y - 50
                    sun = Sunshine(self.project_path, self.screen, x, y, target_x, target_y, 8)
                    self.suns.append(sun)

    def genFollower(self, x, y):
        ret = None
        if 77 <= x <= 126 and 7 <= y <= 77:
            if  self.sunshine >= 100:
                self.next_plant = "peashooter"
                ret = self.for_moving["peashooter"]
            else:
                pygame.mixer.Sound(os.path.join(self.project_path, "audio", "click", "buzzer.ogg")).play()
        if 127 <= x <= 176 and 7 <= y <= 77:
            if self.sunshine >= 50:
                self.next_plant = "wallnut"
                ret = self.for_moving["wallnut"]
            else:
                pygame.mixer.Sound(os.path.join(self.project_path, "audio", "click", "buzzer.ogg")).play()
        if 177 <= x <= 226 and 7 <= y <= 77:
            if self.sunshine >= 50:
                self.next_plant = "sunflower"
                ret = self.for_moving["sunflower"]
            else:
                pygame.mixer.Sound(os.path.join(self.project_path, "audio", "click", "buzzer.ogg")).play()
        return ret

    def pick_sun(self, x, y):
        w, h = self.for_moving["sun"].get_size()
        if self.suns:
            for sun in self.suns:
                if sun.x <= x <= sun.x + w and sun.y <= y <= sun.y + h and sun.alive():
                    return sun
        return None

    def add_plant(self, pos):
        plant_x, plant_y, plant_line = pos[0], pos[1], pos[2]
        if self.next_plant == "peashooter":
            shooter = Peashooter(self.project_path, self.screen, 270, 20, plant_x, plant_y, 100, plant_line)
            self.peashooters.append(shooter)
            self.plants.append(shooter)
            self.sunshine -= 100
        if self.next_plant == "wallnut":
            wallnut = WallNut(self.project_path, self.screen, 4000, 0, plant_x, plant_y, 50, plant_line)
            self.plants.append(wallnut)
            self.sunshine -= 50
        if self.next_plant == "sunflower":
            sunflower = SunFlower(self.project_path, self.screen, 270, 0, plant_x, plant_y, 50, plant_line)
            self.plants.append(sunflower)
            self.sunflowers.append(sunflower)
            self.sunshine -= 50

    def draw_plants(self):
        for plant in self.plants:
            plant.draw()

    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw()

    def draw_suns(self):
        for sun in self.suns:
            sun.draw()

    def add_counter(self):
        self.counter += 1


class ZombieManager:
    def __init__(self, project_path, screen):
        self.project_path = project_path
        self.screen = screen
        self.zombies = []
        self.counter = 800
        self.gen_frequency = 1800
        self.total_zombies = 20
        self.generated_zombies = 0
        self.killed_zombies = 0

    def gen_zombie(self):
        if (not self.counter % self.gen_frequency == 0) or self.generated_zombies >= self.total_zombies:
            return None
        line = random.randint(1, 5)
        zombie = Zombie(self.project_path, self.screen, 270, 48, 0.18, 800, line*95 - 90, line)
        self.zombies.append(zombie)
        self.generated_zombies += 1
        if self.generated_zombies == 1:
            pygame.mixer.Sound(os.path.join(self.project_path, "audio", "zombies", "zombies_coming.ogg")).play()
        return zombie

    def add_counter(self):
        self.counter += 1

    def draw_zombies(self):
        for zombie in self.zombies:
            zombie.draw()


class Gaming:
    def __init__(self, screen, project_path, flag):
        self.screen = screen
        self.project_path = project_path
        self.flag = flag
        self.counter = 0
        self.mouse_pickup = False
        self.follower = None
        self.images = {
            "background": pygame.image.load(os.path.join(project_path, "image", "gaming", "main_background.jpg")).convert(),
            "seedbank": pygame.image.load(os.path.join(project_path, "image", "gaming", "seedbank.png")).convert_alpha(),
            "peashooter_packet": pygame.image.load(os.path.join(project_path, "image", "Plants", "PeaShooterPacket.png")).convert_alpha(),
            "wallnut_packet": pygame.image.load(os.path.join(project_path, "image", "Plants", "NutWallPacket.png")).convert_alpha(),
            "sunflower_packet": pygame.image.load(os.path.join(project_path, "image", "Plants", "SunflowerPacket.png")).convert_alpha(),
            "win": pygame.image.load(os.path.join(project_path, "image", "gaming", "win.png")).convert_alpha(),
            "lose": pygame.image.load(os.path.join(project_path, "image", "gaming", "lose.png")).convert_alpha(),
            "Ready": pygame.image.load(os.path.join(project_path, "image", "gaming", "ready", "Ready.png")).convert_alpha(),
            "Set": pygame.image.load(os.path.join(project_path, "image", "gaming", "ready", "Set.png")).convert_alpha(),
            "Plant": pygame.image.load(os.path.join(project_path, "image", "gaming", "ready", "Plant.png")).convert_alpha()
        }
        self.sounds = {
            "packet_pickup": pygame.mixer.Sound(os.path.join(project_path, "audio", "plants", "packet_pickup.ogg")),
            "packet_putdown": pygame.mixer.Sound(os.path.join(project_path, "audio", "plants", "packet_putdown.ogg")),
            "hit": pygame.mixer.Sound(os.path.join(project_path, "audio", "plants", "hit.ogg")),
            "chomp": pygame.mixer.Sound(os.path.join(project_path, "audio", "zombies", "chomp.ogg")),
            "gulp": pygame.mixer.Sound(os.path.join(project_path, "audio", "zombies", "gulp.ogg")),
        }
        self.plant_manager = PlantManager(self.project_path, self.screen)
        self.zombie_manager = ZombieManager(self.project_path, self.screen)
        self.state = "Ready"
        """
        "Ready": 准备阶段
        "Running": 游戏正在进行
        "Win": 玩家胜利，钱袋未点击
        "Winning": 玩家胜利，钱袋已点击
        "Lose": 玩家失败
        """
        self.checker = {
            "win_x": 0,
            "win_y": 0
        }
    def add_counter(self):
        self.counter += 1

    def get_grid_pos(self, x, y):
        return (x+25) // 80 * 80 - 25, y // 95 * 95 , y // 95

    def draw_bg(self):
        self.screen.blit(self.images["background"], (-200, 0))

    def draw_seedbank(self):
        self.screen.blit(self.images["seedbank"], (0, 0))
        self.screen.blit(self.images["peashooter_packet"], (77, 7))
        self.screen.blit(self.images["wallnut_packet"], (127, 7))
        self.screen.blit(self.images["sunflower_packet"], (177, 7))

    def peashooters_shoot(self):
        for peashooter in self.plant_manager.peashooters:
            peashooter.add_counter()
            flag = False
            for zombie in self.zombie_manager.zombies:
                if zombie.alive() and peashooter.line == zombie.line and peashooter.x - zombie.x <= 60:
                    flag = True
                    break
            if flag:
                if not peashooter.shooting:
                    peashooter.shooting = True
                    peashooter.counter = 0
                if peashooter.counter % peashooter.frequency == 0:
                    bullet = peashooter.shoot()
                    self.plant_manager.bullets.append(bullet)
            else:
                peashooter.shooting = False

    def bullets_update(self):
        for i in range(len(self.plant_manager.bullets) - 1, -1, -1):
            bullet = self.plant_manager.bullets[i]
            bullet.add_counter()
            if bullet.state == "flying":
                for zombie in self.zombie_manager.zombies:
                    if zombie.alive() and bullet.line == zombie.line and 20 <= bullet.x - zombie.x <= 120:
                        bullet.splat()
                        self.sounds["hit"].play()
                        zombie.hurt(bullet.atk)
                if bullet.state == "flying":
                    bullet.move()
            if bullet.state == "splat":
                if bullet.counter >= 10:
                    bullet.is_alive = False
                    del self.plant_manager.bullets[i]

    def plants_update(self):
        for i in range(len(self.plant_manager.plants) - 1, -1, -1):
            plant = self.plant_manager.plants[i]
            if not plant.is_alive:
                del self.plant_manager.plants[i]
                if isinstance(plant, Peashooter):
                    self.plant_manager.peashooters.remove(plant)
                elif isinstance(plant, SunFlower):
                    self.plant_manager.sunflowers.remove(plant)

    def suns_update(self):
        for i in range(len(self.plant_manager.suns) - 1, -1, -1):
            sun = self.plant_manager.suns[i]
            if not sun.is_alive and (sun.x, sun.y) == (sun.target_x, sun.target_y):
                del self.plant_manager.suns[i]
                self.plant_manager.sunshine += 25
            else:
                sun.move()

    def zombie_update(self):
        if not self.zombie_manager.zombies:
            return
        for i in range(len(self.zombie_manager.zombies) - 1, -1, -1):
            zombie = self.zombie_manager.zombies[i]
            zombie.add_counter()
            if zombie.state == "walk":
                zombie.x -= zombie.speed
                t = zombie.counter // 30
                zombie.cur_image = zombie.image_walk[t % 5 + 1]
                for plant in self.plant_manager.plants:
                    if plant.line == zombie.line and -35 <= plant.x - zombie.x <= 60:
                        zombie.eat(plant)
                        break
                if zombie.x <= -30:
                    self.state = "Lose"
                    pygame.mixer.music.load(os.path.join(self.project_path, "audio", "lose.mp3"))
                    pygame.mixer.music.play()
                    self.counter = 0
            if zombie.state == "eat":
                t = zombie.counter // 12
                zombie.cur_image = zombie.image_eat[t % 7 + 1]
                if zombie.counter % 84 == 0:
                    zombie.eating_obj.hurt(zombie.atk)
                    if not zombie.eating_obj.is_alive:
                        self.sounds["gulp"].play()
                        zombie.walk()
                if zombie.counter % 42 == 0:
                    self.sounds["chomp"].play()

            if not zombie.alive():
                del self.zombie_manager.zombies[i]
                self.zombie_manager.killed_zombies += 1
                if self.zombie_manager.killed_zombies == 2:
                    self.zombie_manager.gen_frequency = 800
                elif self.zombie_manager.killed_zombies == self.zombie_manager.total_zombies // 5:
                    self.zombie_manager.gen_frequency = 500
                elif self.zombie_manager.killed_zombies == self.zombie_manager.total_zombies // 3 * 2:
                    self.zombie_manager.gen_frequency = 30
                if self.zombie_manager.killed_zombies == self.zombie_manager.total_zombies:
                    self.state = "Win"
                    self.counter = 0
                    self.checker["win_x"] = zombie.x
                    self.checker["win_y"] = zombie.y + 50


    def show_killing_counter(self):
        BLACK = (0, 0, 0)
        font = pygame.font.SysFont(None, 36)
        text = f"{self.zombie_manager.killed_zombies} / {self.zombie_manager.total_zombies}"
        text_surface = font.render(text, True, BLACK)
        self.screen.blit(text_surface, (710, 575))

    def show_sunshine(self):
        BLACK = (0, 0, 0)
        font = pygame.font.SysFont(None, 24)
        text = f"{self.plant_manager.sunshine}"
        text_surface = font.render(text, True, BLACK)
        self.screen.blit(text_surface, (20, 65))


    def get_moneybag_position(self, x, y):
        WIDTH, HEIGHT = 800, 600
        factor = 0.03
        img_rect = self.images["win"].get_rect()
        target_x = WIDTH // 2 - img_rect.width // 2
        target_y = HEIGHT // 2 - img_rect.height // 2
        dx = target_x - x
        dy = target_y - y
        x += dx * factor
        y += dy * factor
        # 如果非常接近目标就停止（避免浮动）
        if abs(dx) < 2 and abs(dy) < 2:
            x, y = target_x, target_y
        return x, y

    def check_end(self, flag):
        if self.state == "Running":
            return flag
        if self.state == "Win":
            self.screen.blit(self.images["win"], (self.checker["win_x"], self.checker["win_y"]))
            return flag
        if self.state == "Winning":
            self.checker["win_x"], self.checker["win_y"] = self.get_moneybag_position(self.checker["win_x"], self.checker["win_y"])
            orig_width, orig_height = self.images["win"].get_size()
            target_width = min(orig_width + self.counter // 6, orig_width + 32)
            scale_ratio = target_width / orig_width
            target_height = int(orig_height * scale_ratio)
            img_scaled = pygame.transform.scale(self.images["win"], (target_width, target_height))
            self.screen.blit(img_scaled, (self.checker["win_x"], self.checker["win_y"]))
            if self.counter >= 300:
                self.__init__(self.screen, self.project_path, self.flag)
                return "Home"
        if self.state == "Lose":
            surface = self.screen.copy()
            flag = self.lose(surface)
        return flag

    def lose(self, surface):
        clock = pygame.time.Clock()
        cnt = 0
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(surface, (0, 0))
            if cnt == 300:
                pygame.mixer.music.load(os.path.join(self.project_path, "audio", "scream.mp3"))
                pygame.mixer.music.play()
            if cnt >= 300:
                img = self.images["lose"]
                w, h = img.get_size()
                self.screen.blit(img, (400 - w//2, 300 - h//2))
            pygame.display.update()
            cnt += 1
            if cnt >= 550:
                break
            clock.tick(60)
        self.__init__(self.screen, self.project_path, self.flag)
        return "Home"

    def ready(self):
        if self.counter == 20:
            pygame.mixer.music.load(os.path.join(self.project_path, "audio", "ready", "Ready.mp3"))
            pygame.mixer.music.play()
        if self.counter == 60:
            pygame.mixer.music.load(os.path.join(self.project_path, "audio", "ready", "Set.mp3"))
            pygame.mixer.music.play()
        if self.counter == 100:
            pygame.mixer.music.load(os.path.join(self.project_path, "audio", "ready", "Plant.mp3"))
            pygame.mixer.music.play()
        img = None
        if 20 <= self.counter <= 45:
            img = self.images["Ready"]
        if 60 <= self.counter <= 85:
            img = self.images["Set"]
        if 100 <= self.counter <= 125:
            img = self.images["Plant"]
        if self.counter > 260:
            self.state = "Running"
            pygame.mixer.music.load(os.path.join(self.project_path, "audio", "grasswalk.mp3"))
            pygame.mixer.music.play(-1)
        if img is not None:
            x, y = img.get_size()
            self.screen.blit(img, (400 - x // 2, 300 - y // 2))



    def run(self, flag, events):
        self.draw_bg()
        self.draw_seedbank()

        self.add_counter()

        if self.state == "Ready":
            self.ready()
            return flag
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "Win":
                    self.state = "Winning"
                    pygame.mixer.music.load(os.path.join(self.project_path, "audio", "win.mp3"))
                    pygame.mixer.music.play()
                    self.counter = 0
                    break
                if not self.mouse_pickup:
                    self.follower = self.plant_manager.genFollower(mouse_x, mouse_y)
                    if self.follower:
                        self.mouse_pickup = True
                        self.sounds["packet_pickup"].play()
                    sun = self.plant_manager.pick_sun(mouse_x, mouse_y)
                    if sun:
                        sun.is_alive = False
                        sun.set_target(30, 30)
                        sun.reset_speed()
                        pygame.mixer.Sound(os.path.join(self.project_path, "audio", "plants", "points.ogg")).play()
                else:
                    if 55 <= mouse_x <= 774 and 95 <= mouse_y <= 569:
                        #能够确保所有植物都种在格子中
                        self.plant_manager.add_plant(self.get_grid_pos(mouse_x, mouse_y))
                        self.sounds["packet_putdown"].play()
                    self.mouse_pickup = False


        self.plant_manager.draw_plants()
        if self.mouse_pickup:
            self.screen.blit(self.follower, (mouse_x-23, mouse_y-35))

        self.peashooters_shoot()
        self.plant_manager.gen_sun()
        self.bullets_update()
        self.plants_update()
        self.suns_update()

        self.zombie_manager.gen_zombie()
        self.zombie_update()

        self.zombie_manager.draw_zombies()
        self.plant_manager.draw_bullets()
        self.plant_manager.draw_suns()

        self.zombie_manager.add_counter()
        self.plant_manager.add_counter()

        self.show_killing_counter()
        self.show_sunshine()
        flag = self.check_end(flag)
        return flag


