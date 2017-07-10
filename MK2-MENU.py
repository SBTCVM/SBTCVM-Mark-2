#!/usr/bin/env python
import time
import os
import sys
import pygame
from pygame.locals import *
#import VMSYSTEM.libSBTCVM as libSBTCVM
#import VMSYSTEM.libbaltcalc as libbaltcalc
import VMSYSTEM.libvmui as vmui


print "SBTCVM menu system v2.0.1"

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("SBTCVM Mark 2 | Menu", "SBTCVM Mark 2 | Menu")
#put SBTCVM in kiosk mode.
#this adjusts how SBTCVM works in certain cases to better mesh with the menu system.
#such as disabling the wait-on-exit feature.
GLOBKIOSK=1

#SBTCVM Mark 2
#Simple Balanced Ternary Computer Virtual Machine
#
#v2.0.1
#
#(c)2016-2017 Thomas Leathers and Contributors
#
#  SBTCVM Mark 2 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  SBTCVM Mark 2 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with SBTCVM Mark 2. If not, see <http://www.gnu.org/licenses/>

#simple text iterator. loads the refrenced text file from VMSYSTEM.
#(shows the text screens)


#SBTCVM
windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'icon64.png'))

pygame.display.set_icon(windowicon)
#screen fonts
simplefont = pygame.font.SysFont(None, 16)
simplefontA = pygame.font.SysFont(None, 20)
simplefontB = pygame.font.SysFont(None, 22)
simplefontC = pygame.font.SysFont(None, 32)
screensurf=pygame.display.set_mode((800, 600))

#initalize VMUI system
#SBTCVM_MK2.py also does this.
#libvmui is where the menu support logic and menu extras functions are located.
vmui.initui(screensurf, 1)
#
evhappenflg=0
#visual menu item names:
mainmenulst=["Get Started", "Demo Menu", "Help Menu", "Games Menu", "Extras Menu", "Quit"]
#selection codes:
mainmenucode=["GETSTART", "DEMO", "HELP", "GAMES", "EXTRAS", "QUIT"]
mainmenudesc=["Get started with SBTCVM", "A selection of various demo programs.", "Get Help", "Play some balanced ternary computer games.", "A selection of various extras.", "Quit."]
#number of menu items:
mainmenucnt=6
menudesc="Main Menu"

#demomenu
demomenulst=["Main Menu", "6-trit Color map", "Fibonacci", "Flower", "Dazzle", "Pixel Patterns", "Ray Burst"]
demomenucode=["MAIN", "COLMAP", "FIB", "FLOWER", "DEMODAZ", "DEMOPIXPAT", "DEMORAYBURST"]
demomenudesc=["Return to main menu.", "See a 6-trit color map be calculated.", "The Fibonacci Sequence.", "See an example of image conversion.", "A randomly seeded, endless rainbow box demo.", "A randomly seeded, pixel patterns demo.", "A randomly seeded, Ray 'burst' demo."]
demomenucnt=7

#getstartmenu
stmenulst=["Main Menu", "Welcome",  "Intro Program"]
stmenucode=["MAIN", "WELCOME", "STINTRO"]
stmenudesc=["Return to main menu.", "A welcome to SBTCVM.", "An introduction to SBTCVM, that runs in SBTCVM."]
stmenucnt=3

hlpmenulst=["Main Menu", "More help",  "About"]
hlpmenucode=["MAIN", "HLPOVER", "CREDIT"]
hlpmenudesc=["Return to main menu.", "How to get more help.", "About SBTCVM Mark 2."]
hlpmenucnt=3

exmenulst=["Main Menu", "Clock"]
exmenucode=["MAIN", "CLOCK"]
exmenudesc=["Return to main menu.", "A balanced ternary clock."]
exmenucnt=2

gamemenulst=["Main Menu", "Guess That Trit"]
gamemenucode=["MAIN", "GAMEGTT"]
gamemenudesc=["Return to main menu.", "a number guessing game with a gameshow theme."]
gamemenucnt=2

curmenulst=mainmenulst
curmenucnt=mainmenucnt
curmenucode=mainmenucode
curmenudesc=mainmenudesc

vmlaunchbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-LAUNCH.png')).convert_alpha()
vmbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VMBG.png')).convert()
qflg=0
menuhighnum=1
ixreturn=0
retfromexec=0
screensurf.blit(vmbg, (0, 0))
vmui.dummyreadouts()
while qflg!=1:
	if retfromexec==1:
		print "----------------"
		print "return from VM execution."
		print "----------------"
		retfromexec=0
		pygame.display.set_caption("SBTCVM Mark 2 | Menu", "SBTCVM Mark 2 | Menu")
		screensurf.blit(vmbg, (0, 0))
		vmui.dummyreadouts()
	#starting point for menu
	texhigcnt=2
	#separation between each line of text's origin
	texhigjump=22
	#menu line count variable. should be set to 1 here.
	indlcnt=1
	
	screensurf.blit(vmlaunchbg, (0, 0))
	datdict={}
	for indx in curmenulst:
		if indlcnt==menuhighnum:
			textit=simplefontB.render(indx, True, (0, 0, 0), (255, 255, 255))
		else:
			textit=simplefontB.render(indx, True, (0, 0, 0))
		gx=screensurf.blit(textit, (650, texhigcnt))
		datdict[indlcnt]=gx
		texhigcnt += texhigjump
		indlcnt += 1
		
	menulabel=simplefontC.render(menudesc, True, (0, 0, 0), (255, 255, 255))
	screensurf.blit(menulabel, (158, 4))
	itemlabel=simplefontB.render(curmenudesc[(menuhighnum - 1)], True, (0, 0, 0), (255, 255, 255))
	screensurf.blit(itemlabel, (170, 34))
	pygame.display.update()
	pygame.event.pump()
	pygame.event.clear()
	#reads keyboard controlls, moves cursers when instructed by up/down arrow keys.
	#sets ixreturn to 1 when return is pressed.
	evhappenflg=0
	while evhappenflg==0:
		time.sleep(.1)
		for event in pygame.event.get():
			texhigcnt=2
			#separation between each line of text's origin
			texhigjump=22
			#menu line count variable. should be set to 1 here.
			indlcnt=1
			pos = pygame.mouse.get_pos()
			for indx in curmenulst:
				if indlcnt==menuhighnum:
					if datdict[indlcnt].collidepoint(pos)==1:
						textit=simplefontB.render(indx, True, (0, 0, 150), (255, 255, 255))
						gx=screensurf.blit(textit, (650, texhigcnt))
					else:
						textit=simplefontB.render(indx, True, (0, 0, 0), (255, 255, 255))
						gx=screensurf.blit(textit, (650, texhigcnt))
				else:
					
					if datdict[indlcnt].collidepoint(pos)==1:
						textit=simplefontB.render(indx, True, (0, 0, 150), (129, 173, 219))
						gx=screensurf.blit(textit, (650, texhigcnt))
					else:
						textit=simplefontB.render(indx, True, (0, 0, 0), (129, 173, 219))
						gx=screensurf.blit(textit, (650, texhigcnt))
				pygame.display.update([gx])
				texhigcnt += texhigjump
				indlcnt += 1
			if event.type == KEYDOWN and event.key == K_UP:
				menuhighnum -= 1
				evhappenflg=1
				#menusound2.play()
				break
			if event.type == KEYDOWN and event.key == K_RIGHT:
				menuhighnum += 1
				evhappenflg=1
				#menusound2.play()
				break
			if event.type == KEYDOWN and event.key == K_DOWN:
				menuhighnum += 1
				evhappenflg=1
			#	menusound2.play()
				break
			if event.type == KEYDOWN and event.key == K_LEFT:
				menuhighnum -= 1
				evhappenflg=1
				#menusound2.play()
				break
			if event.type == KEYDOWN and event.key == K_RETURN:
				ixreturn=1
				evhappenflg=1
				#menusound2.play()
				break
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-MENU.png')))
				break
			if event.type == MOUSEBUTTONDOWN:
				mousexcnt=1
				for fxd in curmenulst:
					if datdict[mousexcnt].collidepoint(event.pos)==1 and event.button==1:
						menuhighnum=mousexcnt
						ixreturn=1
						evhappenflg=1
						break
					mousexcnt += 1
				break
			if event.type == QUIT:
				sys.exit()
				evhappenflg=1
				break
	#makes menus "roll over"
	if menuhighnum<=0:
		menuhighnum=curmenucnt
	elif menuhighnum>curmenucnt:
		menuhighnum=1
	#print menuhighnum
	#when a menu item is chosen (return) this section determines the action to preform based on the menuitem code for that menu item
	if ixreturn==1:
		ixreturn=0
		#launcher operations.
		if curmenucode[(menuhighnum - 1)]=="STINTRO":
			GLOBSTREG="intro.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="FIB":
			GLOBSTREG="fib.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="COLMAP":
			GLOBSTREG="colmap3.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="FLOWER":
			GLOBSTREG="flower.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="DEMODAZ":
			GLOBSTREG="dazzle.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="DEMOPIXPAT":
			GLOBSTREG="pixelpat.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="DEMORAYBURST":
			GLOBSTREG="rayburst.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="GAMEGTT":
			GLOBSTREG="gtt.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		#quit item
		if curmenucode[menuhighnum - 1]=="QUIT":
			qflg=1
		#text screens
		if curmenucode[menuhighnum - 1]=="CREDIT":
			vmui.creditsscroll()
		if curmenucode[menuhighnum - 1]=="CLOCK":
			vmui.BTCLOCKDATE()
		if curmenucode[menuhighnum - 1]=="HLPOVER":
			vmui.textsciter_main("L_HELP.TXT")
		if curmenucode[menuhighnum - 1]=="WELCOME":
			vmui.textsciter_main("L_WEL.TXT")
		#this code action id unfinished
		if curmenucode[menuhighnum - 1]=="DEMOMODE":
			#vmui.textsciter_main("L_WEL.TXT")
			GLOBSTREG="colmap3.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		#Menu Swapping items
		#this is how the menu system is able to run many menus with one instance of code.
		if curmenucode[menuhighnum - 1]=="MAIN":
			menuhighnum=1
			curmenulst=mainmenulst
			curmenucnt=mainmenucnt
			curmenucode=mainmenucode
			curmenudesc=mainmenudesc
			menudesc="Main Menu"
		elif curmenucode[menuhighnum - 1]=="DEMO":
			menuhighnum=1
			curmenulst=demomenulst
			curmenucnt=demomenucnt
			curmenucode=demomenucode
			curmenudesc=demomenudesc
			menudesc="Demo Menu"
		elif curmenucode[menuhighnum - 1]=="GETSTART":
			menuhighnum=1
			curmenulst=stmenulst
			curmenucnt=stmenucnt
			curmenucode=stmenucode
			curmenudesc=stmenudesc
			menudesc="Get Started"
		elif curmenucode[menuhighnum - 1]=="HELP":
			menuhighnum=1
			curmenulst=hlpmenulst
			curmenucnt=hlpmenucnt
			curmenucode=hlpmenucode
			curmenudesc=hlpmenudesc
			menudesc="Help Menu"
		elif curmenucode[menuhighnum - 1]=="EXTRAS":
			menuhighnum=1
			curmenulst=exmenulst
			curmenucnt=exmenucnt
			curmenucode=exmenucode
			curmenudesc=exmenudesc
			menudesc="Extras Menu"
		elif curmenucode[menuhighnum - 1]=="GAMES":
			menuhighnum=1
			curmenulst=gamemenulst
			curmenucnt=gamemenucnt
			curmenucode=gamemenucode
			curmenudesc=gamemenudesc
			menudesc="Games Menu"
	
	
	
	

