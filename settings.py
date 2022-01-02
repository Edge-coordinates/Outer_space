# -*- coding: UTF-8 -*-

class Settings():
    """存储游戏所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (244, 96, 108)

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 35
        self.bullet_color = 60,60,60
        self.bullet_allowed = 3
        
        # Ghost1设置            
        self.fleet_drop_speed = 10
        # fleet_direction为1表示右转，为-1表示向左移
        self.fleet_direction = 1

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.ghost1_speed_factor = 0.5
    
        # fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction = 1

        # 计分
        self.ghost1_points = 5

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.ghost1_speed_factor *= self.speedup_scale
        self.ghost1_points = int(self.ghost1_points*self.score_scale)