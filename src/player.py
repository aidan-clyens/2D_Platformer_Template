from constants import *
from blocks import *
import pygame

class Player(Block):
    grav_mult = 1
    jump_mult = 1
    jumping = False
    is_dead = False
    won_level = False

    right_border = WIDTH
    left_border = 0

    camX = 0
    camY = 0

    def __init__(self, x, y):
        Block.__init__(self, PLAYER_WIDTH, PLAYER_HEIGHT, x, y, WHITE)
        self.dx = 0
        self.dy = 0

    def update(self, level_blocks):
        pressed = pygame.key.get_pressed()

        if self.rect.right > self.right_border:
            self.right_border += WIDTH
            self.left_border += WIDTH
            self.camX += WIDTH

        if self.rect.left < self.left_border:
            self.right_border -= WIDTH
            self.left_border -= WIDTH
            self.camX -= WIDTH

        if pressed[pygame.K_a]:
            self.left()
        if pressed[pygame.K_d]:
            self.right()
        if pressed[pygame.K_SPACE]:
            self.jump()

        self.move(level_blocks)
        Block.update(self, self.camX, self.camY)

    def move(self, level_blocks):
        self.rect.x += self.dx

        for block in level_blocks:
            if self.rect.colliderect(block):
                block.on_collide(self, x=True)

        self.dx = 0
        self.dy += GRAVITY
        self.rect.y += self.grav_mult*self.dy

        for block in level_blocks:
            if self.rect.colliderect(block):
                block.on_collide(self, y=True)

        if self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.is_dead = True

    def left(self):
        self.dx = -PLAYER_SPEED

    def right(self):
        self.dx = PLAYER_SPEED

    def jump(self):
        if not self.jumping:
            self.dy -= self.jump_mult * JUMP_FORCE
            self.jumping = True
