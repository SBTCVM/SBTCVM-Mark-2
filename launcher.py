#!/usr/bin/env python
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
import pygame
import time
import copy
import sys
import os
import subprocess
from pygame.locals import *



print "SBTCVM Launcher v2.0"
pygame.display.init()
pygame.font.init()
pygame.mixer.init()

simplefontC = pygame.font.SysFont(None, 28)
simplefontB = pygame.font.SysFont(None, 19)
pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN])
pygame.display.set_caption(("SBTCVM Launcher"), ("SBTCVM Launcher"))

windowicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'icon.png'))
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((800, 600))
#image data:
bg=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'launchbg.jpg')).convert()
abticn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'about.png')).convert_alpha()
creditsicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'credits.png')).convert_alpha()
exiticn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'exit.png')).convert_alpha()
fvicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'fileview.png')).convert_alpha()
gtticn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'gtt.png')).convert_alpha()
introicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'intro.png')).convert_alpha()
menuicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'menu.png')).convert_alpha()
tutorialicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'tutorial.png')).convert_alpha()
settingsicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'settings.png')).convert_alpha()

icn1=bg.blit(menuicn, (5, 70))
icn2=bg.blit(tutorialicn, (68, 70))
icn3=bg.blit(gtticn, (145, 70))
icn4=bg.blit(introicn, (215, 70))
icn5=bg.blit(creditsicn, (282, 70))
icn6=bg.blit(fvicn, (348, 70))
icn7=bg.blit(abticn, (425, 70))
icn8=bg.blit(exiticn, (565, 70))
icn9=bg.blit(settingsicn, (490, 70))

menulabel=simplefontC.render("SBTCVM launcher", True, (0, 0, 0), (255, 255, 255))
bg.blit(menulabel, (158, 4))
#itemlabel=simplefontB.render(curmenudesc[(menuhighnum - 1)], True, (0, 0, 0), (255, 255, 255))
#bg.blit(itemlabel, (170, 34))
scupdate=1
qflg=0
while qflg==0:
	if scupdate==1:
		scupdate=0
		screensurf.blit(bg, (0, 0))
		pygame.display.update()
	time.sleep(0.1)
	for event in pygame.event.get():
		if event.type == QUIT:
			qflg=1
			break
		if event.type == KEYDOWN and event.key == K_F1:
			subprocess.Popen(["python", "MK2-TOOLS.py", "helpview", "launcher.txt"])
		if event.type == KEYDOWN and event.key == K_F8:
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-launcher.png')))
			break
		if event.type==MOUSEBUTTONDOWN:
			if icn1.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "MK2-MENU.py"])
			if icn2.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "SBTCVM_tutorial.py"])
			if icn3.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "MK2-RUN.py", "gtt.streg"])
			if icn4.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "MK2-RUN.py", "intro.streg"])
			if icn5.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "MK2-TOOLS.py", "uicredits"])
			if icn6.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "fileview.py"])
			if icn7.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "MK2-TOOLS.py", "textview", (os.path.join("VMSYSTEM", "launcherabout.txt"))])
			if icn8.collidepoint(event.pos)==1 and event.button==1:
				qflg=1
				break
			if icn9.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "settings.py"])
