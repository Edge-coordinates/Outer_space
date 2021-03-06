class GameStats():
    """跟踪游戏统计信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.rest_stats()
        self.game_active = False
        self.game_continue = 0
        self.high_score = 0 # 任何情况下都不应重置最高分
        
    def rest_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        