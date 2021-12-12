"""Project"""

import pygame
import os
import time
import random
from pygame import mixer


# ------------------------------------------------------------------------------
#   Import File
# ------------------------------------------------------------------------------

#Display
pygame.font.init()
width, height = 700, 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("SpaceShip-Simulator")

#icon
icon = pygame.image.load(os.path.join("assets", "icon.png"))
pygame.display.set_icon(icon)

#Images
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_bg.jpg")), (width, height))
#           ^^^ตั้งค่าขนาดภาพbgให้พอดีกับdisplay                           ชื่อไฟล์BG^^^
menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "menu_bg.jpg")), (width, height))

#Ship
enemy_00 = pygame.image.load(os.path.join("assets", "enemy_flyer_sprite.png"))
enemy_01 = pygame.image.load(os.path.join("assets", "enemy_shooter_sprite.png"))
enemy_02 = pygame.image.load(os.path.join("assets", "enemy_Twin_sprite.png"))
player_ship = pygame.image.load(os.path.join("assets", "player_main_sprite.png"))

#Lasers
laser_00 = pygame.image.load(os.path.join("assets", "enemy_shooter_laser_sprite.png"))
laser_01 = pygame.image.load(os.path.join("assets", "enemy_shooter_laser_sprite.png"))
laser_02 = pygame.image.load(os.path.join("assets", "enemy_twin_laser_sprite.png"))
player_laser = pygame.image.load(os.path.join("assets", "player_laser_sprite.png"))

#BGM and SFX
pygame.mixer.init()
def bgm_mainmenu(): #เสียง BGM หน้า main menu
    pygame.mixer.music.load(os.path.join("BGMandSFX", "BGM_hortwire - Reconfig.ogg"))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

def bgm_game(): #เสียง BGM ในตัวเกม
    pygame.mixer.music.load(os.path.join("BGMandSFX", "BGM_unnamed. - Sundown.ogg"))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

laser_sfx = pygame.mixer.Sound("BGMandSFX/SFX_LaserBlastQuick PE1095107.ogg")

# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    cooldown_00 = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))# player ship
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):#เช็คว่าlaserออกนอกจอหรือป่าว
                self.lasers.remove(laser)#ถ้าหลุดออกนอกจอจะลบทิ้ง
            elif laser.collision(obj):#เช็คว่าโดนplayerไหม
                obj.health -= 10#ถ้าโดน ลดเลือดไป10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.cooldown_00:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            pygame.mixer.Sound.play(laser_sfx)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = player_ship
        self.laser_img = player_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    Enemy_match = {
                "00": (enemy_00, laser_00),
                "01": (enemy_01, laser_01),
                "02": (enemy_02, laser_02)
                }

    def __init__(self, x, y, number, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.Enemy_match[number]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):#แก้กระสุนชนhitbox
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None



# ------------------------------------------------------------------------------
#   Command & Menu
# ------------------------------------------------------------------------------

def main():
    """function display"""
    activate = True
    fps = 60
    level = 0
    miss = 10
    main_font = pygame.font.SysFont("Magneto", 40)
    lose_font = pygame.font.SysFont("Magneto", 50)
    bgm_game()

    enemies = []
    wave_length = 5
    enemy_vel = 1# enemy จะเคลื่อนที่ทีละ 1 pixel

    player_vel = 5# เมื่อเคลื่อนที่ playerจะย้ายไป 5 pixel
    laser_vel = 5

    player = Player(350, 650)# ตำแหน่งของplayer

    clock = pygame.time.Clock()

    lose = False
    lose_count = 0

    def bg_window():
        """set bg and text"""
        win.blit(bg, (0, 0))

        for enemy in enemies:
            enemy.draw(win)

        player.draw(win)

        if lose:#ถ้าแพ้เมื่อไหร่ จะแสดงข้อความนี้ ปรากฏตำแหน่งตามนี้
            lose_text = lose_font.render("You Lose!!", 1, (255, 255, 255))
            win.blit(lose_text, (width/2 - lose_text.get_width()/2, 350))

        # text
        miss_text = main_font.render(f"Missed: {miss}", 1, (255, 255, 255))
        level_text = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        #ตั้งค่าตำแหน่งของtext
        win.blit(miss_text, (10, 10))
        win.blit(level_text, (width - level_text.get_width() - 10, 10))

        pygame.display.update()

    while activate:
        clock.tick(fps)
        bg_window()

        if miss <= 0 or player.health <= 0:#ถ้า miss เป็น 0 จะแสดงผลว่าแพ้
            lose = True
            lose_count += 1

        if lose: #เมื่อหน้าจอขึ้นว่าแพ้เสร็จ จะกลับเข้าสู่หน้า menu
            if lose_count > fps*3:
                activate = False
                bgm_mainmenu()
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, width-100), random.randrange(-1500, -100), \
                    random.choice(["00", "01", "02"]))# สุ่ม enemy
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu()

        #set keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.y - player_vel > 0:# up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < height:# down
            player.y += player_vel
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:# left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < width:# right
            player.x += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > height:
                miss -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)#laser_velติดลบ เพื่อที่จะทำให้กระสุนไปด้านบน

def main_menu():
    """function mainmenu"""
    title_font = pygame.font.SysFont("Magneto", 40)
    menu_font = pygame.font.SysFont("Magneto", 48)
    bgm_mainmenu()
    activate = True

    while activate:
        win.blit(menu_bg, (0, 0))
        menu_text = menu_font.render("Main menu", 1, (255, 255, 255))
        win.blit(menu_text, (width/2 - menu_text.get_width()/2, 20))

        title_text = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        win.blit(title_text, (width/2 - title_text.get_width()/2, 600))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                activate = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
