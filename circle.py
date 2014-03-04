__author__ = 'marty'
import pygame

class circle(pygame.sprite.Sprite):
    def __init__(self,x,y,radius,name):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.radius=radius
        self.name=name


    def collidepoint(self,point):
        return (self.x-point[0])**2 + (self.y-point[1])**2<self.radius**2
