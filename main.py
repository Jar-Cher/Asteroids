# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # !/usr/bin/env python
    # -*- coding: utf-8 -*-
    import pygame, sys, math, time

    # from rot import *
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((640, 510))
    pygame.display.set_caption('Asteroids')
    done = True
    CONST = 10 ** 99


    def rot_center1(image, angle):
        """Поворачивет фигуру, сохраняя её форму и центр, но работает только с квадратами"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image


    def rot_center2(image, rect, angle):
        """Поворачивает любую фигуру, сохраняя её центр"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect


    def random(a, b):
        return ((CONST * time.time()) ** 0.33) % (b - a) + a


    """ Объявляем классы """


    class Hero(pygame.sprite.Sprite):
        def __init__(self, xpos, ypos, filename):
            self.x = xpos
            self.y = ypos
            self.bitmap = pygame.image.load(filename)
            self.bitmap.set_colorkey((255, 255, 255))

        def render(self):
            screen.blit(self.bitmap, (self.x, self.y))


    class Enemy(pygame.sprite.Sprite):
        def __init__(self, xpos, ypos, filename):
            self.x = xpos
            self.y = ypos
            self.bitmap = pygame.image.load(filename)  # Привет Игорь
            self.bitmap.set_colorkey((255, 255, 255))
            self.lifetime = 0

        def render(self):
            screen.blit(self.bitmap, (self.x, self.y))


    class bullet(pygame.sprite.Sprite):
        def __init__(self, xpos, ypos, filename, vector, lt, sd):
            self.x = xpos
            self.y = ypos
            self.bitmap = pygame.image.load(filename)
            self.bitmap.set_colorkey((255, 255, 255))
            # self.ship = instal
            self.angle = vector
            # bullets.add(self)
            self.lifetime = lt
            self.sound = sd
            self.sound.play()

        def render(self):
            screen.blit(self.bitmap, (self.x, self.y))


    # class basic_rocket(pygame.sprite.Sprite.weapon):
    # def __init__(self,ima = 'basic_rocket'):
    # self.angle = hero.angle
    # self.name = ima
    fbullets = []
    enemies = []
    ebullets = []
    """ Создаем Героя, загружаем файлы """
    hero = Hero(320, 240, 'data/ship.bmp')
    original_bitmap = pygame.image.load('data/ship.bmp')
    original_bitmap.set_colorkey((250, 250, 250))
    music = pygame.mixer.Sound('data/theme1.wav')
    thrust_sound = pygame.mixer.Sound('data/thrust.wav')
    bullet_sound = pygame.mixer.Sound('data/missile.wav')
    screen = pygame.image.load('data/nebula.jpg')
    """ Создаём информационную строку """
    info_string = pygame.Surface((640, 30))
    """ Устанавливаем стартовые переменные """
    basic_font = pygame.font.SysFont('Arial', 20)
    hero.angle = 0
    hero.ux = 0
    hero.uy = 0
    hero.expl = 0
    hero.reload = 51
    hero.alive = True
    # start_rocket = basic_rocket('starting_one')
    # hero.gun = [start_rocket]
    music.play(-1)
    pygame.key.set_repeat(1, 1)
    gametime = 0
    f = open('data/data.txt', 'r')
    max_score = int(f.read())
    score = 0
    f.close()
    clock = pygame.time.Clock()
    while done:
        clock.tick(30)
        """ Обработка событий """
        for i in pygame.event.get():
            """ Выход из игры по нажатию крестика"""
            if i.type == pygame.QUIT:
                done = False
            """ Обработка нажатий клавиш"""
            if (i.type == pygame.KEYDOWN) and (hero.alive == True):
                if (i.key == pygame.K_UP):
                    """Герой ускоряется, воспроизводится звук двигателя"""
                    hero.uy = math.cos(hero.angle * (math.pi / 180)) * 0.1 + hero.uy
                    hero.ux = math.sin(hero.angle * (math.pi / 180)) * 0.1 + hero.ux
                    thrust_sound.play()
                if (i.key == pygame.K_RIGHT):
                    """Герой поворачивается вправо"""
                    hero.angle = (hero.angle - 1) % 360
                    # hero.bitmap = pygame.transform.rotate(original_bitmap,hero.angle)
                    hero.bitmap = rot_center1(original_bitmap, hero.angle)
                if (i.key == pygame.K_LEFT):
                    """Герой поворачивается влево"""
                    hero.angle = (hero.angle + 1) % 360
                    # hero.bitmap = pygame.transform.rotate(original_bitmap,hero.angle)
                    hero.bitmap = rot_center1(original_bitmap, hero.angle)
                if (i.key == pygame.K_SPACE) and (hero.reload > 50):
                    """Если время перезарядки больше 50, то Герой открывает огонь, воспроизводится звук выстрела, время перезарядки обнуляется"""
                    new = bullet(hero.x + 13, hero.y + 13, 'data/missile.bmp', hero.angle, 100, bullet_sound)
                    # new.bitmap.set_colorkey((250,250,250))
                    fbullets.append(new)
                    hero.reload = 0
        window.blit(info_string, (0, 480))
        window.blit(screen, (0, 0))
        """Проверяем, не вылетел ли герой слишком далеко за пределы экрана"""
        if (675 > hero.x > -35):
            hero.x -= hero.ux
        elif (hero.x < -35):
            hero.x = 674
        elif (hero.x > 675):
            hero.x = -34
        if (515 > hero.y > -35):
            hero.y -= hero.uy
        elif (hero.y < -35):
            hero.y = 514
        elif (hero.y > 515):
            hero.y = -34

        info = '     Score: ' + str(score) + '     High score: ' + str(max_score)
        pygame.display.flip()

        screen = pygame.image.load('data/nebula.jpg')
        info_string.fill((45, 80, 40))
        info_string.blit(basic_font.render(info, 1, (210, 120, 200)), (0, 5))
        """ Увеличиваем 'время' """
        hero.reload += 1
        gametime += 1
        if (gametime % 150 == 0) and (hero.alive == True):
            new = Enemy(random(0, 586), random(0, 426), 'data/enemy.gif')
            # new = Enemy(310, random(0,426), 'data/enemy.gif')
            enemies.append(new)
        """Обработка полёта снарядов"""
        for j in fbullets:
            j.x = -math.sin(j.angle * (math.pi / 180)) * 3.5 + j.x
            j.y = -math.cos(j.angle * (math.pi / 180)) * 3.5 + j.y
            j.render()
            j.lifetime -= 1
            for p in enemies:
                if math.sqrt(((p.x + 27) - (j.x + 4)) ** 2 + ((p.y + 27) - (j.y + 4)) ** 2) <= 31:
                    fbullets.remove(j)
                    enemies.remove(p)
                    score += 1
                    if score > max_score:
                        max_score = score
            if j.lifetime == 0:
                fbullets.remove(j)
        for j in ebullets:
            j.x = -math.sin(j.angle * (math.pi / 180)) * 3.5 + j.x
            j.y = -math.cos(j.angle * (math.pi / 180)) * 3.5 + j.y
            j.render()
            j.lifetime -= 1
            # for p in enemies:
            # if math.sqrt(((p.x+27)-(j.x+4))**2 + ((p.y+27)-(j.y+4))**2)<=31:
            # fbullets.remove(j)
            # enemies.remove(p)
            # score += 1
            # if score > max_score:
            # max_score = score
            if j.lifetime == 0:
                ebullets.remove(j)
            if (math.sqrt(((hero.x + 17) - (j.x + 4)) ** 2 + ((hero.y + 17) - (j.y + 4)) ** 2) <= 21) and (
                    hero.alive == True):
                hero.alive = False
                music.stop()
                music = pygame.mixer.Sound('data/IWBTB_Soundtrack_-_04_-_Game_Over.ogg')
                hero.x -= 20
                hero.y -= 20
                music.play()
                ebullets.remove(j)
        for j in enemies:
            j.lifetime += 1
            if (j.lifetime % 50 == 0) and (hero.alive == True):
                if (j.x >= hero.x) and (j.x - hero.x != -10):
                    deg = 90 - math.degrees(math.atan(((j.y + 27) - (hero.y + 17)) / ((j.x + 27) - (hero.x + 17))))
                elif (j.x - hero.x == -10):
                    if (j.y >= hero.y):
                        deg = 0
                    else:
                        deg = 180
                else:
                    deg = -90 + math.degrees(-math.atan(((j.y + 27) - (hero.y + 17)) / ((j.x + 27) - (hero.x + 17))))
                new = bullet(j.x + 27, j.y + 27, 'data/missile.bmp', deg, 250, bullet_sound)
                ebullets.append(new)
                j.lifetime = 0
            j.render()
        if hero.alive == False:
            if hero.expl < 10:
                hero.expl += 1
                hero.bitmap = pygame.image.load('data/explosion' + str(hero.expl) + '.bmp')
                hero.bitmap.set_colorkey((255, 255, 255))
        hero.render()
    pygame.quit()
    f = open('data/data.txt', 'w')
    f.write(str(max_score))
    f.close()