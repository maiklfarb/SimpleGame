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

        ship = Rocket(self.screen, self.settings, "1.png")
        self.ships.add(ship)
        ship2 = Rocket(self.screen,self.settings, "2.png", True)
        self.ships.add(ship2)

        # Контейнееры пуль для кораблей
        self.bullets = pygame.sprite.Group()
        self.bullets2 = pygame.sprite.Group()

    def Fire(self, _shipDown=True):
        if _shipDown == True:
            bullet = Bullet(self.screen, self.settings, self.ships.sprites()[0], _shipDown=_shipDown)
            self.bullets.add(bullet)
        else:
            bullet = Bullet(self.screen, self.settings, self.ships.sprites()[1], _shipDown=_shipDown)
            self.bullets2.add(bullet)

    def FireMega(self):
        if len(self.bullets) < self.settings.MegaFireCount:
            bullet = Bullet(self.screen, self.settings, self.ships.sprites()[0])
            bullet.rect.width = 200
            bullet.rect.height = 5
            bullet.rect.midbottom = self.ships.sprites()[0].rect.midbottom
            bullet.bulletSpeed = 1.5
            self.bullets.add(bullet)

    def FireMultiple(self, n):
        left = 5
        right = 0
        for i in range(0, n):
            bullet = Bullet(self.screen, self.settings, self.ships.sprites()[0])

            if i % 2 == 0:
                bullet.rect.x += right
                right += 5
            else:
                bullet.rect.x -= left
                left += 5

            self.bullets.add(bullet)

    def FireSpread(self):
        bulletCenter = Bullet(self.screen, self.settings, self.ships.sprites()[0])
        bulletRight = Bullet(self.screen, self.settings, self.ships.sprites()[0], "right")
        bulletLeft = Bullet(self.screen, self.settings, self.ships.sprites()[0], "left")

        self.bullets.add(bulletCenter)
        self.bullets.add(bulletRight)
        self.bullets.add(bulletLeft)

    # Метод проверки нажатия клавиши
    def CheckDown(self, event):
        if event.key == pygame.K_RIGHT:
            self.ships.sprites()[0].isRight = True
        elif event.key == pygame.K_LEFT:
            self.ships.sprites()[0].isLeft = True
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
            self.ships.sprites()[1].isRight = True
        elif event.key == pygame.K_a:
            self.ships.sprites()[1].isLeft = True

    def CheckUp(self,event):
        # Метод проверки отпускания клавиши
        if event.key == pygame.K_RIGHT:
            self.ships.sprites()[0].isRight = False
        elif event.key == pygame.K_LEFT:
            self.ships.sprites()[0].isLeft = False
        elif event.key == pygame.K_UP:
            self.ships.sprites()[0].isUp = False
        elif event.key == pygame.K_DOWN:
            self.ships.sprites()[0].isDown = False

        elif event.key == pygame.K_d:
            self.ships.sprites()[1].isRight = False
        elif event.key == pygame.K_a:
            self.ships.sprites()[1].isLeft = False

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

        for ship in self.ships.sprites():
            ship.blitme()

        for bullet in self.bullets2.sprites():
            bullet.blitme()
        for bullet in self.bullets.sprites():
            bullet.blitme()

        pygame.display.flip()

    def start(self):
        # Бесконечно делаем
        while True:
            self.CheckEvent()

            self.ships.update()

            # Вызываем метод update у группы спрайтов
            self.bullets.update()
            self.bullets2.update()

            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

            for bullet in self.bullets2.copy():
                if bullet.rect.bottom >= self.screen.get_height():
                    self.bullets2.remove(bullet)

            try:
                if len(self.ships.sprites()) > 1:
                    #print(pygame.sprite.spritecollide(self.ships.sprites()[1], self.bullets, True))

                    damage1 = len(pygame.sprite.spritecollide(self.ships.sprites()[1], self.bullets, True))
                    if damage1 > 0:
                        #print(len(self.ships))
                        print(f"Player 1: {self.ships.sprites()[1].health}")
                        if self.ships.sprites()[1].health >= 1:
                            self.ships.sprites()[1].health -= damage1
                        else:
                            self.ships.remove(self.ships.sprites()[1])

                    damage2 = len(pygame.sprite.spritecollide(self.ships.sprites()[1], self.bullets, True))
                    if damage2 > 0:
                        #print(len(self.ships))
                        print(f"Player 0: {self.ships.sprites()[0].health}")
                        if self.ships.sprites()[0].health >= 1:
                            self.ships.sprites()[0].health -= damage2
                        else:
                            self.ships.remove(self.ships.sprites()[0])
            except IndexError:
                print("Ошибка.")






            self.UpdateScreen()


if __name__ == '__main__':
    game = Two()
    game.start()