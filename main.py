from pygame import *
from random import randint

mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def draw(self):
        scr.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group()
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 5, 15, 20)
        bullets.add(bullet)


lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = -30
            self.rect.x = randint(-30, 600)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()


scr_size = (700, 500)

scr = display.set_mode(scr_size)

bg = transform.scale(image.load("galaxy.jpg"), scr_size)

player = Player("rocket.png", 100, 400, 3, 40, 50)


monsters = sprite.Group()

spawn_list = [0]  # Initialize with a value

for e in range(5):
    spawn = randint(0, 500)
    for s_l in spawn_list:
        while abs(s_l - spawn) < 100:
            spawn = randint(0, 500)
    spawn_list.append(spawn)
    enemy = Enemy("ufo.png", spawn, -30, 1, 50, 50)
    monsters.add(enemy)


# mixer_music.load("space.ogg")
# mixer_music.play()

fire_sound = mixer.Sound("fire.ogg")


win = font.Font(None, 70).render("You Win!!!", 1, (0, 255, 0))
lose = font.Font(None, 70).render("You Lose!!!", 1, (255, 0, 0))

hit = 0

finish = False
is_game = True

clock = time.Clock()

while is_game:
    while not finish:

        scr.blit(bg, (0, 0))
        player.draw()
        player.update()

        monsters.draw(scr)
        monsters.update()

        bullets.draw(scr)
        bullets.update()

        if hit >= 5:
            finish = True
            scr.blit(win, (100, 100))

        lost_text = font.Font(None, 36).render(f"Пролетело: {lost}", True, (255, 255, 255))
        scr.blit(lost_text, (10, 10))

        hits = font.Font(None, 36).render(f"Сбито: {hit}", True, (255, 255, 255))
        scr.blit(hits, (10, 40))


        collides = sprite.groupcollide(bullets, monsters, True, True)
        for collide in collides:
            hit += 1
            enemy = Enemy("ufo.png", randint(0, 500), -30, 1.2, 50, 50)
            monsters.add(enemy)

        if sprite.spritecollide(player, monsters, False) or lost >= 3:
            finish = True
            scr.blit(lose, (100, 100))



        for e in event.get():
            if e.type == QUIT:
                finish = True
                is_game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    fire_sound.play()
                    player.fire()

        clock.tick(60)
        display.update()

    for e in event.get():
        if e.type == QUIT:
             is_game = False

    clock.tick(60)
    display.update()
