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

pygame.display.init()
pygame.font.init()
pygame.display.set_caption(("Settings"), ("Settings"))

windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'settings64.png'))
pygame.display.set_icon(windowicon)

screensurf=pygame.display.set_mode((800, 600))

#image data
setbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'settingsbg.jpg')).convert()
swon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'switchon.png')).convert()
swoff=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'switchoff.png')).convert()
csup=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'cpusuper.png')).convert()
csupsel=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'cpusupers.png')).convert()
cnorm=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'cpunorm.png')).convert()
cnormsel=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'cpunorms.png')).convert()
cfas=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'cpufast.png')).convert()
cfassel=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'cpufasts.png')).convert()
cslow=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'cpuslower.png')).convert()
cslowsel=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'cpuslowers.png')).convert()

lbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'lbtn.png')).convert()
rbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'rbtn.png')).convert()
saveicn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'save.png')).convert()
quiticn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'quit.png')).convert()
reseticn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'reset.png')).convert()
helpicn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "settings"), 'help.png')).convert()

simplefontC = pygame.font.SysFont(None, 28)
simplefontB = pygame.font.SysFont(None, 19)



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

#CPU SPEED PRESETS
#handled as strings here for sake of simplicity. 
CPUSLOW="0.001"
CPUNORM="0.0005"
CPUFAST="0.00001"
CPUSUPER="0.000005"

menulabel=simplefontC.render("Settings", True, (0, 0, 0), (255, 255, 255))
setbg.blit(menulabel, (158, 4))
menulabel=simplefontB.render("CPU Speed:", True, (0, 0, 0))
setbg.blit(menulabel, (0, 62))

#frameskip selector code
fskiplist=[0, 1, 2, 3, 4, 5, 10, 15, 20, 50, 100]
fslen=10
fspoint=0
fscnt=0

for f in fskiplist:
	if f == fskip:
		fspoint=fscnt
	fscnt += 1

#mixer rate selector code
mixlist=[8000, 11025, 22050, 44100, 48000]
mixlen=4
mixpoint=0
mixcnt=0

for f in mixlist:
	if f == mixrate:
		mixpoint=mixcnt
	mixcnt += 1

qflg=0
scupdate=1
while qflg==0:
	time.sleep(0.05)
	if scupdate==1:
		scupdate=0
		screensurf.blit(setbg, (0, 0))
		if CPUWAIT==CPUSLOW:
			CSX=screensurf.blit(cslowsel, (0, 80))
		else:
			CSX=screensurf.blit(cslow, (0, 80))
		if CPUWAIT==CPUNORM:
			CNX=screensurf.blit(cnormsel, (140, 80))
		else:
			CNX=screensurf.blit(cnorm, (140, 80))
		if CPUWAIT==CPUFAST:
			CFX=screensurf.blit(cfassel, (280, 80))
		else:
			CFX=screensurf.blit(cfas, (280, 80))
		if CPUWAIT==CPUSUPER:
			CUX=screensurf.blit(csupsel, (420, 80))
		else:
			CUX=screensurf.blit(csup, (420, 80))
		quitx=screensurf.blit(quiticn, (550, 150))
		savex=screensurf.blit(saveicn, (600, 150))
		resetx=screensurf.blit(reseticn, (650, 150))
		helpx=screensurf.blit(helpicn, (700, 150))
		menulabel=simplefontB.render(("Frame Skip: " + str(fskip)), True, (0, 0, 0))
		screensurf.blit(menulabel, (0, 120))
		fsup=screensurf.blit(rbtn, (40, 140))
		fsdown=screensurf.blit(lbtn, (0, 140))
		menulabel=simplefontB.render(("Sound Mixer Rate: " + str(mixrate)), True, (0, 0, 0))
		screensurf.blit(menulabel, (120, 120))
		mixup=screensurf.blit(rbtn, (160, 140))
		mixdown=screensurf.blit(lbtn, (120, 140))
		
		menulabel=simplefontB.render("Status Readouts.", True, (0, 0, 0))
		screensurf.blit(menulabel, (0, 180))
		if disablereadouts==0:
			disre=screensurf.blit(swon, (0, 200))
		else:
			disre=screensurf.blit(swoff, (0, 200))
		menulabel=simplefontB.render("TTY (virtual text display)", True, (0, 0, 0))
		screensurf.blit(menulabel, (250, 180))
		if ttystyle==0:
			ttyx=screensurf.blit(swon, (250, 200))
		else:
			ttyx=screensurf.blit(swoff, (250, 200))
		menulabel=simplefontB.render("Step By Step CPU debug mode.", True, (0, 0, 0))
		screensurf.blit(menulabel, (0, 230))
		if stepbystep==1:
			stepx=screensurf.blit(swon, (0, 250))
		else:
			stepx=screensurf.blit(swoff, (0, 250))
		menulabel=simplefontB.render("Log execution process.", True, (0, 0, 0))
		screensurf.blit(menulabel, (250, 230))
		if vmexeclogflg==1:
			vmex=screensurf.blit(swon, (250, 250))
		else:
			vmex=screensurf.blit(swoff, (250, 250))
		menulabel=simplefontB.render("Dump IObus on exit.", True, (0, 0, 0))
		screensurf.blit(menulabel, (0, 280))
		if logIOexit==1:
			ioex=screensurf.blit(swon, (0, 300))
		else:
			ioex=screensurf.blit(swoff, (0, 300))
		menulabel=simplefontB.render("Dump memory bus on exit.", True, (0, 0, 0))
		screensurf.blit(menulabel, (250, 280))
		if logromexit==1:
			romex=screensurf.blit(swon, (250, 300))
		else:
			romex=screensurf.blit(swoff, (250, 300))
		menulabel=simplefontB.render("Log memory bus operations", True, (0, 0, 0))
		screensurf.blit(menulabel, (0, 330))
		if tromlogging==1:
			tromx=screensurf.blit(swon, (0, 350))
		else:
			tromx=screensurf.blit(swoff, (0, 350))
		
		
		
		pygame.display.update()
	for event in pygame.event.get():
		if event.type == QUIT:
			qflg=1
			break
		if event.type == KEYDOWN and event.key == K_F1:
			subprocess.Popen(["python", "MK2-TOOLS.py", "helpview", "settings.txt"])
		if event.type == KEYDOWN and event.key == K_F8:
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-settings.png')))
			break
		if event.type==MOUSEBUTTONDOWN:
			if quitx.collidepoint(event.pos)==1 and event.button==1:
				qflg=1
				break
			if helpx.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "MK2-TOOLS.py", "helpview", "settings.txt"])
			if savex.collidepoint(event.pos)==1 and event.button==1:
				libvmconf.saveconf()
			if resetx.collidepoint(event.pos)==1 and event.button==1:
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
				fskiplist=[0, 1, 2, 3, 4, 5, 10, 15, 20, 50, 100]
				fslen=10
				fspoint=0
				fscnt=0
				for f in fskiplist:
					if f == fskip:
						fspoint=fscnt
					fscnt += 1
				#mixer rate selector code
				mixlist=[8000, 11025, 22050, 44100, 48000]
				mixlen=4
				mixpoint=0
				mixcnt=0			
				for f in mixlist:
					if f == mixrate:
						mixpoint=mixcnt
					mixcnt += 1
				scupdate=1
				print "dxreset"
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
			if CSX.collidepoint(event.pos)==1 and event.button==1:
				CPUWAIT=CPUSLOW
				libvmconf.setconf("cpu", "cpuwait", str(CPUWAIT))
				scupdate=1
			if CNX.collidepoint(event.pos)==1 and event.button==1:
				CPUWAIT=CPUNORM
				libvmconf.setconf("cpu", "cpuwait", str(CPUWAIT))
				scupdate=1
			if CFX.collidepoint(event.pos)==1 and event.button==1:
				CPUWAIT=CPUFAST
				libvmconf.setconf("cpu", "cpuwait", str(CPUWAIT))
				scupdate=1
			if  CUX.collidepoint(event.pos)==1 and event.button==1:
				CPUWAIT=CPUSUPER
				libvmconf.setconf("cpu", "cpuwait", str(CPUWAIT))
				scupdate=1
			if  fsup.collidepoint(event.pos)==1 and event.button==1:
				fspoint += 1
				if fspoint>fslen:
					fspoint=0
				fskip=fskiplist[fspoint]
				libvmconf.setconf("video", "fskip", str(fskip))
				scupdate=1
			if  fsdown.collidepoint(event.pos)==1 and event.button==1:
				fspoint -= 1
				if fspoint<0:
					fspoint=fslen
				fskip=fskiplist[fspoint]
				libvmconf.setconf("video", "fskip", str(fskip))
				scupdate=1
			if  mixup.collidepoint(event.pos)==1 and event.button==1:
				mixpoint += 1
				if mixpoint>mixlen:
					mixpoint=0
				mixrate=mixlist[mixpoint]
				libvmconf.setconf("audio", "mixrate", str(mixrate))
				scupdate=1
			if  mixdown.collidepoint(event.pos)==1 and event.button==1:
				mixpoint -= 1
				if mixpoint<0:
					mixpoint=mixlen
				mixrate=mixlist[mixpoint]
				libvmconf.setconf("audio", "mixrate", str(mixrate))
				scupdate=1