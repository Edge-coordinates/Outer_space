import pygame
from pygame.sprite import Sprite


class Ghost1(Sprite):
    """表示单个敌军的类"""

    def __init__(self, ai_settings, screen):
        """初始化Enemy并设置其起始位置"""
        super(Ghost1, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载敌军的图像，并设置其rect属性
        self.image = pygame.image.load('images/Ghost1.bmp')
        self.image = pygame.transform.scale(self.image, (50, 50))  # 转化大小
        self.rect = self.image.get_rect()

        # 每个Enemy最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储每个敌军的准确位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果Enemy位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向右移动Enemy"""
        self.x += (self.ai_settings.ghost1_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
    def blitme(self):
        """在指定位置绘制Enemy"""
        self.screen.blit(self.image, self.rect)
