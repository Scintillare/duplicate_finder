import pygame
from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode((1200,800),HWSURFACE|DOUBLEBUF|RESIZABLE)
screen_width, screen_height = screen.get_size()

pic1=pygame.image.load("D:\Diana\Pictures\\gsf.jpg") #You need an example picture in the same folder as this file!
pic2=pygame.image.load("D:\Diana\Pictures\\gsf.jpg") #You need an example picture in the same folder as this file!
pic3=pygame.image.load("D:\Diana\Pictures\\gsf.jpg") #You need an example picture in the same folder as this file!

width, height = tuple(map(sum, zip(pic1.get_size(), pic2.get_size(), pic3.get_size())))
margin = 10
resize_scale = float(width+5*margin)/screen_width

screen.blit(pygame.transform.scale(pic1, tuple(map(lambda x: int(x/resize_scale), pic1.get_size()))), (margin, screen_height/4))
pygame.display.flip()
while True:
    pygame.event.pump()
    event=pygame.event.wait()
    if event.type==QUIT: 
        pygame.display.quit()
    elif event.type==VIDEORESIZE:
        print(event.dict)
        screen_width, screen_height = screen.get_size()
        resize_scale = float(width+5*margin)/screen_width
        screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)

        screen.blit(pygame.transform.scale(pic1, tuple(map(lambda x: int(x/resize_scale), pic1.get_size()))),(0,0))
        pygame.display.flip()
        
        