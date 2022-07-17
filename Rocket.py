import pygame
from pygame.sprite import Sprite
from Health import Health

class Rocket(Sprite):
    def __init__(self, screen, settings, image, spawnUp=False):
        super().__init__()
        if spawnUp == False:
            self.shipDown = True
        else:
            self.shipDown = False
        self.health = 5
        self.screen = screen
        self.scrinRect = screen.get_rect()
        self.settings = settings
        self.image = pygame.image.load(f"Images/{image}")
        self.rect = self.image.get_rect()
        self.healths = pygame.sprite.Group()

        if not spawnUp:
            self.rect.midbottom = self.scrinRect.midbottom
        else:
            self.rect.midtop = self.scrinRect.midtop
        self.generate_hearts()
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.isRight = False
        self.isLeft = False
        self.isUp = False
        self.isDown = False
    def update(self):
        if self.isLeft and self.rect.left > 0:
            self.x -= self.settings.speed
        if self.isRight and self.rect.right < self.scrinRect.right:
            self.x += self.settings.speed
        if self.isDown and self.rect.bottom < self.scrinRect.bottom:
            self.y += self.settings.speed
        if self.isUp and self.rect.top > self.scrinRect.top:
            self.y -= self.settings.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        for heart in self.healths.sprites():
            heart.blitme()

    def generate_hearts(self):
        direction = 1
        if not self.shipDown:
            direction *= -1
        for i in range(self.health):
            heart = Health(self.screen, "n.png", self.shipDown)
            heart.rect.x -= 40 * i * direction
            self.healths.add(heart)

    def damage(self, n):
        self.health -= n
        for i in range(n):
            lastHeart = self.healths.sprites()[-1]
            self.healths.remove(lastHeart)


