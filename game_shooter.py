from pygame import *
from random import *
from time import time as timer

okie_width = 1200
okie_height = 700
display.set_caption('ZXC 1000-7')

okienko = display.set_mode((okie_width, okie_height))
background = transform.scale(image.load('background3.png'), (okie_width, okie_height))

score = 0
lost = 0
max_lost = 4
goal = 15
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        okienko.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < okie_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Shadow_Fiend(GameSprite):
    #???
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > okie_height:
            self.rect.x = randint(90, okie_width - 90)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > okie_height:
            self.rect.x = randint(80, okie_width - 80)
            self.rect.y = 0


squiller = Player('hoodwink.png', 9, okie_height-170, 150, 180, 15)

asteroids = sprite.Group()
for i in range(1, 6):
    stone = Asteroid('asteroid.png', randint(90, okie_width - 90), -40, 130, 150, randint(1, 8))
    asteroids.add(stone)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Shadow_Fiend('SF.png', randint(90, okie_width - 90), -40, 130, 150, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

mixer.init()
mixer.music.load('Where.mp3')
mixer.music.play()

fire_sound = mixer.Sound('hoodwink_attack.mpeg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('ПОБЕДА!', True, (255, 255, 255))
font2 = font.Font(None, 36)

run = True
finish = False

rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire += 1
                    fire_sound.play()
                    squiller.fire()
                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish:
        okienko.blit(background, (0, 0))

        text = font2.render('Счет:' + str(score), 1, (245, 255, 255))
        okienko.blit(text, (10, 20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (245, 255, 255))
        okienko.blit(text_lose, (10, 50))

        squiller.update()
        squiller.reset()

        monsters.update()
        monsters.draw(okienko)

        bullets.update()
        bullets.draw(okienko)

        asteroids.draw(okienko)
        asteroids.update()

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait...', 1, (233, 171, 171))
                okienko.blit(reload, (200, 480))
            else:
                rel_time = False
                num_fire = 0

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Shadow_Fiend('SF.png', randint(90, okie_width - 90), -40, 130, 150, randint(1, 5))
            monsters.add(monster)

        lose = font1.render(f'ПОРАЖЕНИЕ! Вы сбили {score} гуля(-ей)', True, (187, 30, 0))

        if sprite.spritecollide(squiller, monsters, True) or sprite.spritecollide(squiller, asteroids, True):
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            okienko.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            okienko.blit(win, (200, 200))

        if life == 3:
            life_color = (128, 255, 0)

        if life == 2:
            life_color = (51, 201, 0)

        if life == 1:
            life_color = (255, 0, 0)

        text_num_fire = font1.render(str(num_fire), 1, (128, 255, 0))
        text_life = font1.render(str(life), 1, life_color)
        okienko.blit(text_life, (1100, 20))
        okienko.blit(text_num_fire, (20, 80))
    display.update()
    time.delay(60)

