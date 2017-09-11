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
#import VMSYSTEM.libvmconf as libvmconf
import VMSYSTEM.libvmui as vmui
import VMSYSTEM.libthemeconf as libthemeconf

pygame.display.init()
pygame.font.init()
pygame.display.set_caption(("Theme"), ("Theme"))

windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'settings64.png'))
pygame.display.set_icon(windowicon)

screensurf=pygame.display.set_mode((450, 300))
screenx=450
screeny=300
vmui.initui(screensurf, 1)
#image data
sbtcvmbadge=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'SBTCVMbadge.png')).convert()
#setbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'settingsbg2.jpg')).convert()
#swon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'switchon.png')).convert()
#swoff=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'switchoff.png')).convert()
swn=vmui.makeswitchbtn("ON", "OFF")
swon=swn[0]
swoff=swn[1]

#bgbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'bgbtn.png')).convert()
#themebtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'themebtn.png')).convert()
#fvfilemenu=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'fvfilemenu.png')).convert()

fmicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'filemenuicon.png')).convert_alpha()
fvfilemenu=vmui.makemenubtn("FILE", icon=fmicon)
bgbtn=vmui.makemenubtn("BACKGROUND", width=89)
themebtn=vmui.makemenubtn("THEME", width=120)

simplefontC = pygame.font.SysFont(None, 28)
simplefontB = pygame.font.SysFont(None, 19)
catfont = pygame.font.SysFont(None, 19)

iterate1=os.path.join("VMSYSTEM", "CFG")
iterate2=os.path.join("VMUSER", "CFG")

thememenu=list()

curtheme=libthemeconf.getconf("theme", "themefile")
curthemename=(libthemeconf.getthemeinfo(curtheme))[0]
curbg=int(libthemeconf.getconf("desk", "bgtheme"))
curbgname=vmui.getbgname(curbg)
for fname in os.listdir(iterate1):
	fnamelo=fname.lower()
	if fnamelo.endswith((".thm")):
		thname=(libthemeconf.getthemeinfo(fname))[0]
		thitm=vmui.menuitem(thname, fname)
		thememenu.extend([thitm])
for fname in os.listdir(iterate2):
	fnamelo=fname.lower()
	if fnamelo.endswith((".thm")):
		thname=(libthemeconf.getthemeinfo(fname))[0]
		thitm=vmui.menuitem(thname, fname)
		thememenu.extend([thitm])		

themenot="""NOTICE:
You may need to restart SBTCVM utilities
for changes to take effect!"""


fm0=vmui.menuitem("Help (F1)", "HELP")
fm1=vmui.menuitem("Save", "SAVE")
fm2=vmui.menuitem("Reset", "RESET")
fm3=vmui.menuitem("Quit", "QUIT")
filemenu=[fm0, fm1, fm2, fm3]



qflg=0
scupdate=1

stcolor=libthemeconf.desktext
while qflg==0:
	time.sleep(0.05)
	if scupdate==1:
		scupdate=0
		hudrect=pygame.Rect(0, 0, screenx, 60)
		#screensurf.blit(setbg, (0, 0))
		screensurf.fill(libthemeconf.deskcolor)
		pygame.draw.rect(screensurf, libthemeconf.hudbg, hudrect, 0)
		screensurf.blit(sbtcvmbadge, ((screenx-120), 0))
		hudy=3
		hudpad=5
		fmx=screensurf.blit(fvfilemenu, (hudy, 5))
		fmxy=hudy
		hudy += hudpad
		hudy += fvfilemenu.get_width()
		
		bgx=screensurf.blit(bgbtn, (hudy, 5))
		menulabel=catfont.render(curbgname, True, libthemeconf.btntext)
		screensurf.blit(menulabel, (hudy, 5))
		bgxy=hudy
		hudy += hudpad
		hudy += bgbtn.get_width()
		themexy=hudy
		themex=screensurf.blit(themebtn, (hudy, 5))
		menulabel=catfont.render(curthemename, True, libthemeconf.btntext)
		screensurf.blit(menulabel, (hudy, 5))
		
		
		pygame.display.update()
	for event in pygame.event.get():
		if event.type == QUIT:
			qflg=1
			break
		if event.type == KEYDOWN and event.key == K_F1:
			subprocess.Popen(["python", "helpview.py", "settings.xml"])
		if event.type == KEYDOWN and event.key == K_F8:
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-theme.png')))
			break
		if event.type==MOUSEBUTTONDOWN:
			if themex.collidepoint(event.pos)==1 and event.button==1:
				curbak=curtheme
				curtheme=vmui.menuset(thememenu, themexy, 45, reclick=0, fontsize=26)
				if curtheme==None:
					curtheme=curbak
				libthemeconf.setconf("theme", "themefile", curtheme)
				curthemename=(libthemeconf.getthemeinfo(curtheme))[0]
				scupdate=1
				
			if bgx.collidepoint(event.pos)==1 and event.button==1:
				vmui.settheme(bgxy, 45, nosave=1)
				curbg=int(libthemeconf.getconf("desk", "bgtheme"))
				curbgname=vmui.getbgname(curbg)
				scupdate=1
			if fmx.collidepoint(event.pos)==1 and event.button==1:
				menuret=vmui.menuset(filemenu, fmxy, 45, reclick=0, fontsize=26)
				if menuret=="HELP":
					subprocess.Popen(["python", "helpview.py", "theme.xml"])
				if menuret=="SAVE":
					libthemeconf.saveconf()
					vmui.okdiag(themenot, (screenx // 2), (screeny // 2))
				if menuret=="RESET":
					
					libthemeconf.resetconf()
					curtheme=libthemeconf.getconf("theme", "themefile")
					curthemename=(libthemeconf.getthemeinfo(curtheme))[0]
					curbg=int(libthemeconf.getconf("desk", "bgtheme"))
					curbgname=vmui.getbgname(curbg)
					#frameskip selector code
					print "dxreset"
					scupdate=1
				if menuret=="QUIT":
					qflg=1
					break