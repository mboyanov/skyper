__author__ = 'marty'

import pygame, math, sys
from pygame.locals import *
from skyper import skyper
from circle import circle
import operator
import MODE
import threading
screen = pygame.display.set_mode((1024, 768))
mode=MODE.general
clock = pygame.time.Clock()
myskyper = skyper('xaxamy')
circles=[]
data = myskyper.getData()
t=threading.Thread(target=myskyper.parseData)
t.daemon=True
t.start()

WHITE = (255, 255, 255)

circles.append(circle(512, 384, 40, 'YOU'))
maxkey = max(data.iteritems(), key=operator.itemgetter(1))[0]
ratio = 60 / data[maxkey]
for d in data:
    data[d] = data[d] * ratio

index = 0
print data
for d in data:
    x = int(512 + math.cos(index * 2 * math.pi / len(data)) * 300)
    y = int(368 + math.sin(index * 2 * math.pi / len(data)) * 300)
    circles.append(circle(x, y, int(data[d]), d))
    index = index + 1

pygame.init()
while 1:
    # USER INPUT
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            clicked_sprites = [c for c in circles if c.collidepoint(pos)]
            print clicked_sprites
            if len(clicked_sprites)>0:

                clicked_sprite=clicked_sprites[0]
                print (clicked_sprite.name)
                result=myskyper.getInfo(clicked_sprite.name)
                mode=MODE.person

        if not hasattr(event, 'key'):
            continue
        down = event.type == KEYDOWN  # key down or up?

        if event.key == K_ESCAPE: sys.exit(0)  # quit the game
    screen.fill(WHITE)




    font = pygame.font.SysFont("comicsansms", 16)

    if (mode==MODE.general):
        for circle in circles:
            pygame.draw.circle(screen, (100, 100, 100), (circle.x, circle.y), circle.radius)

            screen.blit(font.render(circle.name, 1, (0, 0, 0)),
                        (circle.x - len(circle.name) * 40 / 16, circle.y - circle.radius - 16))
    else:
        for r in range(len(result)):
            screen.blit(font.render(result[r] ,1, (0, 0, 0)),
                        (512-len(result[r])*40/16,r*30))





    pygame.display.flip()
