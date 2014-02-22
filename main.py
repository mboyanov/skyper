__author__ = 'marty'

import pygame, math, sys
from pygame.locals import *
from skyper import skyper
from circle import circle
import operator
screen = pygame.display.set_mode((1024, 768))

clock = pygame.time.Clock()
myskyper=skyper()
data=myskyper.getData('xaxamy')
WHITE = (255,255,255)
circles=[]
circles.append(circle(512,384,40,'YOU'))
maxkey=max(data.iteritems(), key=operator.itemgetter(1))[0]
ratio=60/data[maxkey]
for d in data:
    data[d]=data[d]*ratio

index=0
print data
for d in data:
    x=int(512+math.cos(index*2*math.pi/len(data))*300)
    y=int(368+math.sin(index*2*math.pi/len(data))*300)
    circles.append(circle(x,y,int(data[d]),d))
    index=index+1

pygame.init()
while 1:
# USER INPUT
  clock.tick(30)
  for event in pygame.event.get():
    if not hasattr(event, 'key'):
      continue
    down = event.type == KEYDOWN # key down or up?

    if event.key == K_ESCAPE: sys.exit(0) # quit the game
  screen.fill(WHITE)
# SIMULATION
# .. new speed and direction based on acceleration and turn

  # .. new position based on current position, speed and direction



  font = pygame.font.SysFont("comicsansms", 16)

  for circle in circles:
      pygame.draw.circle(screen,(100,100,100),(circle.x,circle.y),circle.radius)


      screen.blit(font.render(circle.name,1,(0,0,0)), (circle.x-len(circle.name)*40/16,circle.y-circle.radius-16))
  # for i in range(len(data)):
  #   if sumr>1024:
  #     sumr=0
  #     y+=200
  #   sumr+=max(2*int(data[i][1]),100)
  #   pygame.draw.circle(screen, (100,100,100), (sumr,y), int(data[i][1]), 0)
  #   locs.append((sumr-30,y))
  # for i in range(len(data)):
  #   label = font.render(data[i][0], 12, (0,0,0))
  #   screen.blit(label, locs[i])





  pygame.display.flip()
