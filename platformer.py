import pygame

WIDTH = 800
HEIGHT = 600

BLOCK_WIDTH = WIDTH / 20
BLOCK_HEIGHT = BLOCK_WIDTH

ROWS = HEIGHT / BLOCK_HEIGHT
COLS = WIDTH / BLOCK_WIDTH

PLAYER_WIDTH = BLOCK_WIDTH
PLAYER_HEIGHT = BLOCK_HEIGHT

PLAYER_SPEED = 10
GRAVITY = 0.5
JUMP_FORCE = 10

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (125,125,125)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

right_border = WIDTH
left_border = 0

camX = 0
camY = 0

level = [
    "-                                       ",
    "-                                       ",
    "-                                       ",
    "-                                       ",
    "-                                       ",
    "-                                       ",
    "-                                       ",
    "-                                       ",
    "-                              -        ",
    "-                                       ",
    "-     p                    -            ",
    "-                       -               ",
    "-                      -                ",
    "-                     -                 ",
    "----------------------------------------"
]

class Block():
    def __init__(self, w, h, x, y, colour):
        self.image = pygame.Surface([w,h])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, [self.rect.x - camX, self.rect.y - camY])

    def update(self):
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

class Player(Block):
    jumping = False

    def __init__(self, x, y):
        Block.__init__(self, PLAYER_WIDTH, PLAYER_HEIGHT, x, y, WHITE)
        self.dx = 0
        self.dy = 0

    def update(self, level_blocks):
        global right_border, left_border, camX
        
        pressed = pygame.key.get_pressed()

        if self.rect.right > right_border:
            right_border += WIDTH
            left_border += WIDTH
            camX += WIDTH

        if self.rect.left < left_border:
            right_border -= WIDTH
            left_border -= WIDTH
            camX -= WIDTH

        if pressed[pygame.K_a]:
            self.left()
        if pressed[pygame.K_d]:
            self.right()
        if pressed[pygame.K_SPACE]:
            self.jump()

        self.move(level_blocks)
        Block.update(self)

    def move(self, level_blocks):
        self.rect.x += self.dx

        for block in level_blocks:
            if self.rect.colliderect(block):
                if self.dx > 0:
                    self.rect.right = block.rect.left
                elif self.dx < 0:
                    self.rect.left = block.rect.right
        
        self.dy += GRAVITY
        self.rect.y += self.dy
    
        for block in level_blocks:
            if self.rect.colliderect(block):
                if self.dy > 0:
                    self.rect.bottom = block.rect.top
                    self.dy = 0
                    self.jumping = False
                elif self.dy < 0:
                    self.rect.top = block.rect.bottom

        self.dx = 0
    
    def left(self):
        self.dx = -PLAYER_SPEED

    def right(self):
        self.dx = PLAYER_SPEED
    
    def jump(self):
        if not self.jumping:
            self.dy -= JUMP_FORCE
            self.jumping = True

def draw_level():
    level_blocks = []

    for row in range(0, ROWS):
        for col in range(0, 2*COLS):
            if level[row][col] == '-':
                level_block = LevelBlock(col*BLOCK_WIDTH, row*BLOCK_HEIGHT, GREY)
                level_blocks.append(level_block)
            if level[row][col] == 'p':
                player = Player(col*BLOCK_WIDTH, row*BLOCK_HEIGHT)
            
    return player, level_blocks

def main():
    pygame.init()
    running = True

    clock = pygame.time.Clock()

    player, level_blocks = draw_level()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        for level_block in level_blocks:
            level_block.update()
        player.update(level_blocks)
                    
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()