import pygame, time, sys
from pygame.locals import *
import random
import os

pygame.init()

FPS = 30
framesPerSec = pygame.time.Clock()

black = (0, 0, 0)
red = (255, 0, 0)
purple = (120, 0, 100)
white = (255, 255, 255)

# Print current working directory
print("Current working directory:", os.getcwd())

# Change working directory if necessary


# Pencere boyutunu kare ve daha büyük olacak şekilde ayarlayalım
window_size = 700
window = pygame.display.set_mode((window_size, window_size))
window.fill(black)
pygame.display.set_caption("Asteroid Avoid")

speed = 10

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

from pygame import mixer
mixer.init()

# Function to load a music file with error handling
def load_music(file_name):
    try:
        mixer.music.load(file_name)
    except pygame.error:
        print(f"Error: No file '{file_name}' found in working directory '{os.getcwd()}'.")
        sys.exit()

# Function to load a sound file with error handling
def load_sound(file_name):
    try:
        return pygame.mixer.Sound(file_name)
    except pygame.error:
        print(f"Error: No file '{file_name}' found in working directory '{os.getcwd()}'.")
        sys.exit()

# Load high score from file
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Save high score to file
def save_high_score(high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

load_music("space2.mp3")
mixer.music.set_volume(0.7)
mixer.music.play()

# Skor arttığında çalacak ses dosyasını yükleyin
score_sound = load_sound("collect_points.mp3")
# Game over olduğunda çalacak müzik dosyasını yükleyin
game_over_sound = load_sound("game_over.mp3")

def load_image(file_name):
    try:
        return pygame.image.load(file_name)
    except pygame.error:
        print(f"Error: No file '{file_name}' found in working directory '{os.getcwd()}'.")
        sys.exit()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("alien2.png")
        self.image = pygame.transform.scale(self.image, (80, 70))  # Görseli yeniden boyutlandırma
        self.rect = self.image.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, 0)))  # Yeni pencere boyutuna göre ayarlandı

    def move(self, destroyed):
        self.rect.move_ip(0, speed)
        if self.rect.bottom > SCREEN_HEIGHT or destroyed:  # Yeni pencere boyutuna göre ayarlandı
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, 0))  # Yeni pencere boyutuna göre ayarlandı

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("rocket.png")
        self.image = pygame.transform.scale(self.image, (130, 180))  # Görseli yeniden boyutlandırma
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10))  # Rocket biraz yukarıda başlasın

    def draw(self, surface):
        self.draw_headlights(surface)
        surface.blit(self.image, self.rect)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-10, 0)  # Hızı 10 olarak ayarladım
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(10, 0)  # Hızı 10 olarak ayarladım

    def draw_headlights(self, surface):
        # Define the polygon points for the headlights
        headlight_width = 50
        headlight_end_width = 200
        headlight_length = 150
        headlight_color = (255, 255, 255, 150)  # More white with some transparency

        points = [
            (self.rect.centerx - headlight_width // 2, self.rect.top),
            (self.rect.centerx + headlight_width // 2, self.rect.top),
            (self.rect.centerx + headlight_end_width // 2, self.rect.top - headlight_length),
            (self.rect.centerx - headlight_end_width // 2, self.rect.top - headlight_length),
        ]
        
        headlight_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(headlight_surface, headlight_color, points)
        surface.blit(headlight_surface, (0, 0))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = load_image("fireball_image3.png")
        self.image = pygame.transform.scale(self.image, (30, 30))  # Görseli yeniden boyutlandırma
        self.rect = self.image.get_rect(center=player.rect.midtop)

    def update(self):
        self.rect.move_ip(0, -10)
        if self.rect.top < 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Background():
    def __init__(self):
        self.backgroundImage = load_image("backgroundImage2.png")
        self.backgroundImage = pygame.transform.scale(self.backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rectBGimage = self.backgroundImage.get_rect()
        self.bgY1 = 0
        self.bgX1 = 0
        self.bgY2 = -self.rectBGimage.height
        self.bgX2 = 0
        self.moveSpeed = 5

    def update(self):
        self.bgY1 += self.moveSpeed
        self.bgY2 += self.moveSpeed
        if self.bgY1 > self.rectBGimage.height:
            self.bgY1 = -self.rectBGimage.height
        if self.bgY2 > self.rectBGimage.height:
            self.bgY2 = -self.rectBGimage.height
    
    def render(self):
        window.blit(self.backgroundImage, (self.bgX1, self.bgY1))
        window.blit(self.backgroundImage, (self.bgX2, self.bgY2))

background = Background()

INCREASE_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INCREASE_SPEED, 3000)

P1 = Player()
E1 = Enemy()
E2 = Enemy()
E3 = Enemy()

enemyGroup = pygame.sprite.Group()
enemyGroup.add(E1)
enemyGroup.add(E2)
enemyGroup.add(E3)

bullets = pygame.sprite.Group()

font = pygame.font.SysFont("Verdana", 40)
gameOverFont = pygame.font.SysFont("Verdana", 80)
scoreFont = pygame.font.SysFont("Verdana", 50)
buttonFont = pygame.font.SysFont("Verdana", 30)

score = 0
lives = 3  # Başlangıçta 3 can
destroyed = False
high_score = load_high_score()  # Load the high score at the start

# Kalp görselini yükleyin ve yeniden boyutlandırın
heart_image = load_image("heart3.png")
heart_image = pygame.transform.scale(heart_image, (40, 40))  # Kalp boyutunu ayarlayın
heart_rect = heart_image.get_rect()

# Game over arka plan görselini yükleyin
game_over_background = load_image("gameover.png")
game_over_background = pygame.transform.scale(game_over_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Son ateşleme zamanı
last_shot_time = pygame.time.get_ticks()
shoot_delay = 250  # milisaniye cinsinden gecikme süresi

def show_game_over_screen():
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    window.blit(game_over_background, (0, 0))  # Game over arka plan görselini çiz
    finalScoreRender = scoreFont.render("Score: " + str(score), True, white)
    highScoreRender = scoreFont.render("High Score: " + str(high_score), True, white)
    window.blit(finalScoreRender, (SCREEN_WIDTH//2 - finalScoreRender.get_width()//2, SCREEN_HEIGHT - 150))  # Skoru ekranın altına ortalayın
    window.blit(highScoreRender, (SCREEN_WIDTH//2 - highScoreRender.get_width()//2, SCREEN_HEIGHT - 100))  # High score'u göster
    
    # Yeniden Başla butonu
    buttonText = buttonFont.render("Restart", True, white)
    buttonRect = buttonText.get_rect()
    buttonRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT - 180)  # Butonu ekranın altına ortalayın
    pygame.draw.rect(window, purple, buttonRect.inflate(20, 10))
    window.blit(buttonText, buttonRect)
    
    pygame.display.update()
    
    # Game over müziğini çal
    game_over_sound.play()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:  # 'R' tuşuna basıldığında yeniden başlat
                    waiting = False
                    return True
            if event.type == MOUSEBUTTONDOWN:
                if buttonRect.collidepoint(event.pos):
                    waiting = False
                    return True
    return False

def reset_game():
    global P1, E1, E2, E3, enemyGroup, bullets, score, lives, destroyed
    P1 = Player()
    E1 = Enemy()
    E2 = Enemy()
    E3 = Enemy()
    enemyGroup = pygame.sprite.Group()
    enemyGroup.add(E1)
    enemyGroup.add(E2)
    enemyGroup.add(E3)
    bullets = pygame.sprite.Group()
    score = 0
    lives = 3
    destroyed = False

while True:
    scoreRender = font.render("Score: " + str(score), True, red)
    highScoreRender = font.render("High Score: " + str(high_score), True, red)
    background.update()
    background.render()
    window.blit(scoreRender, (10, 10))
    window.blit(highScoreRender, (10, 50))  # High score'u ekranın üst kısmında göster
    
    # Canları ekranda sağ üst köşede göster
    for i in range(lives):
        window.blit(heart_image, (SCREEN_WIDTH - (i + 1) * (heart_rect.width + 10), 10))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == INCREASE_SPEED:
            speed += 0.5

    collision = pygame.sprite.spritecollideany(P1, enemyGroup)
    if collision:
        lives -= 1
        if lives <= 0:
            if show_game_over_screen():
                reset_game()
            else:
                pygame.quit()
                sys.exit()
        else:
            collision.kill()

    pressed_keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    if pressed_keys[K_SPACE] and current_time - last_shot_time > shoot_delay:
        new_bullet = Bullet(P1)
        bullets.add(new_bullet)
        last_shot_time = current_time

    for bullet in bullets:
        bullet.update()
        bullet.draw(window)

    # Çarpışmaları kontrol et ve meteorları yok et
    collisions = pygame.sprite.groupcollide(enemyGroup, bullets, True, True)
    if collisions:
        score += len(collisions)  # Çarpışma sayısına göre skoru artır
        score_sound.play()  # Skor arttığında ses çal
        for hit in collisions:
            enemyGroup.add(Enemy())

    for enemy in enemyGroup:
        enemy.move(destroyed)
        enemy.draw(window)

    P1.update()
    P1.draw(window)

    pygame.display.update()
    framesPerSec.tick(FPS)
