import pygame
import sys
from Settings import Settings
# импортируем класс Rocket
from Rocket import Rocket
from Bullet import Bullet

class Two:
    def __init__(self):
        # Инициализация игры и движка pygame
        pygame.init()
        # Создай объект Settings и сохрани ее в переменную класса
        self.settings = Settings()
        # Установи полноэкранный режим дисплея
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Измени объект настроек (его высоту) на основе текущего разрешения экрана
        self.settings.scrinWidth = self.screen.get_rect().width
        # Измени объект настроек (его ширину) на основе текущего разрешения экрана
        self.settings.scrinHeight = self.screen.get_rect().height
        pygame.display.set_caption("Simple Game")

        # Создай объект Rocket и сохрани его в переменную класса
        self.ships = pygame.sprite.Group()

        self.ship = Rocket(self.screen, self.settings, "1.png")
        self.ships.add(self.ship)
        self.ship2 = Rocket(self.screen,self.settings, "2.png", True)
        self.ships.add(self.ship2)

        # Контейнееры пуль для кораблей
        self.bullets = pygame.sprite.Group()
        self.bullets2 = pygame.sprite.Group()

    def Fire(self, _shipDown=True):
        if _shipDown == True:
            bullet = Bullet(self.screen, self.settings, self.ship, _shipDown=_shipDown)
            self.bullets.add(bullet)
        else:
            bullet = Bullet(self.screen, self.settings, self.ship2, _shipDown=_shipDown)
            self.bullets2.add(bullet)

    def FireMega(self):
        if len(self.bullets) < self.settings.MegaFireCount:
            bullet = Bullet(self.screen, self.settings, self.ship)
            bullet.rect.width = 200
            bullet.rect.height = 5
            bullet.rect.midbottom = self.ship.rect.midbottom
            bullet.bulletSpeed = 1.5
            self.bullets.add(bullet)

    def FireMultiple(self, n):
        left = 5
        right = 0
        for i in range(0, n):
            bullet = Bullet(self.screen, self.settings, self.ship)

            if i % 2 == 0:
                bullet.rect.x += right
                right += 5
            else:
                bullet.rect.x -= left
                left += 5

            self.bullets.add(bullet)

    def FireSpread(self):
        bulletCenter = Bullet(self.screen, self.settings, self.ship)
        bulletRight = Bullet(self.screen, self.settings, self.ship, "right")
        bulletLeft = Bullet(self.screen, self.settings, self.ship, "left")

        self.bullets.add(bulletCenter)
        self.bullets.add(bulletRight)
        self.bullets.add(bulletLeft)

    # Метод проверки нажатия клавиши
    def CheckDown(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.isRight = True
        elif event.key == pygame.K_LEFT:
            self.ship.isLeft = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_KP_ENTER:
            self.Fire()
        elif event.key == pygame.K_KP0:
            self.FireMultiple(11)
        elif event.key == pygame.K_KP1:
            self.FireSpread()
        #elif event.key == pygame.K_SPACE:
        #    self.FireMega()
        elif event.key == pygame.K_SPACE:
            self.Fire(False)
        elif event.key == pygame.K_d:
            self.ship2.isRight = True
        elif event.key == pygame.K_a:
            self.ship2.isLeft = True

    def CheckUp(self,event):
        # Метод проверки отпускания клавиши
        if event.key == pygame.K_RIGHT:
            self.ship.isRight = False
        elif event.key == pygame.K_LEFT:
            self.ship.isLeft = False
        elif event.key == pygame.K_UP:
            self.ship.isUp = False
        elif event.key == pygame.K_DOWN:
            self.ship.isDown = False

        elif event.key == pygame.K_d:
            self.ship2.isRight = False
        elif event.key == pygame.K_a:
            self.ship2.isLeft = False

    def CheckEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.CheckDown(event)
            elif event.type == pygame.KEYUP:
                self.CheckUp(event)

    def UpdateScreen(self):
        self.screen.fill(self.settings.colour)

        self.ship.blitme()
        self.ship2.blitme()
        for bullet in self.bullets2.sprites():
            bullet.blitme()
        for bullet in self.bullets.sprites():
            bullet.blitme()

        pygame.display.flip()

    def start(self):
        # Бесконечно делаем
        while True:
            self.CheckEvent()
            self.ship.Update()
            self.ship2.Update()
            # Вызываем метод update у группы спрайтов
            self.bullets.update()
            self.bullets2.update()

            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

            for bullet in self.bullets2.copy():
                if bullet.rect.bottom >= self.screen.get_height():
                    self.bullets2.remove(bullet)

            if pygame.sprite.spritecollideany(self.ship2, self.bullets):
                print(len(self.ships))
                if self.ship2.health >= 1:
                    self.ship2.health -= 1
                else:
                    self.ships.remove(self.ship2)
                    self.ship2.kill()




            self.UpdateScreen()


if __name__ == '__main__':
    game = Two()
    game.start()