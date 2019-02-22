# -*- coding: utf-8 -*-
import pygame

class Ship():
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初试位置"""
        self.screen = screen
        self.ai_settings = ai_settings
        #加载飞船图像并获取其外接矩阵
        self.image = pygame.image.load('ship.bmp') #加载图片，返回表示飞船的surface
        #self.rect 返回<rect(0, 0, 60, 48)> 0,0 为左上角的坐标 60，48 为矩形的宽和高
        self.rect = self.image.get_rect() #获取飞船的属性，通过设置矩形四角和中心x和y的坐标来指定矩形的位置
        
        #self.screen_rect 返回<rect(0, 0, 1200, 800)> 0, 0 为左上角的坐标 1200, 800 为生成屏幕的宽和高
        self.screen_rect = screen.get_rect()  
        
        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx #将游戏元素居中 若要将游戏元素和屏幕边缘对齐，采用top/bottom/left/right
        self.rect.bottom = self.screen_rect.bottom #若要调整元素水平或垂直位置，直接条用对应矩阵左上角顶顶啊的x和y坐标值
                                                                           #注意，原点坐标是左上角，右下角代表（1200， 800）
        #控制飞船移动的速度因子
        self.center = float(self.rect.centerx)
        
        #移动标志,初始化的运动模式
        self.moving_right = False
        self.moving_left = False
    def update(self):
        #飞船向右移动
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
         #根据self.center更新rect对象
        self.rect.centerx =self.center #self.rect.centerx只会存储self.center的整数部分
    
    def blitme(self):# 根据self。rect指定的位置将图像绘制到屏幕上
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕中央"""
        self.center = self.screen_rect.centerx