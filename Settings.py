# -*- coding: utf-8 -*-
class Settings():
    def __init__(self):
        """初始化所有的游戏设置"""
        #屏幕设置
        #子弹设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230 , 230)
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 2
        self.bullet_width = 100
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 20
        self.alien_speed_factor = 2
        self.fleet_drop_speed = 10
        #fleet_direction为1表示向右移动，-1为左移
        self.fleet_direction = 1
        self.ship_limit = 1


            
        