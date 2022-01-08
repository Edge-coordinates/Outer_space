# -*- coding: UTF-8 -*-

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from enemy import Ghost1
import game_functions as gf


def run_game():
    # 初始化pygame,设置屏幕和对向。
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Aline Invasion")

    # Create the Play button
    play_button = Button(ai_settings, screen, "Play")
    continue_button = Button(ai_settings, screen, "Continue")
    # 创建一个用于存储游戏统计信息的实例并创建计分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一个文件用于存储历史最高分
    fo = open('date/high_score.txt', mode = 'a+')
    # 创建一艘飞船, 一个子弹编组, 和一个Enemy群
    ship = Ship(ai_settings, screen)
    bullets = Group()
    ghosts = Group()
    # 创建敌军群
    gf.create_fleet(ai_settings, screen, ship, ghosts)
    
    # 开始游戏主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, continue_button, play_button, ship, ghosts, bullets, fo)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, stats, sb, screen, ship, ghosts, bullets)
            gf.update_Ghosts(ai_settings, stats, sb, screen, ship, ghosts, bullets)
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, ghosts, bullets, play_button, continue_button)

run_game()
