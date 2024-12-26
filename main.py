import pygame
from pygame.locals import *

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Танчики')


FPS = 60
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color, controls):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 5
        self.bullets = pygame.sprite.Group()
        self.controls = controls
        self.alive = True

    def update(self, keys):
        if keys[self.controls['left']]:
            self.rect.x -= self.speed
        if keys[self.controls['right']]:
            self.rect.x += self.speed
        if keys[self.controls['up']]:
            self.rect.y -= self.speed
        if keys[self.controls['down']]:
            self.rect.y += self.speed

        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, -10 if self.controls['shoot'] == K_SPACE else 10)
        self.bullets.add(bullet)

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)
            self.bullets.update()
            self.bullets.draw(surface)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(red)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y  += self.speed
        if self.rect.bottom < 0 or self.rect.top > height:
            self.kill()


def main():
    clock = pygame.time.Clock()
    running = True
    tank1 = Tank(200, 500, green, {
        'left': K_LEFT, 'right': K_RIGHT, 'up': K_UP, 'down': K_DOWN, 'shoot': K_RETURN
    })

    tank2 = Tank(600, 100, green, {
        'left': K_a, 'right': K_d, 'up': K_w, 'down': K_s, 'shoot': K_SPACE
    })

    tanks = pygame.sprite.Group(tank1, tank2)

    while running:
        screen.fill(white)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == tank1.controls['shoot'] and tank1.alive:
                    tank1.shoot()
                if event.key == tank2.controls['shoot'] and tank2.alive:
                    tank2.shoot()

        tank1.update(keys)
        tank2.update(keys)

        for bullet in tank1.bullets:
            if tank2.alive and tank2.rect.colliderect(bullet.rect):
                tank1.alive = False
                bullet.kill()

        for bullet in tank2.bullets:
            if tank1.alive and tank1.rect.colliderect(bullet.rect):
                tank2.alive = False
                bullet.kill()

        tank1.draw(screen)
        tank2.draw(screen)
        if not tank1.alive or not  tank2.alive:
            font = pygame.font.Font(None, 74)
            text = font.render('Game over', True, black)
            screen.blit(text, (width//2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

main()