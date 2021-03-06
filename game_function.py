# -*- coding: utf-8 -*-
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    #监视键盘和鼠标事件，#舰艇鼠标和键盘的响应，事件循环
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, screen, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
def check_keyup_events(event, screen, ship): 
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key ==pygame.K_LEFT:
        ship.moving_left = False
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    #创建一个直接退出的键
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
        
#创建一颗子弹，并放到编组bullets里
def fire_bullet(ai_settings, screen, ship, bullets):
    """若没有达到限制，就发射一颗子弹"""
    """创建新子弹，并将其加入到编组bullets中"""    
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
        # 设置背景颜色,每次循环时都重绘屏幕，背景色填充，之接受一种颜色
        screen.fill(ai_settings.bg_color)     
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()  
        aliens.draw(screen) #让一群外星人出现, 对编组调用draw() 能画出编组中每一个元素，绘制位置由元素属性rect决定
        #alien.blitme() 让一个外星人出现在屏幕上
      
        if not stats.game_active:
            play_button.draw_button()
            
        
        #让最近绘制的屏幕可见
        pygame.display.flip() 

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    #更新子弹的位置
    bullets.update()
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)   
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):  
    """响应子弹和外星人的碰撞"""
    #删除发生碰撞的子弹和外星人     
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if len(aliens) == 0:
        #删除所有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        
def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可以容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    """创建一个外星人，并计算一行可容纳多少个外星人"""
    alien = Alien(ai_settings, screen)
    number_aliens_x =  get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    #创建外星人群
    for row_number in range(number_rows):
        #创建一个外星人
        for alien_number in range(number_aliens_x):
            #创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
def change_fleet_direction(ai_settings, aliens):
    """整群外星人向下移动，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    #将ships_left减1
    stats.ships_left -= 1
    
    #清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    
    #创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    
    """响应飞船被外星人撞到"""
    if stats.ships_left > 0 :
        #将ships_left减1
        stats.ships_left -= 1
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到那样处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
        
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人在屏幕边缘，更新外星人群所有外星人的位置"""
  
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    #检查外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    
    #检查是否有外星人到达底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


    