# -*- coding: utf-8 -*-
import pygame
import Settings, ships
import game_function as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings.Settings()
    #创建显示框
    #screen 是一个surface，需要用到屏幕的宽和高
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    #创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    
    stats = GameStats(ai_settings)

    #创建一艘飞船、一个子弹的编组和一个外星人的编组
    ship = ships.Ship(ai_settings, screen) 
    bullets = Group()
    aliens = Group()
    
    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    #游戏开始主循环
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)   

run_game()