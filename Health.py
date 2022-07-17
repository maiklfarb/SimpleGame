import pygame
from pygame.sprite import Sprite
class Health(Sprite):
    def __init__(self, screen, image, shipDown=False):
        super().__init__()
        self.screen = screen
        self.scrinRect = screen.get_rect()
        self.image = pygame.image.load(f"Images/{image}")
        self.rect = self.image.get_rect()

        if shipDown:
            self.rect.bottomright = self.scrinRect.bottomright
        else:
            self.rect.topleft = self.scrinRect.topleft


    def blitme(self):
        self.screen.blit(self.image, self.rect)