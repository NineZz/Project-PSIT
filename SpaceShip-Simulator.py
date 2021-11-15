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
# icon = pygame.image.load(os.path.join("assets", "icon.jpg"))
# pygame.display.set_icon(icon)

#Images
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_bg.jpg")), (width, height))
#           ^^^ตั้งค่าขนาดภาพbgให้พอดีกับdisplay                           ชื่อไฟล์BG^^^
menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "menu_bg.jpg")), (width, height))

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
        pygame.draw.rect(window, (255, 255, 255), (self.x, self.y, 70, 70))# test the player ship

def main():
    """function display"""
    activate = True
    fps = 60
    level = 1
    miss = 3
    main_font = pygame.font.SysFont("Magneto", 40)

    player_vel = 5# เมื่อเคลื่อนที่ playerจะย้ายไป 5 pixel

    ship = Ship(350, 650)# ตำแหน่งของplayer

    clock = pygame.time.Clock()

    def bg_window():
        """set bg and text"""
        win.blit(bg, (0, 0))
        # text
        miss_text = main_font.render(f"Missed: {miss}", 1, (255, 255, 255))
        level_text = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        #ตั้งค่าตำแหน่งของtext
        win.blit(miss_text, (10, 10))
        win.blit(level_text, (width - level_text.get_width() - 10, 10))

        ship.draw(win)

        pygame.display.update()

    while activate:
        clock.tick(fps)
        bg_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                activate = False

        #set keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and ship.y - player_vel > 0:# up
            ship.y -= player_vel
        if keys[pygame.K_DOWN] and ship.y + player_vel + 50 < height:# down
            ship.y += player_vel
        if keys[pygame.K_LEFT] and ship.x - player_vel > 0:# left
            ship.x -= player_vel
        if keys[pygame.K_RIGHT] and ship.x + player_vel + 50 < width:# right
            ship.x += player_vel

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
