# создай игру "Лабиринт"!

from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < height - 80:
            self.rect.y += self.speed


class Enemy(GameSprite):
    direction = "left"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        if self.direction == "right":
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, wall_x, wall_y, wall_w, wall_h):
        super().__init__()
        self.color1, self.color2, self.color3 = color1, color2, color3
        self.w, self.h = wall_w, wall_h
        self.image = Surface((self.w, self.h))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


width = 700
height = 500
window = display.set_mode((width, height))
display.set_caption("Лабиринт")
background = transform.scale(image.load("background.jpg"), (width, height))
clock = time.Clock()
FPS = 60
game = True
finish = True
mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()

money = mixer.Sound("money.ogg")
kick = mixer.Sound("kick.ogg")

player = Player("hero.png", 5, height - 80, 4)
monster = Enemy("cyborg.png", width - 80, 280, 2)
treasures = GameSprite("treasure.png", width - 120, height - 80, 0)

w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20, 10, 380)
w4 = Wall(154, 205, 50, 200, 130, 10, 350)
w5 = Wall(154, 205, 50, 450, 130, 10, 360)
w6 = Wall(154, 205, 50, 300, 20, 10, 350)
w7 = Wall(154, 205, 50, 390, 120, 130, 10)

font.init()
font = font.SysFont("Arial", 70)
win = font.render("YOU WIN!", True, (255, 215, 0))
lose = font.render("YOU LOSE!", True, (180, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        monster.update()
        monster.reset()
        treasures.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()

        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or \
            sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or \
            sprite.collide_rect(player, w6) or sprite.collide_rect(player, w7):
            finish = False
            window.blit(lose, (200, 200))
            kick.play()

        if sprite.collide_rect(player, treasures):
            finish = False
            window.blit(win, (200, 200))
            money.play()

        display.update()
    clock.tick(FPS)
