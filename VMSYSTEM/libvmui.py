#!/usr/bin/env python
import time
import os
import sys
import pygame
from pygame.locals import *
import libSBTCVM
import libbaltcalc
pygame.font.init()
pygame.mixer.init()

#libvmui
#this library handles many graphical tasks, as well as containing
#functions for many tools and features found in the menus and in MK2-TOOLS
#even the VM pause menu is in here.

#fonts
simplefont = pygame.font.SysFont(None, 16)
simplefontA = pygame.font.SysFont(None, 20)
simplefontB = pygame.font.SysFont(None, 22)
simplefontC = pygame.font.SysFont(None, 32)
smldispfont = pygame.font.Font(os.path.join("VMSYSTEM", "SBTCVMreadout.ttf"), 16)
lgdispfont = pygame.font.Font(os.path.join("VMSYSTEM", "SBTCVMreadout.ttf"), 16)


#these use the same squarewave generator as SBTCVM's buzzer.
#sound A
menusound1=pygame.mixer.Sound(libSBTCVM.autosquare(300, 0.1))
#menu select sound
menusound2=pygame.mixer.Sound(libSBTCVM.autosquare(250, 0.1))
#clock widget second sound
menusound3=pygame.mixer.Sound(libSBTCVM.autosquare(280, 0.1))

#PAUSE MENU DATA
#-----
#Pause menu
#visual menu item names:
paumenulst=["Continue VM", "Quick Help", "About", "Extras Menu", "Stop VM"]
paumenulstKIOSK=["Continue VM", "Quick Help", "About", "Extras Menu", "Exit to Main Menu"]
#selection codes:
paumenucode=["CONTINUE", "QHELP", "CREDIT", "EXTRAS", "VMSTOP"]
paumenudesc=["Continue running VM", "Get Quick Help", "About SBTCVM Mark 2", "Extra stuff", "Stop VM"]
paumenudescKIOSK=["Continue running VM", "Get Quick Help", "About SBTCVM Mark 2", "Extras", "Exit to the Main Menu."]
#number of menu items:
paumenucnt=5
pmenudesc="Pause Menu"
#-----
#pause extras menu
expaumenulst=["Pause Menu", "clock"]
#selection codes:
expaumenucode=["PAUSE", "CLOCK"]
expaumenudesc=["Return To Pause Menu", "A balanced Ternary clock"]
#number of menu items:
expaumenucnt=2
expmenudesc="Pause Menu | extras"
#-----


#used by tools launcher to draw backgrounds as needed.
def toolsscreen(mode):
	if mode==1:
		screensurf.blit(vmbg, (0, 0))
		screensurf.blit(vmtoolsbg, (0, 0))
		dummyreadouts()
		menulabel=simplefontC.render("Tools and Utilities", True, (0, 0, 0), (255, 255, 255))
		screensurf.blit(menulabel, (158, 4))
	if mode==2:
		screensurf.blit(vmtoolsbgfull, (0, 0))
		menulabel=simplefontC.render("Tools and Utilities", True, (0, 0, 0), (255, 255, 255))
		screensurf.blit(menulabel, (158, 4))
	if mode==3:
		screensurf.blit(vmbg, (0, 0))
		dummyreadouts()

#used to show placeholder readouts.
def dummyreadouts():
	screensurf.blit(CPULEDSTANDBY, (749, 505))
	screensurf.blit(LEDGREENOFF, (750, 512))
	curROMtex=lgdispfont.render("A", True, (255, 0, 255), (0, 0, 0)).convert()
	screensurf.blit(curROMtex, (126, 522))
	ROMadrtex=lgdispfont.render("---------", True, (0, 127, 255), (0, 0, 0)).convert()
	screensurf.blit(ROMadrtex, (425, 564))
	reg2text=lgdispfont.render("000000000", True, (255, 127, 0), (0, 0, 0)).convert()
	screensurf.blit(reg2text, (219, 564))
	reg1text=lgdispfont.render("000000000", True, (255, 0, 127), (0, 0, 0)).convert()
	screensurf.blit(reg1text, (219, 521))
	datatext=smldispfont.render("000000000", True, (0, 255, 127), (0, 0, 0)).convert()
	screensurf.blit(datatext, (8, 566))
	insttext=smldispfont.render("000000", True, (0, 255, 255), (0, 0, 0)).convert()
	screensurf.blit(insttext, (8, 522))
	curthrtex=lgdispfont.render("--", True, (127, 0, 255), (0, 0, 0)).convert()
	screensurf.blit(curthrtex, (170, 522))

#SBTCVM pause menu.
#called upon by SBTCVM_MK2.py when Escape is pressed.
def pausemenu():
	print "------------------"
	print "SBTCVM pause menu."
	#print "------------------"
	#print KIOSKMODE
	curmenulst=paumenulst
	curmenucnt=paumenucnt
	curmenucode=paumenucode
	if KIOSKMODE==1:
		curmenudesc=paumenudescKIOSK
		curmenulst=paumenulstKIOSK
	else:
		curmenudesc=paumenudesc
		curmenulst=paumenulst
	menudesc=pmenudesc
	scbak=screensurf.copy()
	#vmlaunchbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-LAUNCH.png')).convert()
	screensurf.blit(vmlaunchbg, (0, 0))
	qflg=0
	menuhighnum=1
	ixreturn=0
	retfromexec=0
	while qflg!=1:
		#if retfromexec==1:
		#	print "----------------"
		#	print "return from VM execution."
		#	print "----------------"
		#	retfromexec=0
		#	pygame.display.set_caption("SBTCVM Mark 2 | Menu", "SBTCVM Mark 2 | Menu")
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
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					screensurf.blit(scbak, (0, 0))
					pygame.display.update()
					#print "------------------"
					print "continue VM. "
					print "------------------"
					return("c")
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-PAUSE.png')))
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
			if curmenucode[menuhighnum - 1]=="QHELP":
				textsciter_internal("L_QHELP.TXT")
			if curmenucode[menuhighnum - 1]=="CREDIT":
				creditsscroll()
			if curmenucode[menuhighnum - 1]=="CLOCK":
				BTCLOCKDATE()
			
			if curmenucode[menuhighnum - 1]=="CONTINUE":
				screensurf.blit(scbak, (0, 0))
				pygame.display.update()
				#print "------------------"
				print "continue VM. "
				print "------------------"
				return("c")
			if curmenucode[menuhighnum - 1]=="VMSTOP":
				if KIOSKMODE==0:
					screensurf.blit(scbak, (0, 0))
					pygame.display.update()
				#print "------------------"
				print "stop VM. "
				print "------------------"
				return("s")
			if curmenucode[menuhighnum - 1]=="EXTRAS":
				menuhighnum=1
				curmenulst=expaumenulst
				curmenucnt=expaumenucnt
				curmenucode=expaumenucode
				curmenudesc=expaumenudesc
				menudesc=expmenudesc
			elif curmenucode[menuhighnum - 1]=="PAUSE":
				menuhighnum=1
				curmenulst=paumenulst
				curmenucnt=paumenucnt
				curmenucode=paumenucode
				if KIOSKMODE==1:
					curmenudesc=paumenudescKIOSK
					curmenulst=paumenulstKIOSK
				else:
					curmenudesc=paumenudesc
					curmenulst=paumenulst
				menudesc=pmenudesc
			
			


#Initalize (must be called prior to all other functions)
def initui(scsurf, kiomode):
	global screensurf
	screensurf=scsurf
	global vmlaunchbg
	global KIOSKMODE
	global GNDlamp
	global POSlamp
	global NEGlamp
	global CPULEDSTANDBY
	global LEDGREENOFF
	global GFXLOGO
	global CREDITHBAR
	global vmtoolsbg
	global vmtoolsbgfull
	global vmbg
	KIOSKMODE=kiomode
	vmtoolsbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-TOOLS.png')).convert_alpha()
	vmtoolsbgfull=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-TOOLS_FULL.png')).convert()
	vmbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VMBG.png')).convert()
	vmlaunchbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-PAUSEMASK.png')).convert_alpha()
	GNDlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampGND.png')).convert()
	POSlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampPOS.png')).convert()
	NEGlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampNEG.png')).convert()
	GFXLOGO=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'GFXLOGO.png')).convert()
	CREDITHBAR=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'CREDITHBAR.png')).convert()
	#indicator lamps
	#GREEN
	#LEDGREENON=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-GREEN.png')).convert()
	LEDGREENOFF=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-GREEN-OFF.png')).convert()
	#CPU
	#CPULEDACT=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-BLUE.png')).convert()
	CPULEDSTANDBY=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-ORANGE.png')).convert()

	

#used by pausemenu function.
def textsciter_internal(flookup):
	abt = open(os.path.join("VMSYSTEM", flookup))
	pixcnt1=96
	pixjmp=16
	
	for fnx in abt:
		fnx=fnx.replace('\n', '')
		abttextB=simplefontA.render(fnx, True, (255, 255, 255))
		screensurf.blit(abttextB, (9, pixcnt1))
		pixcnt1 += pixjmp
	pixcnt1 += pixjmp
	fnx="Press any key to continue"
	abttextB=simplefontB.render(fnx, True, (0, 0, 0), (255, 255, 255))
	screensurf.blit(abttextB, (9, pixcnt1))
	pygame.display.update()
	evhappenflg2=0
	while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-PAUSE.png')))
					break
				elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
					evhappenflg2=1
					#menusound2.play()
					break

def textsciter(flookup):
	global screensurf
	scbak=screensurf.copy()
	screensurf.blit(vmlaunchbg, (0, 0))
	abt = open(os.path.join("VMSYSTEM", flookup))
	pixcnt1=96
	pixjmp=16
	
	for fnx in abt:
		fnx=fnx.replace('\n', '')
		abttextB=simplefontA.render(fnx, True, (255, 255, 255), (0, 0, 127))
		screensurf.blit(abttextB, (9, pixcnt1))
		pixcnt1 += pixjmp
	pixcnt1 += pixjmp
	fnx="Press any key to continue"
	abttextB=simplefontB.render(fnx, True, (0, 0, 0), (255, 255, 255))
	screensurf.blit(abttextB, (9, pixcnt1))
	pygame.display.update()
	evhappenflg2=0
	while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-OTHER.png')))
					break
				elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
					evhappenflg2=1
					#menusound2.play()
					break
	screensurf.blit(scbak, (0, 0))
	pygame.display.update()

def textsciter_main(flookup):
	abt = open(os.path.join("VMSYSTEM", flookup))
	pixcnt1=96
	pixjmp=16
	
	for fnx in abt:
		fnx=fnx.replace('\n', '')
		abttextB=simplefontA.render(fnx, True, (0, 0, 0))
		screensurf.blit(abttextB, (9, pixcnt1))
		pixcnt1 += pixjmp
	pixcnt1 += pixjmp
	fnx="Press any key to continue"
	abttextB=simplefontB.render(fnx, True, (0, 0, 0), (255, 255, 255))
	screensurf.blit(abttextB, (9, pixcnt1))
	pygame.display.update()
	evhappenflg2=0
	while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-MENU.png')))
					break
				elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
					evhappenflg2=1
					#menusound2.play()
					break

#Balanced ternary clock function. (shows clock that is in the extras menu.
def BTCLOCKDATE():
	
	loopend=0
	hourY=227
	minY=227
	secY=227
	ttextY=204
	helplab = simplefontB.render(('''Red=-, violet=0 blue=+'''), True, (255, 255, 255))
	screensurf.blit(helplab, (3, 120))
	prevtime=None
	#quick fix to solve drawing glitches
	scbak=screensurf.copy()
	while loopend==0:
		
		#screensurf.fill((127, 127, 127))
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-MENU.png')))
				break
			elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
				loopend=1
			if event.type == QUIT:
				loopend=1
		screensurf.blit(scbak, (0, 0))
		pygame.event.clear()
		curtim=time.localtime()
		hourdec=curtim[3]
		mindec=curtim[4]
		secdec=curtim[5]
		if prevtime!=secdec:
			menusound3.play()
		prevtime=secdec
		hourbt=libSBTCVM.trunkto4(libbaltcalc.DECTOBT(hourdec))
		minbt=libSBTCVM.trunkto5(libbaltcalc.DECTOBT(mindec))
		secbt=libSBTCVM.trunkto5(libbaltcalc.DECTOBT(secdec))
		hourX=3
		hourtext = simplefont.render(("Hr. " + str(hourdec) + ""), True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(hourtext, (hourX, ttextY))
		for fxg in hourbt:
			if fxg=="0":
				screensurf.blit(GNDlamp, (hourX, hourY))
			if fxg=="+":
				screensurf.blit(POSlamp, (hourX, hourY))
			if fxg=="-":
				screensurf.blit(NEGlamp, (hourX, hourY))
			hourX += 9
		minX=(hourX + 9)
		mintext = simplefont.render(("Min. " + str(mindec) + ""), True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(mintext, (minX, ttextY))
		for fxg in minbt:
			if fxg=="0":
				screensurf.blit(GNDlamp, (minX, minY))
			if fxg=="+":
				screensurf.blit(POSlamp, (minX, minY))
			if fxg=="-":
				screensurf.blit(NEGlamp, (minX, minY))
			minX += 9
		secX=(minX + 9)
		sectext = simplefont.render(("Sec. " + str(secdec) + ""), True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(sectext, (secX, ttextY))
		for fxg in secbt:
			if fxg=="0":
				screensurf.blit(GNDlamp, (secX, secY))
			if fxg=="+":
				screensurf.blit(POSlamp, (secX, secY))
			if fxg=="-":
				screensurf.blit(NEGlamp, (secX, secY))
			secX += 9
		pygame.display.update()

def creditsscroll():
	pixcnt1=0
	pixjmp=14
	scrollsurfwid=24
	
	texttable=["","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
	GFXLOGOCRED=GFXLOGO.copy()
	while True:
		abt = open(os.path.join("VMSYSTEM", "L_CREDIT.TXT"))
		for flid in abt:
			flid=flid.replace('\n', '')
			texttable.pop(0)
			texttable.append(flid)
			scrollsurfyaw=-20
			scrollmaskyaw=65
			slidecnt=0
			pixcnt1=0
			scrollsurf=pygame.Surface((600, 410))
			scrollmask=pygame.Surface((600, 370))
			scrollsurf.fill((255, 255, 255))
			for qlid in texttable:
				if qlid=="-<GFXLOGO>-":
					abttextbox=GFXLOGOCRED.get_rect()
					abttextbox.centerx=scrollsurf.get_rect().centerx
					abttextbox.y=pixcnt1
					scrollsurf.blit(GFXLOGOCRED, abttextbox)
				elif qlid=="-<HBAR>-":
					abttextbox=CREDITHBAR.get_rect()
					abttextbox.centerx=scrollsurf.get_rect().centerx
					abttextbox.y=pixcnt1
					scrollsurf.blit(CREDITHBAR, abttextbox)
				elif qlid!="":
					abttext=simplefont.render(qlid, True, (0,0,0), (255, 255, 255))
					abttextbox=abttext.get_rect()
					abttextbox.centerx=scrollsurf.get_rect().centerx
					abttextbox.y=pixcnt1
					scrollsurf.blit(abttext, abttextbox)
				pixcnt1 += pixjmp
			while slidecnt!=14:
				scrollmask.blit(scrollsurf, (0, scrollsurfyaw))
				screensurf.blit(scrollmask, (scrollsurfwid, scrollmaskyaw))
				scrollsurfyaw -= 1
				slidecnt += 1
				time.sleep(.05)
				pygame.display.update()
			scrollmask.blit(scrollsurf, (0, scrollsurfyaw))
			screensurf.blit(scrollmask, (scrollsurfwid, scrollmaskyaw))
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-MENU.png')))
				elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
					return()



