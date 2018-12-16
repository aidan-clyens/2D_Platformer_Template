from constants import *
import pygame

class Menu():
    def __init__(self, title, button):
        self.title_font = pygame.font.SysFont(menu_font, 60)
        self.button_font = pygame.font.SysFont(menu_font, 40)

        self.button_text = button

        self.title = self.title_font.render(title, True, WHITE)
        self.play_button = self.button_font.render(button, True, WHITE)

    def update(self):
        screen.fill(BLACK)
        screen.blit(self.title, [WIDTH / 2 -
                                 self.title.get_rect().width / 2, HEIGHT / 2])
        screen.blit(self.play_button, [WIDTH / 2 - self.play_button.get_rect().width / 2,
                                       HEIGHT / 2 + self.title.get_rect().height + self.play_button.get_rect().height])

    def is_click(self):
        mouse = pygame.mouse.get_pos()

        if mouse[0] > 367 and mouse[0] < 431 and mouse[1] > 371 and mouse[1] < 391:
            self.play_button = self.button_font.render(
                self.button_text, True, GREY)

            click = pygame.mouse.get_pressed()

            if click[0] == 1:
                return True
        else:
            self.play_button = self.button_font.render(
                self.button_text, True, WHITE)

        return False


class PauseMenu(Menu):
    def __init__(self):
        Menu.__init__(self, "2D Platformer", "PLAY")


class GameOverMenu(Menu):
    def __init__(self):
        Menu.__init__(self, "Game Over", "Play Again?")


class LevelWonMenu(Menu):
    def __init__(self):
        Menu.__init__(self, "You Won!", "Play Again?")
