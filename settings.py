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
import VMSYSTEM.libvmconf as libvmconf
import VMSYSTEM.libvmui as vmui
import VMSYSTEM.libthemeconf as libthemeconf

pygame.display.init()
pygame.font.init()
pygame.display.set_caption(("Settings"), ("Settings"))

windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'settings64.png'))
pygame.display.set_icon(windowicon)

screensurf=pygame.display.set_mode((450, 400))
screenx=450
screeny=400
vmui.initui(screensurf, 1)
#image data
sbtcvmbadge=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'SBTCVMbadge.png')).convert()
#setbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'settingsbg2.jpg')).convert()
#swon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'switchon.png')).convert()
#swoff=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'switchoff.png')).convert()
swn=vmui.makeswitchbtn("ON", "OFF")
swon=swn[0]
swoff=swn[1]

#cpubtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'cpuspeed.png')).convert()
#mixbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'mixrate.png')).convert()
#fskipbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'frameskip.png')).convert()
#fvfilemenu=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'fvfilemenu.png')).convert()
fmicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'filemenuicon.png')).convert_alpha()
fvfilemenu=vmui.makemenubtn("FILE", icon=fmicon)
cpubtn=vmui.makemenubtn("CPU SPEED", width=80)
mixbtn=vmui.makemenubtn("MIXER RATE", width=80)
fskipbtn=vmui.makemenubtn("FRAME SKIP", width=80)

lbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'lbtn.png')).convert()
rbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'rbtn.png')).convert()
saveicn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'save.png')).convert()
quiticn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'quit.png')).convert()
reseticn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'reset.png')).convert()
helpicn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'help.png')).convert()

simplefontC = pygame.font.SysFont(None, 28)
simplefontB = pygame.font.SysFont(None, 19)
catfont = pygame.font.SysFont(None, 19)


CPUWAIT=libvmconf.getconf("cpu", "cpuwait")#
stepbystep=int(libvmconf.getconf("cpu", "stepbystep"))#

vmexeclogflg=int(libvmconf.getconf("log", "vmexec"))#
logromexit=int(libvmconf.getconf("log", "romexit"))#
logIOexit=int(libvmconf.getconf("log", "ioexit"))#
tromlogging=int(libvmconf.getconf("log", "tromlogging"))

disablereadouts=int(libvmconf.getconf("video", "disablereadouts"))#
fskip=int(libvmconf.getconf("video", "fskip"))#
ttystyle=int(libvmconf.getconf("video", "ttystyle"))#
#DEFAULTSTREG=libvmconf.getconf("bootup", "DEFAULTSTREG")
mixrate=int(libvmconf.getconf("audio", "mixrate"))#

fm0=vmui.menuitem("Help (F1)", "HELP")
fm1=vmui.menuitem("Save", "SAVE")
fm2=vmui.menuitem("Reset", "RESET")
fm3=vmui.menuitem("Quit", "QUIT")
filemenu=[fm0, fm1, fm2, fm3]


#CPU SPEED PRESETS
#handled as strings here for sake of simplicity. 
CPUSLOW="0.001"
CPUNORM="0.0005"
CPUFAST="0.00001"
CPUSUPER="0.000005"

cpu0=vmui.menuitem("Slow", "0.001")
cpu1=vmui.menuitem("Normal", "0.0005")
cpu2=vmui.menuitem("Fast", "0.00001")
cpu3=vmui.menuitem("Super", "0.000005")
cpumenu=[cpu0, cpu1, cpu2, cpu3]


#frameskip selector code
fskiplist=[0, 1, 2, 3, 4, 5, 10, 15, 20, 50, 100]
fskipmenu=list()
for f in fskiplist:
	dx=vmui.menuitem(str(f), f)
	fskipmenu.extend([dx])

#mixer rate selector code
mixlist=[8000, 11025, 22050, 44100, 48000]
mixmenu=list()
for f in mixlist:
	dx=vmui.menuitem(str(f), f)
	mixmenu.extend([dx])

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
		fmx=screensurf.blit(fvfilemenu, (3, 5))
		mixx=screensurf.blit(mixbtn, (45, 5))
		menulabel=catfont.render(str(mixrate), True, libthemeconf.btntext)
		screensurf.blit(menulabel, (45, 5))
		
		fskipx=screensurf.blit(fskipbtn, (127, 5))
		menulabel=catfont.render(str(fskip), True, libthemeconf.btntext)
		screensurf.blit(menulabel, (127, 5))
		
		cpux=screensurf.blit(cpubtn, (209, 5))
		if CPUWAIT==CPUSLOW:
			menulabel=catfont.render("Slow", True, libthemeconf.btntext)
		elif CPUWAIT==CPUNORM:
			menulabel=catfont.render("Normal", True, libthemeconf.btntext)
		elif CPUWAIT==CPUFAST:
			menulabel=catfont.render("Fast", True, libthemeconf.btntext)
		elif CPUWAIT==CPUSUPER:
			menulabel=catfont.render("Super", True, libthemeconf.btntext)
		else:
			menulabel=catfont.render("Other", True, libthemeconf.btntext)
		screensurf.blit(menulabel, (209, 5))
		
		menulabel=simplefontB.render("Status Readouts.", True, stcolor)
		screensurf.blit(menulabel, (0, 80))
		if disablereadouts==0:
			disre=screensurf.blit(swon, (0, 100))
		else:
			disre=screensurf.blit(swoff, (0, 100))
		menulabel=simplefontB.render("TTY (virtual text display)", True, stcolor)
		screensurf.blit(menulabel, (250, 80))
		if ttystyle==0:
			ttyx=screensurf.blit(swon, (250, 100))
		else:
			ttyx=screensurf.blit(swoff, (250, 100))
		menulabel=simplefontB.render("Step By Step CPU debug mode.", True, stcolor)
		screensurf.blit(menulabel, (0, 150))
		if stepbystep==1:
			stepx=screensurf.blit(swon, (0, 170))
		else:
			stepx=screensurf.blit(swoff, (0, 170))
		menulabel=simplefontB.render("Log execution process.", True, stcolor)
		screensurf.blit(menulabel, (250, 150))
		if vmexeclogflg==1:
			vmex=screensurf.blit(swon, (250, 170))
		else:
			vmex=screensurf.blit(swoff, (250, 170))
		menulabel=simplefontB.render("Dump IObus on exit.", True, stcolor)
		screensurf.blit(menulabel, (0, 220))
		if logIOexit==1:
			ioex=screensurf.blit(swon, (0, 240))
		else:
			ioex=screensurf.blit(swoff, (0, 240))
		menulabel=simplefontB.render("Dump memory bus on exit.", True, stcolor)
		screensurf.blit(menulabel, (250, 220))
		if logromexit==1:
			romex=screensurf.blit(swon, (250, 240))
		else:
			romex=screensurf.blit(swoff, (250, 240))
		menulabel=simplefontB.render("Log memory bus operations", True, stcolor)
		screensurf.blit(menulabel, (0, 290))
		if tromlogging==1:
			tromx=screensurf.blit(swon, (0, 310))
		else:
			tromx=screensurf.blit(swoff, (0, 310))
		
		
		
		pygame.display.update()
	for event in pygame.event.get():
		if event.type == QUIT:
			qflg=1
			break
		if event.type == KEYDOWN and event.key == K_F1:
			subprocess.Popen(["python", "helpview.py", "settings.xml"])
		if event.type == KEYDOWN and event.key == K_F8:
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-settings.png')))
			break
		if event.type==MOUSEBUTTONDOWN:
			if fmx.collidepoint(event.pos)==1 and event.button==1:
				menuret=vmui.menuset(filemenu, 3, 45, reclick=0, fontsize=26)
				if menuret=="HELP":
					subprocess.Popen(["python", "helpview.py", "settings.xml"])
				if menuret=="SAVE":
					libvmconf.saveconf()
				if menuret=="RESET":
					libvmconf.resetconf()
					CPUWAIT=libvmconf.getconf("cpu", "cpuwait")
					stepbystep=int(libvmconf.getconf("cpu", "stepbystep"))
					vmexeclogflg=int(libvmconf.getconf("log", "vmexec"))
					logromexit=int(libvmconf.getconf("log", "romexit"))
					logIOexit=int(libvmconf.getconf("log", "ioexit"))
					tromlogging=int(libvmconf.getconf("log", "tromlogging"))
					disablereadouts=int(libvmconf.getconf("video", "disablereadouts"))
					fskip=int(libvmconf.getconf("video", "fskip"))
					ttystyle=int(libvmconf.getconf("video", "ttystyle"))
					mixrate=int(libvmconf.getconf("audio", "mixrate"))
					#frameskip selector code
					print "dxreset"
					scupdate=1
				if menuret=="QUIT":
					qflg=1
					break
			if mixx.collidepoint(event.pos)==1 and event.button==1:
				mixratebak=mixrate
				mixrate=vmui.menuset(mixmenu, 45, 45, reclick=0, fontsize=26)
				if mixrate==None:
					mixrate=mixratebak
				libvmconf.setconf("audio", "mixrate", str(mixrate))
				scupdate=1
			if cpux.collidepoint(event.pos)==1 and event.button==1:
				cpubak=CPUWAIT
				CPUWAIT=vmui.menuset(cpumenu, 209, 45, reclick=0, fontsize=26)
				if CPUWAIT==None:
					CPUWAIT=cpubak
				libvmconf.setconf("cpu", "cpuwait", str(CPUWAIT))
				scupdate=1
			if fskipx.collidepoint(event.pos)==1 and event.button==1:
				fskipbak=fskip
				fskip=vmui.menuset(fskipmenu, 127, 45, reclick=0, fontsize=26)
				if fskip==None:
					fskip=fskipbak
				libvmconf.setconf("video", "fskip", str(fskip))
				scupdate=1
			#if quitx.collidepoint(event.pos)==1 and event.button==1:
				#qflg=1
				#break
			#if helpx.collidepoint(event.pos)==1 and event.button==1:
				#subprocess.Popen(["python", "helpview.py", "settings.xml"])
			#if savex.collidepoint(event.pos)==1 and event.button==1:
				#libvmconf.saveconf()
			#if resetx.collidepoint(event.pos)==1 and event.button==1:
				#libvmconf.resetconf()
				#CPUWAIT=libvmconf.getconf("cpu", "cpuwait")
				#stepbystep=int(libvmconf.getconf("cpu", "stepbystep"))
				#vmexeclogflg=int(libvmconf.getconf("log", "vmexec"))
				#logromexit=int(libvmconf.getconf("log", "romexit"))
				#logIOexit=int(libvmconf.getconf("log", "ioexit"))
				#tromlogging=int(libvmconf.getconf("log", "tromlogging"))
				#disablereadouts=int(libvmconf.getconf("video", "disablereadouts"))
				#fskip=int(libvmconf.getconf("video", "fskip"))
				#ttystyle=int(libvmconf.getconf("video", "ttystyle"))
				#mixrate=int(libvmconf.getconf("audio", "mixrate"))
				##frameskip selector code
				#print "dxreset"
			if disre.collidepoint(event.pos)==1 and event.button==1:
				if disablereadouts==0:
					disablereadouts=1
				else:
					disablereadouts=0
				scupdate=1
				libvmconf.setconf("video", "disablereadouts", str(disablereadouts))
			if ttyx.collidepoint(event.pos)==1 and event.button==1:
				if ttystyle==0:
					ttystyle=1
				else:
					ttystyle=0
				scupdate=1
				libvmconf.setconf("video", "ttystyle", str(ttystyle))
			if stepx.collidepoint(event.pos)==1 and event.button==1:
				if stepbystep==0:
					stepbystep=1
				else:
					stepbystep=0
				scupdate=1
				libvmconf.setconf("cpu", "stepbystep", str(stepbystep))
			if vmex.collidepoint(event.pos)==1 and event.button==1:
				if vmexeclogflg==0:
					vmexeclogflg=1
				else:
					vmexeclogflg=0
				scupdate=1
				libvmconf.setconf("log", "vmexec", str(vmexeclogflg))
			if tromx.collidepoint(event.pos)==1 and event.button==1:
				if tromlogging==0:
					tromlogging=1
				else:
					tromlogging=0
				scupdate=1
				libvmconf.setconf("log", "tromlogging", str(tromlogging))
			if romex.collidepoint(event.pos)==1 and event.button==1:
				if logromexit==0:
					logromexit=1
				else:
					logromexit=0
				scupdate=1
				libvmconf.setconf("log", "romexit", str(logromexit))
			if ioex.collidepoint(event.pos)==1 and event.button==1:
				if logIOexit==0:
					logIOexit=1
				else:
					logIOexit=0
				scupdate=1
				libvmconf.setconf("log", "ioexit", str(logIOexit))
			