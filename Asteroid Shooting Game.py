'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
'''

'''
Samantha Bennefield
2/10/17
Mr. Davis
Asteroid Shooting Game
'''

import pygame
import sys
import random

listAsteroid=[]
listLaser=[]
leveltime=50
creationTime=leveltime
lives=3
score=0

#Images
spaceshipImg = pygame.image.load('spaceship.png') #<--The spaceship
spaceImg = pygame.image.load('space.jpg') #<--The planet thing in the background

#Colors
background = (0, 0, 0)
entity_color = (255, 255, 255)


#Background Music
pygame.mixer.init(44100, -16,2,2048)
pygame.mixer.music.load('bg_music.wav')
pygame.mixer.music.play(-1, 0.0)

#Sound Effects
soundObj1 = pygame.mixer.Sound('asteroid_explosion.wav')
soundObj2 = pygame.mixer.Sound('laser_sound.wav')
soundObj3 = pygame.mixer.Sound('ship_explosion.wav')


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Spaceship(Entity):
    def __init__(self, x, y, width, height):
        super(Spaceship, self).__init__(x, y, width, height)

        self.image = spaceshipImg


class Player(Spaceship):
    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)

        self.y_change = 0
        self.y_dist = 5

    def MoveKeyDown(self, key):
        if (key == pygame.K_UP): #<--Move ship up
            self.y_change += -self.y_dist
        elif (key == pygame.K_DOWN): #<--Move ship down
            self.y_change += self.y_dist
        elif (key == pygame.K_SPACE): #<--Fire bullet
            soundObj2.play() #<--Play laser sound
            bullet = Bullet(player.rect.x+90, player.rect.y+59, 10, 10)
            all_sprites_list.add(bullet)
            listLaser.append(bullet)

    def MoveKeyUp(self, key):
        if (key == pygame.K_UP):
            self.y_change += self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += -self.y_dist

    def update(self):
        self.rect.move_ip(0, self.y_change)

        #Keep the spaceship on screen
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > window_height - self.height:
            self.rect.y = window_height - self.height


class Asteroid(Entity):
    def __init__(self, x, y, width, height):
        super(Asteroid, self).__init__(x, y, width, height)

        self.image = pygame.Surface([width, height])
        self.image.fill(entity_color)

        self.x_direction = 5

        self.speed = 2

    def update(self):
        self.rect.x-=self.speed
        if self.rect.x <= 0:
            self.kill()


class Bullet(Entity):
    def __init__(self, x, y, width, height):
        super(Bullet, self).__init__(x, y, width, height)

        self.image = pygame.Surface([width, height])
        self.image.fill(entity_color)

        self.x_direction = 1
        self.y_direction = 0

        self.speed = 3

    def update(self):
        self.rect.move_ip(self.speed * self.x_direction,
                          self.speed * self.y_direction)

        if self.rect.x > window_width: #<---If it goes off the screen
            self.kill()


pygame.init()

window_width = 700
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Asteroids")

clock = pygame.time.Clock()

player = Player(20, window_height / 2, 20, 50) #<--The spaceship

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)


def checkKill(all):
    global lives
    for i in all:
        if i.rect.colliderect(player.rect):
            all.remove(i)
            i.remove(all_sprites_list)
            killed=True
            print('dead')
            lives-=1
            print(lives)


def laserHit(asteroids,lasers):
    global score
    for i in asteroids:
        for x in listLaser:
            if i.rect.colliderect(x):
                soundObj1.play()
                i.remove(all_sprites_list)
                x.remove(all_sprites_list)
                asteroids.remove(i)
                lasers.remove(x)
                score+=100
                print(score)


#The starting asteroid
First = Asteroid(window_width, random.randint(10, window_height - 10), 20, 20)
listAsteroid.append(First)

all_sprites_list.add(First)


fontObj = pygame.font.Font('freesansbold.ttf', 32)

#Score Text
textSurfaceObj = fontObj.render('Score:'+str(score), True, entity_color)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (590, 30)

#Lives Text
textSurfaceObj2 = fontObj.render('Lives:'+str(lives), True, entity_color)
textRectObj2 = textSurfaceObj2.get_rect()
textRectObj2.center = (80, 30)



start_screen=False
while (start_screen==False):
    screen.fill(background)
    textSurfaceObj4 = fontObj.render('Asteroids', True, entity_color)
    textRectObj4 = textSurfaceObj4.get_rect()
    textRectObj4.center = (360, 100)

    textSurfaceObj5 = fontObj.render('Press any key to start', True, entity_color)
    textRectObj5 = textSurfaceObj4.get_rect()
    textRectObj5.center = (270, 300)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            start_screen=True

    screen.blit(textSurfaceObj4, textRectObj4)
    screen.blit(textSurfaceObj5, textRectObj5)
    pygame.display.flip()

#Game Loop
while True:

    laserHit(listAsteroid, listLaser)
    checkKill(listAsteroid)

    file = open("highscore.txt", "w")

    if lives==0:
        listAsteroid=[]
        listLaser=[]
        creationTime=1
        soundObj3.play()
        all_sprites_list.remove(player)
        screen.fill(background)
        file.write(score)
        file.close()



    if creationTime <= 0:
        x = Asteroid(window_width, random.randint(10, window_height - 10), 20, 20)
        listAsteroid.append(x)
        all_sprites_list.add(x)
        leveltime -= 1
        creationTime = leveltime
        x.speed+=.1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            player.MoveKeyDown(event.key)
        elif event.type == pygame.KEYUP:
            player.MoveKeyUp(event.key)


    for ent in all_sprites_list:
        ent.update()

    screen.fill(background)
    screen.blit(spaceImg, (200, 200))
    screen.blit(textSurfaceObj, textRectObj)
    screen.blit(textSurfaceObj2, textRectObj2)

    textSurfaceObj = fontObj.render('Score:' + str(score), True, entity_color)
    textSurfaceObj2 = fontObj.render('Lives:' + str(lives), True, entity_color)
    textSurfaceObj3 = fontObj.render('Test', True, entity_color)

    all_sprites_list.draw(screen)

    creationTime -= 1

    pygame.display.flip()

    clock.tick(60)
