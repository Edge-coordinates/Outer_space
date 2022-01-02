import sys
import pygame
from time import sleep

from bullet import Bullet
from enemy import Ghost1


def check_keydown_events(event, ai_settings, stats, sb, play_button, screen, ship, enemies, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True  # 向右移动飞船
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True  # 向左移动飞船
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, stats, screen, ship, bullets)
    elif event.key == pygame.K_p:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        check_play_button(ai_settings, stats, sb, play_button, screen, ship, enemies, bullets, 1, 0, 0)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False  # 停止向右移动飞船
    if event.key == pygame.K_LEFT:
        ship.moving_left = False  # 停止向左移动飞船


def check_events(ai_settings, screen, stats, sb, play_button, ship, enemies, bullets):
    """响应鼠标事件和点击"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, sb, play_button, screen, ship, enemies, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, stats, sb, play_button, screen, ship, enemies, bullets, 0, mouse_x, mouse_y)
            
def check_play_button(ai_settings, stats, sb, play_button, screen, ship, enemies, bullets, flag, mouse_x, mouse_y):
    """Start the game when the player click the play button"""
    if (play_button.rect.collidepoint(mouse_x, mouse_y) and stats.game_active == False) or flag:
        # Hide cursor
        pygame.mouse.set_visible(False)

        # Rest game statistics
        stats.rest_stats()
        stats.game_active = True

        # 重置计分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()

        # empt out the enemies list and the button list
        enemies.empty()
        bullets.empty()

        # Create a new Ghost List and move the ship to the bottom center of the screen
        create_fleet(ai_settings, screen, ship, enemies)
        ship.center_ship()


def fire_bullet(ai_settings, stats, screen, ship, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 创建一个子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullet_allowed and stats.game_active == True:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(ai_settings, stats, sb, screen, ship, ghosts, bullets):
    """更新子弹位置，并删除已消失的子弹"""
    # 更新子弹位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查是否有子弹击中Enemy
    # 如果有，就删除相应的子弹和Enemy
    check_bullet_enemy_collisions(ai_settings, stats, sb, screen, ship, ghosts, bullets)

def check_bullet_enemy_collisions(ai_settings, stats, sb, screen, ship, ghosts, bullets):
    collisions = pygame.sprite.groupcollide(bullets, ghosts, True, True)
    if collisions:
        for ghosts in collisions.values():
            stats.score += ai_settings.ghost1_points * len(ghosts)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(ghosts) == 0:
        """删除现有子弹，加快游戏节奏，并创建一群新的外星人"""
        # 每消灭一群外星人，就提高一个等级
        stats.level += 1
        sb.prep_level()

        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, ghosts)


def create_fleet(ai_settings, screen, ship, ghosts):
    """创建Enemy群"""
    # 创建一个Enemy，并计算一行可以容纳多少Enemy以及可以有多少行
    # Enemy间距为Enemy宽度
    ghost = Ghost1(ai_settings, screen)
    ghost_width = ghost.rect.width
    ghost_height = ghost.rect.height
    ship_height = 56 # ship.rect.height
    available_space_x = ai_settings.screen_width - 2 * ghost_width
    number_ghosts_x = int(available_space_x / (2 * ghost_width))
    available_space_y = ai_settings.screen_height - 3 * ghost_height - ship_height
    number_ghosts_rows = int(available_space_y / (2 * ghost_height))

    # 创建Enemy群
    for row_number in range(number_ghosts_rows):
        for ghost_number in range(number_ghosts_x):
            # 创建一个Enemy并将其加入当前行
            ghost = Ghost1(ai_settings, screen)
            ghost.x = ghost_width + 2 * ghost_width * ghost_number
            ghost.rect.x = ghost.x
            ghost.rect.y = ghost_height + 2 * ghost_height * row_number
            ghosts.add(ghost)

def check_fleet_edges(ai_settings, ghosts):
    """有Enemy到达边缘时采取相应的措施"""
    for ghost in ghosts.sprites():
        if ghost.check_edges():
            change_fleet_direction(ai_settings, ghosts)
            break

def change_fleet_direction(ai_settings, ghosts):
    """将Enemy群体整体向下平移并视情况改变其方向"""
    for ghost in ghosts.sprites():
        ghost.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, sb, screen, ship, enemies, bullets):
    """响应被Enemy撞到的飞船"""
    if stats.ship_left > 0:
    # 将ships_left减1
        stats.ship_left -= 1
        # Empt out the Ghost List and the Bullet List
        enemies.empty()    
        bullets.empty()
        # 跟新计分牌
        sb.prep_ship()
        # Create a new Ghost List and move the ship to the bottom center of the screen
        create_fleet(ai_settings, screen, ship, enemies)
        ship.center_ship()
        
        # Peause for a while
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_Ghosts(ai_settings, stats, sb, screen, ship, ghosts, bullets):
    """检查是否有Enemy位于屏幕边缘并更新Enemy群中所有Enemy的位置"""
    check_fleet_edges(ai_settings, ghosts)
    ghosts.update()

    # 检查Enemy和Ship之间的碰撞
    if pygame.sprite.spritecollideany(ship, ghosts):
         ship_hit(ai_settings, stats, sb, screen, ship, ghosts, bullets)

    check_enemies_bottom(ai_settings, stats, sb, screen, ship, ghosts, bullets)

def check_enemies_bottom(ai_settings, stats, sb, screen, ship, enemies, bullets):
    """Check if any enemies reched the buttom"""
    screen_rect = screen.get_rect()
    for enemy in enemies:
        if(enemy.rect.bottom >= screen_rect.bottom):
            # Treated as if a ship was hit
            ship_hit(ai_settings, stats, sb, screen, ship, enemies, bullets)
            break

def check_high_score(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def update_screen(ai_settings, screen, stats, sb, ship, ghosts, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    ghosts.draw(screen)
    # 在飞船和Enemy后面绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 显示的分
    sb.show_score()
    # Draw the button if it is inactive show the play button
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()