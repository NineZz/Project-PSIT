"""Project"""

import pygame
import os
import time
import random

#Display
pygame.font.init()
width, height = 750, 750
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
laser_00 = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
laser_01 = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
laser_02 = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
player_laser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
# name = pygame.image.load(os.path.join("assets", "icon.jpg"))

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))# player ship

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

class Enemy(Ship):
    Enemy_match = {"00": (enemy_00, laser_00),
                 "01": (enemy_01, laser_01),
                 "02": (enemy_02, laser_02)}

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.Enemy_match[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

def main():
    """function display"""
    activate = True
    fps = 60
    level = 0
    miss = 3
    main_font = pygame.font.SysFont("Magneto", 40)

    enemies = []
    wave_length = 5
    enemy_vel = 1# enemy จะเคลื่อนที่ทีละ 1 pixel

    player_vel = 5# เมื่อเคลื่อนที่ playerจะย้ายไป 5 pixel

    player = Player(350, 650)# ตำแหน่งของplayer

    clock = pygame.time.Clock()

    def bg_window():
        """set bg and text"""
        win.blit(bg, (0, 0))

        for enemy in enemies:
            enemy.draw(win)

        player.draw(win)

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

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, width-100), random.randrange(-1500, -100), \
                    random.choice(["00", "01", "02"]))# สุ่ม enemy
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                activate = False

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

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

def main_menu():
    """function mainmenu"""
    title_font = pygame.font.SysFont("Magneto", 40)
    menu_font = pygame.font.SysFont("Magneto", 48)
    activate = True

    while activate:
        win.blit(menu_bg, (0, 0))
        menu_text = menu_font.render("Main menu", 1, (255, 255, 255))
        win.blit(menu_text, (width/2 - menu_text.get_width()/2, 20))

        title_text = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        win.blit(title_text, (width/2 - title_text.get_width()/2, 700))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                activate = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
