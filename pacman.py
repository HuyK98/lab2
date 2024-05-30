import pygame
import random

# Khởi tạo các hằng số cho game
WIDTH = 800
HEIGHT = 600
FPS = 60

# Định nghĩa màu sắc
BACKGROUND_COLOR = (0, 0, 0)  # Màu nền
PACMAN_COLOR = (255, 255, 0)  # Màu Pacman
GHOST_COLOR = (0, 0, 255)  # Màu Ghost
OBSTACLE_COLOR = (255, 0, 0)  # Màu chướng ngại vật
TEXT_COLOR = (255, 255, 255)  # Màu chữ

# Khởi tạo pygame và cửa sổ game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")
clock = pygame.time.Clock()

# Tải âm thanh
eat_sound = pygame.mixer.Sound("eat.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Tải hình ảnh
pacman_img = pygame.image.load("pacman.png")
ghost_img = pygame.image.load("ghost.png")

# Định nghĩa lớp Pacman
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pacman_img, (30, 30))
        self.image.fill(PACMAN_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed = 5  # Tốc độ di chuyển của Pacman

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -self.speed
        if keystate[pygame.K_RIGHT]:
            self.speed_x = self.speed
        if keystate[pygame.K_UP]:
            self.speed_y = -self.speed
        if keystate[pygame.K_DOWN]:
            self.speed_y = self.speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

# Định nghĩa lớp Ghost
class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ghost_img, (20, 20))
        self.image.fill(GHOST_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed_x = -self.speed_x
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.speed_y = -self.speed_y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.image.fill(OBSTACLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Khởi tạo tất cả các sprite
all_sprites = pygame.sprite.Group()
pacman = Pacman()
ghosts = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

all_sprites.add(pacman)

for _ in range(3):
    ghost = Ghost()
    all_sprites.add(ghost)
    ghosts.add(ghost)

for _ in range(10):
    x = random.randrange(WIDTH)
    y = random.randrange(HEIGHT)
    size = 20
    obstacle = Obstacle(x, y, size)
    obstacles.add(obstacle)
    all_sprites.add(obstacle)

# Điểm số
score = 0

# Game loop
running = True
while running:
    # Kiểm tra events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Cập nhật
    all_sprites.update()

    # Kiểm tra va chạm giữa Pacman và Ghosts
    hits = pygame.sprite.spritecollide(pacman, ghosts, True)
    if hits:
        eat_sound.play()
        score += 1
        ghost = Ghost()
        all_sprites.add(ghost)
        ghosts.add(ghost)

    # Kiểm tra va chạm giữa Pacman và Obstacles
    hits = pygame.sprite.spritecollide(pacman, obstacles, True)
    if hits:
        game_over_sound.play()
        running = False

    # Vẽ màn hình game
    screen.fill(BACKGROUND_COLOR)
    all_sprites.draw(screen)

    # Vẽ điểm số
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

    # Hiển thị
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()