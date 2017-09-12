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
import VMSYSTEM.liblaunchutils as launchutils

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
screensurf=pygame.display.set_mode((800, 600), pygame.RESIZABLE)
screenx=800
screeny=600
vmui.initui(screensurf, 1)

diagabt="""Launcher v3.0
Part of the SBTCVM Project
Copyright (c) 2016-2017 Thomas Leathers and Contributors

See README.md for more information."""

#image data:
#bghud=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'launchhud.png')).convert_alpha()
bghud=pygame.Surface((screenx, screeny), SRCALPHA)


bg=(libthemeconf.bgmake(bghud)).convert()

sbtcvmbadge=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'SBTCVMbadge.png')).convert()
bgoverlay=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'helpbgover.png')).convert_alpha()

gtticn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'gtt.png')).convert()
introicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'intro.png')).convert()

DUMMY=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'dummy.png')).convert()
helpicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'help.png')).convert()
fvicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'fileview.png')).convert()
settingsicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'settings.png')).convert()
themeicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'theme.png')).convert()

calcicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'calc.png')).convert()
creditsicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'credits.png')).convert()

romicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'ROM.png')).convert()


#fvfilemenu=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'fvfilemenu.png')).convert()
fmicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'filemenuicon.png')).convert_alpha()
fvfilemenu=vmui.makemenubtn("FILE", icon=fmicon)
fvcatmenu=vmui.makemenubtn("CATEGORY", width=80)
#fvcatmenu=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'catmenu.png')).convert()


class launchtile:
	def __init__(self, label, icon, ltype, lref=None, lref2=None):
		self.label=label
		self.textren=tilefont.render(self.label, True, libthemeconf.tiletext)
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
		self.tilesurf.fill(libthemeconf.tilecolor)
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
			if self.ltype==3:
				if self.lref2!=None:
					return (self.lref, self.lref2)
				else:
					return (self.lref, None)
			if self.ltype==1:
				subprocess.Popen(["python", "MK2-RUN.py", "-k", self.lref])
			if self.ltype==2:
				subprocess.Popen(["python", "MK2-RUN.py", self.lref])
			
#create launchtile objects
helpt=launchtile("Help", helpicn, 0, lref="helpview.py")
filet=launchtile("FileView", fvicn, 0, lref="fileview2.py")
settingt=launchtile("Settings", settingsicn, 0, lref="settings.py")
themet=launchtile("Theme", themeicn, 0, lref="theme.py")

calct=launchtile("Calc", calcicn, 0, lref="calc.py")
creditt=launchtile("Credits", creditsicn, 0, lref="MK2-TOOLS.py", lref2="uicredits")
introt=launchtile("intro", introicn, 1, lref="intro.streg")
gttt=launchtile("GTT", gtticn, 2, lref="gtt.streg")
starryt=launchtile("Starry", romicon, 2, lref="starry.streg")
rayburstt=launchtile("Ray Burst", romicon, 2, lref="rayburst.streg")
dazzlet=launchtile("Dazzle", romicon, 1, lref="dazzle.streg")
pixelpatt=launchtile("Pixel Patterns", romicon, 2, lref="pixelpat.streg")
#launch tools
widtest=launchtile("Test tool", romicon, 3, lref="TEST")

#testwid=launchutils.testwid(screensurf, 40, 40)
activewids=[]

#category lists
maincat=[filet, calct, settingt, themet, helpt, creditt]
gamescat=[gttt]
welcomecat=[introt, creditt]
democat=[introt, starryt, rayburstt, dazzlet, pixelpatt]
ltoolcat=[widtest]
#category definitions
tilelist=maincat
catid=0
catname="Main"

#categoru menu
cmitem0=vmui.menuitem("Main", "MAIN")
cmitem1=vmui.menuitem("Games", "GAMES")
cmitem2=vmui.menuitem("Welcome", "WELCOME")
cmitem3=vmui.menuitem("Demos", "DEMOS")
cmitem4=vmui.menuitem("Mini Tools", "LTOOL")
catmenu=[cmitem0, cmitem1, cmitem2, cmitem3, cmitem4]


#widitem0=vmui.menuitem("main", 

#file menu
fmhelp=vmui.menuitem("Help (F1)", "HELP")
fmabout=vmui.menuitem("About Launcher", "ABOUT")
fmabout2=vmui.menuitem("About SBTCVM", "ABOUT2")
fmbg=vmui.menuitem("Background", "SETBG")
fmquit=vmui.menuitem("Quit", "QUIT")
filemenu=[fmhelp, fmabout, fmabout2, fmbg, fmquit]

versnumgfx=simplefontB.render("v2.0.3", True, libthemeconf.hudtext)



movewid=0
widtomove=None

scupdate=1
qflg=0
resizeflg=0
while qflg==0:
	if resizeflg==1:
		resizeflg=2
	elif resizeflg==2:
		screensurf=pygame.display.set_mode((resw, resh), pygame.RESIZABLE)
		bg=(libthemeconf.bgmake(None)).convert()
		bg=pygame.transform.scale(bg, (resw, resh))
		scupdate=1
		resizeflg=0	
		screeny=resh
		screenx=resw
	#display drawing
	if scupdate==1:
		scupdate=0
		screensurf.fill(libthemeconf.deskcolor)
		screensurf.blit(bg, (0, 0))
		hudrect=pygame.Rect(0, 0, screenx, 44)
		screensurf.blit(bgoverlay, ((screenx - 250), (screeny - 250)))
		pygame.draw.rect(screensurf, libthemeconf.hudbg, hudrect, 0)
		screensurf.blit(sbtcvmbadge, ((screenx-120), 0))
		screensurf.blit(versnumgfx, ((screenx - versnumgfx.get_width() - 10), 30))
		tilex=10
		tiley=60
		tilejumpx=100
		tilejumpy=95
		filemx=screensurf.blit(fvfilemenu, (3, 3))
		catmx=screensurf.blit(fvcatmenu, (48, 3))
		menulabel=catfont.render(catname, True, libthemeconf.btntext)
		screensurf.blit(menulabel, ((48+40-(menulabel.get_width() // 2)), 5))
		#tile render
		
		for tile in tilelist:
			tile.render(tilex, tiley)
			if tilex+tilejumpx+90<screenx:
				tilex += tilejumpx
			else:
				tilex=10
				tiley += tilejumpy
		activewids.sort(key=lambda x: x.wo, reverse=True)
		for wid in activewids:
			wid.render()
		pygame.display.update()
	else:
		uptlist=list()
		activewids.sort(key=lambda x: x.wo, reverse=True)
		for wid in activewids:
			wid.render()
			uptlist.extend([wid.framerect])
		pygame.display.update(uptlist)
	if movewid==1:
		prevpos=movepos
		movepos=pygame.mouse.get_pos()
		xoff =(prevpos[0] - movepos[0])
		yoff =(prevpos[1] - movepos[1])
		widtomove.movet(xoff, yoff)
		scupdate=1
		time.sleep(0.04)
	else:
		time.sleep(0.1)
	#event handler
	for event in pygame.event.get():
		if event.type == QUIT:
			qflg=1
			for wid in activewids:
				wid.hostquit()
			break
		if event.type == KEYDOWN and event.key == K_F1:
			subprocess.Popen(["python", "helpview.py", "launcher.xml"])
		elif event.type == KEYDOWN and event.key == K_F8:
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-launcher.png')))
			break
		elif event.type == KEYDOWN:
			for wid in activewids:
				if wid.wo==0:
					wid.keydown(event)
		if event.type == KEYUP:
			for wid in activewids:
				if wid.wo==0:
					wid.keyup(event)
		if event.type==VIDEORESIZE:
			resizeflg=1
			resw=event.w
			resh=event.h
			time.sleep(0.1)
			break
		if event.type==MOUSEBUTTONUP:
			if movewid==1:
				movewid=0
		if event.type==MOUSEBUTTONDOWN:
			#process tile clicks
			notile=0
			#first=1
			activewids.sort(key=lambda x: x.wo, reverse=False)
			for wid in activewids:
				#if wid.wo==0 and first==1:
				#	print "fun"
				#first=0
				if wid.framerect.collidepoint(event.pos)==1:
					notile=1
					if not wid.widbox.collidepoint(event.pos)==1:
						if wid.closerect.collidepoint(event.pos)==1 and event.button==1:
							wid.close()
							activewids.remove(wid)
							scupdate=1
							break
						else:
							movewid=1
							movepos=event.pos
							widtomove=wid
							if wid.wo!=0:
								wid.wo=0
								activewids.remove(wid)
								for widd in activewids:
									widd.wo += 1
								activewids.extend([wid])
							break
							#activewids.insert(0, wid)
							#activewids.sort(key=lambda x: x.wo, reverse=True)
					else:
						wid.click(event)
						if wid.wo!=0:
							wid.wo=0
							activewids.remove(wid)
							for widd in activewids:
								widd.wo += 1
							activewids.extend([wid])
						break
			if notile==0:
				for tile in tilelist:
					if tile.tilebox.collidepoint(event.pos)==1 and event.button==1:
						actret=tile.act()
						if actret!=None:
							widis=launchutils.widlookup(actret[0])
							widx=widis(screensurf, 0, 40, 40, argument=actret[1])
							#ctivewids=activewids + [widx]
							for wid in activewids:
								wid.wo += 1
							activewids.extend([widx])
							#activewids.sort(key=lambda x: x.wo, reverse=True)
							
							
			#file menu
			if filemx.collidepoint(event.pos)==1 and event.button==1:
				menuret=vmui.menuset(filemenu, 3, 43, reclick=0, fontsize=26)
				if menuret=="HELP":
					subprocess.Popen(["python", "helpview.py", "launcher.xml"])
				if menuret=="ABOUT2":
					subprocess.Popen(["python", "MK2-TOOLS.py", "textview", "README.md"])
				if menuret=="ABOUT":
					vmui.okdiag(diagabt, (screenx // 2), (screeny // 2))
				if menuret=="SETBG":
					vmui.settheme(3, 43)
					scupdate=1
					bg=(libthemeconf.bgmake(None)).convert()
					bg=pygame.transform.scale(bg, (screenx, screeny))
				if menuret=="QUIT":
					qflg=1
					for wid in activewids:
						wid.hostquit()
					break
			#category menu
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
				if menuret=="LTOOL":
					tilelist=ltoolcat
					catid=4
					catname="Mini Tools"
					scupdate=1
