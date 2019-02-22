# -*- coding: utf-8 -*-
"""
类里面包含
屏幕的宽，高，背景色，子弹的宽，高，数量 外星人的向下速度 飞船的移动速度



初始化对象
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("入侵")

监听键盘和鼠标事件
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()

让最近绘制的屏幕可见
pygame.display.flip()


设置背景色
bg_color = (230, 230, 230)
然后再while下面创建screen.fill(bg_color)

self.rect代表物体的位置
将飞船放在屏幕中心可设置为self.rect.centerx = self.screen_rect.centerx
底部：self.rect.bottom = sellf.screen_rect.bottom

self.screen.blit(self.image, self.rect) 可以在指定位置绘制飞船 ，pygame.image.load('')   self.image.get_rect()
图片是根据包裹图片的方形来运动的

game functions
接受键盘和鼠标的信号 -check_events
画出图形-update_screen
ships 
控制飞船的移动--update

外星人


要创建一个外星人 

需要在alien.py里使用 blitme（）：
self.screen.blit(self.image, self.rect)

在主程序里创建
alien = Alien(ai_settings, screen)
在my_game_functions里
更新update_screen():
添加alien.blitme()


"""