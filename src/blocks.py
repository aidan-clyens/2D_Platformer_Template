from constants import *
import pygame


class Block():
    def __init__(self, w, h, x, y, colour):
        self.image = pygame.Surface([w, h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, [self.rect.x -
                                 self.camX, self.rect.y - self.camY])

    def update(self, camX, camY):
        self.camX = camX
        self.camY = camY
        self.draw()

    def test_collision(self, blocks):
        collisions = []
        for block in blocks:
            if self.rect.colliderect(block.rect):
                collisions.append(block)

        return collisions


class LevelBlock(Block):
    def __init__(self, x, y, colour):
        Block.__init__(self, BLOCK_WIDTH, BLOCK_HEIGHT, x, y, colour)

    def on_collide(self, player, x=False, y=False):
        if x:
            if player.dx > 0:
                player.rect.right = self.rect.left
            elif player.dx < 0:
                player.rect.left = self.rect.right
            else:
                pass

        elif y:
            if player.dy * player.grav_mult > 0:
                player.rect.bottom = self.rect.top
                player.dy = 0

                if player.grav_mult == 1:
                    player.jumping = False

                    if self.__class__.__name__ == 'JumpBlock':
                        player.jump_mult = 2
                        player.jump()
                    elif self.__class__.__name__ == 'AntiGravityBlock':
                        player.grav_mult *= -1
                        player.jump_mult = 1
                    else:
                        player.jump_mult = 1

            elif player.dy * player.grav_mult < 0:
                player.dy = 0
                player.rect.top = self.rect.bottom

                if player.grav_mult == -1:
                    player.jumping = False

                    if self.__class__.__name__ == 'JumpBlock':
                        player.jump_mult = 2
                        player.jump()
                    elif self.__class__.__name__ == 'AntiGravityBlock':
                        player.grav_mult *= -1
                        player.jump_mult = 1
                    else:
                        player.jump_mult = 1
            else:
                pass

        if self.__class__.__name__ == 'VictoryBlock':
            player.won_level = True


class JumpBlock(LevelBlock):
    def __init__(self, x, y):
        LevelBlock.__init__(self, x, y, WHITE)


class AntiGravityBlock(LevelBlock):
    def __init__(self, x, y):
        LevelBlock.__init__(self, x, y, BLUE)


class VictoryBlock(LevelBlock):
    def __init__(self, x, y):
        LevelBlock.__init__(self, x, y, YELLOW)
