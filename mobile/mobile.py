import pygame

from constants import *

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE


class Mobile:

    def __init__(self, position=(0, 0), speed=(0, 0), image_path='not_an_image_path'):
        self.x, self.y = position
        self.x_speed, self.y_speed = speed
        self.image = pygame.image.load(image_path)

    def move(self, screen: pygame.Surface):
        """Update the position of the mobile object and
        draw its image at that new location"""

        self._draw(screen)
        self._constraints()

    def _constraints(self):
        """Define how the object moves

            Apply movement constraints to the object's position

            Ex: some object should not cross the window's borders
            while some other should then appear at the apposite border"""

    def _draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        return f' class: {str(self.__class__).split(".")[-1][:-2]}' \
               f' x: {self.x},' \
               f' y: {self.y},' \
               f' x_speed: {self.x_speed},' \
               f' y_speed: {self.y_speed},'


"""________________________________________________________________________"""


class Player(Mobile):

    def __init__(self, position=(0, 0)):
        super().__init__(position, (0, 0), PLAYER_IMAGE_PATH)
        self.bullets = []
        self.is_alive = True
        for _ in range(NB_BULLETS):
            self.bullets.append(Bullet())

    def _constraints(self):
        if self.is_alive:
            if self.x > SCREEN_WIDTH:
                self.x = -self.image.get_width()
            elif self.x < -self.image.get_width():
                self.x = SCREEN_WIDTH
            else:
                self.x += self.x_speed

            if self.y > SCREEN_HEIGHT:
                self.y = -self.image.get_height()
            elif self.y < -self.image.get_height():
                self.y = SCREEN_HEIGHT
            else:
                self.y += self.y_speed

    def can_fire(self):
        """Returns the first bullet that can be fired

        If there is no such a bullet, return -1"""
        if self.is_alive:
            for bullet in self.bullets:
                if not bullet.is_fired:
                    return bullet
            return -1

    def manage_keyboard_events(self, event: pygame.event):
        """Updates the player's speed or fire a bullet accordingly to the keys events (arrow keys, space bar)"""
        if not self.is_alive:
            return
        if event.type == pygame.KEYDOWN:
            self._manage_keydown_events(event)
        elif event.type == pygame.KEYUP:
            self._manage_keyup_events(event)

    def _manage_keyup_events(self, event):
        # left_right_key_released
        self.x_speed = 0 if \
            (event.key == pygame.K_LEFT and self.x_speed < 0) or (event.key == pygame.K_RIGHT and self.x_speed > 0) \
            else self.x_speed
        # up_down_key_released
        self.y_speed = 0 if \
            (event.key == pygame.K_UP and self.y_speed < 0) or (event.key == pygame.K_DOWN and self.y_speed > 0) \
            else self.y_speed

    def _manage_keydown_events(self, event):
        # arrow keys pushed
        if event.key == pygame.K_LEFT:
            self.x_speed = -PLAYER_SPEED
        if event.key == pygame.K_RIGHT:
            self.x_speed = PLAYER_SPEED
        if event.key == pygame.K_DOWN:
            self.y_speed = PLAYER_SPEED
        if event.key == pygame.K_UP:
            self.y_speed = -PLAYER_SPEED

        # player try firing a bullet
        if event.key == pygame.K_SPACE:
            bullet = self.can_fire()
            if isinstance(bullet, Bullet):
                bullet.x = self.x + self.image.get_width() / 2 - bullet.image.get_width() / 2
                bullet.y = self.y - self.image.get_height() / 2
                fire_sound = pygame.mixer.Sound(GUN_SOUND_PATH)
                # play the sound for 125 ms
                fire_sound.play(maxtime=125)
                bullet.is_fired = True

    def _draw(self, screen):
        if self.is_alive:
            super()._draw(screen)


"""________________________________________________________________________"""


class Enemy(Mobile):
    def __init__(self, position=(0, 0)):
        super().__init__(position, (ENEMY_SPEED, 0), ENEMY_IMAGE_PATH)
        self.is_alive = True

    def _constraints(self):
        if self.is_alive:
            if self.x > SCREEN_WIDTH - self.image.get_width() or self.x < 0:
                self.x_speed = -self.x_speed
                self.y = self.y + self.image.get_height()
            self.x += self.x_speed

    def _draw(self, screen):
        if self.is_alive:
            super()._draw(screen)

    def kill_player(self, player: Player):
        if self.is_alive \
                and player.is_alive \
                and self.x < player.x < self.x + self.image.get_width() \
                and self.y < player.y + 10 < self.y + self.image.get_height():
            player.is_alive = False


"""________________________________________________________________________"""


class Bullet(Mobile):
    def __init__(self, position=(0, 0)):
        super().__init__(position, (0, BULLET_SPEED), BULLET_IMAGE_PATH)
        self.is_fired = False

    def _draw(self, screen):
        if self.is_fired:
            super()._draw(screen)

    def _constraints(self):
        if self.is_fired:
            self.y -= self.y_speed
            if self.y < -self.image.get_height():
                self.is_fired = False

    def kill_enemy(self, enemies):
        if self.is_fired:
            for enemy in enemies:
                assert isinstance(enemy, Enemy)
                if enemy.is_alive \
                        and enemy.x < self.x < enemy.x + enemy.image.get_width() - self.image.get_width() \
                        and enemy.y < self.y < enemy.y + enemy.image.get_height():
                    enemy.is_alive = False
                    self.is_fired = False
                    break
