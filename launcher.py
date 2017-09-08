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
import VMSYSTEM.libvmui as vmui
import VMSYSTEM.libvmconf as libvmconf
import VMSYSTEM.libthemeconf as libthemeconf


print "SBTCVM Launcher v3.0"
pygame.display.init()
pygame.font.init()

simplefontC = pygame.font.SysFont(None, 28)
simplefontB = pygame.font.SysFont(None, 19)
tilefont = pygame.font.SysFont(None, 19)
catfont = pygame.font.SysFont(None, 19)

pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN])
pygame.display.set_caption(("SBTCVM Launcher"), ("SBTCVM Launcher"))

windowicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'icon.png'))
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((800, 600))
screenx=800
screeny=600
vmui.initui(screensurf, 1)

diagabt="""Launcher v3.0
Part of the SBTCVM Project
Copyright (c) 2016-2017 Thomas Leathers and Contributors

See README.md for more information."""

#image data:
bghud=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'launchhud.png')).convert_alpha()


bg=(libthemeconf.bgmake(bghud)).convert()
#abticn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'about.png')).convert_alpha()
#exiticn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'exit.png')).convert_alpha()
gtticn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'gtt.png')).convert()
introicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'intro.png')).convert()
#menuicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'menu.png')).convert_alpha()

DUMMY=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'dummy.png')).convert()
helpicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'help.png')).convert()
fvicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'fileview.png')).convert()
settingsicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'settings.png')).convert()
calcicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'calc.png')).convert()
creditsicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'credits.png')).convert()

romicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'ROM.png')).convert()


fvfilemenu=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'fvfilemenu.png')).convert()
fvcatmenu=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'catmenu.png')).convert()


class launchtile:
	def __init__(self, label, icon, ltype, lref=None, lref2=None):
		self.label=label
		self.textren=tilefont.render(self.label, True, (0, 0, 0))
		self.icon=icon
		self.ltype=ltype
		self.lref=lref
		self.lref2=lref2
		self.tileh=90
		self.tilew=90
		self.iconw=60
		self.iconh=60
		self.tilebox=pygame.Rect(0, 0, self.tileh, self.tilew)
		self.tilesurf=pygame.Surface((self.tilew, self.tileh), SRCALPHA)
		self.tilesurf.fill((255, 255, 255, 200))
		self.textx=((self.tileh // 2) - (self.textren.get_width() // 2))
		self.iconx=((self.tileh // 2) - (self.icon.get_width() // 2))
		self.icony=3
		self.texty=(self.icony+self.iconh+3)
		self.tilesurf.blit(self.icon, (self.iconx, self.icony))
		self.tilesurf.blit(self.textren, (self.textx, self.texty))
		
		
	def render(self, xpos, ypos):
		self.tilebox=screensurf.blit(self.tilesurf, (xpos, ypos))
	def act(self):
		if self.lref!=None:
			if self.ltype==0:
				if self.lref2!=None:
					subprocess.Popen(["python", self.lref, self.lref2])
				else:
					subprocess.Popen(["python", self.lref])
			if self.ltype==1:
				subprocess.Popen(["python", "MK2-RUN.py", "-k", self.lref])
			if self.ltype==2:
				subprocess.Popen(["python", "MK2-RUN.py", self.lref])
			

helpt=launchtile("Help", helpicn, 0, lref="helpview.py")
filet=launchtile("FileView", fvicn, 0, lref="fileview2.py")
settingt=launchtile("Settings", settingsicn, 0, lref="settings.py")
calct=launchtile("Calc", calcicn, 0, lref="calc.py")
creditt=launchtile("Credits", creditsicn, 0, lref="MK2-TOOLS.py", lref2="uicredits")
introt=launchtile("intro", introicn, 1, lref="intro.streg")
gttt=launchtile("GTT", gtticn, 1, lref="gtt.streg")
starryt=launchtile("Starry", romicon, 2, lref="starry.streg")
rayburstt=launchtile("Ray Burst", romicon, 2, lref="rayburst.streg")
dazzlet=launchtile("Dazzle", romicon, 1, lref="dazzle.streg")
pixelpatt=launchtile("Pixel Patterns", romicon, 2, lref="pixelpat.streg")
#category lists
maincat=[filet, calct, settingt, helpt, creditt]
gamescat=[gttt]
welcomecat=[introt, creditt]
democat=[introt, starryt, rayburstt, dazzlet, pixelpatt]

#category definitions
tilelist=maincat
catid=0
catname="Main"

cmitem0=vmui.menuitem("Main", "MAIN")
cmitem1=vmui.menuitem("Games", "GAMES")
cmitem2=vmui.menuitem("Welcome", "WELCOME")
cmitem3=vmui.menuitem("Demos", "DEMOS")
catmenu=[cmitem0, cmitem1, cmitem2, cmitem3]

fmhelp=vmui.menuitem("Help (F1)", "HELP")
fmabout=vmui.menuitem("About Launcher", "ABOUT")
fmabout2=vmui.menuitem("About SBTCVM", "ABOUT2")
fmbg=vmui.menuitem("Background", "SETBG")
fmquit=vmui.menuitem("Quit", "QUIT")
filemenu=[fmhelp, fmabout, fmabout2, fmbg, fmquit]



#menulabel=simplefontC.render("SBTCVM launcher v2.0", True, (0, 0, 0))
#bg.blit(menulabel, (258, 4))
#itemlabel=simplefontB.render(curmenudesc[(menuhighnum - 1)], True, (0, 0, 0), (255, 255, 255))
#bg.blit(itemlabel, (170, 34))
scupdate=1
qflg=0
while qflg==0:
	if scupdate==1:
		scupdate=0
		screensurf.blit(bg, (0, 0))
		tilex=10
		tiley=60
		tilejumpx=100
		tilejumpy=95
		filemx=screensurf.blit(fvfilemenu, (3, 3))
		catmx=screensurf.blit(fvcatmenu, (48, 3))
		menulabel=catfont.render(catname, True, (0, 0, 0))
		screensurf.blit(menulabel, ((48+40-(menulabel.get_width() // 2)), 5))
		#menulabel=simplefontC.render("Category: " + catname, True, (0, 0, 0))
		#screensurf.blit(menulabel, (258, 4))
		for tile in tilelist:
			tile.render(tilex, tiley)
			if tilex+tilejumpx<screenx:
				tilex += tilejumpx
			else:
				tilex=10
				tiley += tilejumpy
		pygame.display.update()
	time.sleep(0.1)
	for event in pygame.event.get():
		if event.type == QUIT:
			qflg=1
			break
		if event.type == KEYDOWN and event.key == K_F1:
			subprocess.Popen(["python", "helpview.py", "launcher.xml"])
		if event.type == KEYDOWN and event.key == K_F8:
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-launcher.png')))
			break
		if event.type==MOUSEBUTTONDOWN:
			for tile in tilelist:
				if tile.tilebox.collidepoint(event.pos)==1 and event.button==1:
					tile.act()
			if filemx.collidepoint(event.pos)==1 and event.button==1:
				menuret=vmui.menuset(filemenu, 3, 43, reclick=0, fontsize=26)
				if menuret=="HELP":
					subprocess.Popen(["python", "helpview.py", "launcher.xml"])
				if menuret=="ABOUT2":
					subprocess.Popen(["python", "MK2-TOOLS.py", "textview", "README.md"])
				if menuret=="ABOUT":
					vmui.okdiag(diagabt, (screenx // 2), (screeny // 2))
				if menuret=="SETBG":
					libthemeconf.settheme(3, 43)
					scupdate=1
					bg=(libthemeconf.bgmake(bghud)).convert()
					#bgret=vmui.menuset(bgmenu, 3, 43, reclick=0, fontsize=26)
					#if bgret=="BG0":
						##bg=bg0
						#scupdate=1
						#libthemeconf.setconf("desk", "bgtheme", "0")
						#libthemeconf.saveconf()
						#bg=(libthemeconf.bgmake(bghud)).convert()
					#if bgret=="BG1":
						##bg=bg1
						#scupdate=1
						#libthemeconf.setconf("desk", "bgtheme", "1")
						#libthemeconf.saveconf()
						#bg=(libthemeconf.bgmake(bghud)).convert()
						
				if menuret=="QUIT":
					qflg=1
					break
			if catmx.collidepoint(event.pos)==1 and event.button==1:
				menuret=vmui.menuset(catmenu, 48, 43, reclick=0, fontsize=26)
				if menuret=="MAIN":
					tilelist=maincat
					catid=0
					catname="Main"
					scupdate=1
				if menuret=="GAMES":
					tilelist=gamescat
					catid=1
					catname="Games"
					scupdate=1
				if menuret=="WELCOME":
					tilelist=welcomecat
					catid=2
					catname="Welcome"
					scupdate=1
				if menuret=="DEMOS":
					tilelist=democat
					catid=3
					catname="Demos"
					scupdate=1
			#if icn1.collidepoint(event.pos)==1 and event.button==1:
				#subprocess.Popen(["python", "MK2-MENU.py"])
			#if icn2.collidepoint(event.pos)==1 and event.button==1:
				#subprocess.Popen(["python", "helpview.py"])
			#if icn3.collidepoint(event.pos)==1 and event.button==1:
				#subprocess.Popen(["python", "MK2-RUN.py", "-k", "gtt.streg"])
			#if icn4.collidepoint(event.pos)==1 and event.button==1:
				#subprocess.Popen(["python", "MK2-RUN.py", "-k", "intro.streg"])
			#if icn5.collidepoint(event.pos)==1 and event.button==1:
				#subprocess.Popen(["python", "MK2-TOOLS.py", "uicredits"])
			#if icn6.collidepoint(event.pos)==1 and event.button==1:
				#subprocess.Popen(["python", "fileview2.py"])
			#if icn7.collidepoint(event.pos)==1 and event.button==1:
				##subprocess.Popen(["python", "MK2-TOOLS.py", "textview", (os.path.join("VMSYSTEM", "launcherabout.txt"))])
				#subprocess.Popen(["python", "MK2-TOOLS.py", "textview", "README.md"])
			#if icn8.collidepoint(event.pos)==1 and event.button==1:
			#	qflg=1
			#	break
			#if icn9.collidepoint(event.pos)==1 and event.button==1:
				#subprocess.Popen(["python", "settings.py"])
			#if icn10.collidepoint(event.pos)==1 and event.button==1:
				#subprocess.Popen(["python", "calc.py"])
