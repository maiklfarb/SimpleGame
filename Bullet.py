from pygame.sprite import Sprite
import pygame


class Bullet(Sprite):
    def __init__(self, screen, settings, ship, _type="default", _shipDown=True):
        super().__init__()
        self._shipDown = _shipDown
        self._type = _type
        self.settings = settings
        self.screen = screen
        self.ship = ship
        self.colour = self.settings.bullet_colour
        self.rect = pygame.Rect(0, 0, self.settings.bullet_wight, self.settings.bullet_height)  # x, y, ширина, высота

        if self._shipDown == True:
            self.rect.midbottom = self.ship.rect.midtop

        else:
            self.rect.midtop = self.ship.rect.midbottom

        self._type = _type
        self.bulletSpeed = self.settings.bullet_speed

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        direction = 1
        if self._shipDown == False:
            direction = -1

        self.y -= self.bulletSpeed * direction
        self.rect.y = self.y

        if self._type != "default":
            if self._type == "right":
                self.x += self.bulletSpeed * direction
            elif self._type == "left":
                self.x -= self.bulletSpeed * direction
            self.rect.x = self.x


    def blitme(self):
        pygame.draw.rect(self.screen, self.colour, self.rect)  # где рисуем, цвет, что рисуем