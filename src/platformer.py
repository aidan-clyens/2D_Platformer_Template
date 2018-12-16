from constants import *
from levels import *
from blocks import *
from player import *
from menus import *
import pygame


def draw_level():
    level_blocks = []

    for row in range(0, ROWS):
        for col in range(0, 5*COLS):
            if row < len(level) and col < len(level[0]):
                if level[row][col] == '-':
                    level_block = LevelBlock(
                        col*BLOCK_WIDTH, row*BLOCK_HEIGHT, GREY)
                    level_blocks.append(level_block)
                if level[row][col] == 'J':
                    level_block = JumpBlock(col*BLOCK_WIDTH, row*BLOCK_HEIGHT)
                    level_blocks.append(level_block)
                if level[row][col] == 'G':
                    level_block = AntiGravityBlock(
                        col*BLOCK_WIDTH, row*BLOCK_HEIGHT)
                    level_blocks.append(level_block)
                if level[row][col] == 'V':
                    level_block = VictoryBlock(
                        col*BLOCK_WIDTH, row*BLOCK_HEIGHT)
                    level_blocks.append(level_block)
                if level[row][col] == 'p':
                    player = Player(col*BLOCK_WIDTH, row*BLOCK_HEIGHT)

    return player, level_blocks


def main():
    pygame.init()
    global running
    running = True
    paused = True

    clock = pygame.time.Clock()

    pause_menu = PauseMenu()
    game_over_menu = GameOverMenu()
    level_won_menu = LevelWonMenu()

    player, level_blocks = draw_level()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True

        if paused:
            pause_menu.update()
            paused = not pause_menu.is_click()

        elif player.is_dead:
            game_over_menu.update()
            if game_over_menu.is_click():
                player, level_blocks = draw_level()

        elif player.won_level:
            level_won_menu.update()
            if level_won_menu.is_click():
                player, level_blocks = draw_level()

        else:
            screen.fill(BLACK)

            for level_block in level_blocks:
                level_block.update(player.camX, player.camY)
            player.update(level_blocks)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
