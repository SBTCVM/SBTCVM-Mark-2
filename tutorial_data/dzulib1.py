#!/usr/bin/env python
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
import pygame
pygame.display.init()
#this library should contain any functions and data needed by dezutezeoid
#that don't need to be in the actual engine executable

#some functions do rely on variables only present within DZU-ENG1.py however.
print ("dzulib initalized")
#inital main.sav file structure
savtree='''<?xml version="1.0" encoding="UTF-8"?>
<sav>
	<keysav>
	</keysav>
</sav>
'''
#main.sav init.
def initmainsave():
	print ('Initalize main.sav')
	mainsavfile = open('main.sav', 'w')
	mainsavfile.write(savtree)
	mainsavfile.close()

#image scrollers
def vscroll(scrollval, image):
	offs=image.get_height()
	newimage=image.copy()
	newimage.fill((0, 0, 0, 0))
	newimage.blit(image, (0, scrollval))
	if (str(scrollval))[0]=="-":
		newimage.blit(image, (0, (scrollval + offs)))
	else:
		newimage.blit(image, (0, (scrollval - offs)))
	return newimage

def hscroll(scrollval, image):
	offs=image.get_width()
	newimage=image.copy()
	newimage.fill((0, 0, 0, 0))
	newimage.blit(image, (scrollval, 0))
	if (str(scrollval))[0]=="-":
		newimage.blit(image, ((scrollval + offs), 0))
	else:
		newimage.blit(image, ((scrollval - offs), 0))
	return newimage

