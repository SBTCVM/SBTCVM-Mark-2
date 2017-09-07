#!/usr/bin/env python
import time
import os
import sys
import pygame
from pygame.locals import *
#import libSBTCVM
#import libbaltcalc
import subprocess
pygame.font.init()
#pygame.mixer.init()

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
#menusound1=pygame.mixer.Sound(libSBTCVM.autosquare(300, 0.1))
#menu select sound
#menusound2=pygame.mixer.Sound(libSBTCVM.autosquare(250, 0.1))
#clock widget second sound
#menusound3=pygame.mixer.Sound(libSBTCVM.autosquare(280, 0.1))

#PAUSE MENU DATA
#-----
#Pause menu
#visual menu item names:
paumenulst=["Continue VM", "VM Help", "About", "Extras Menu", "Stop VM"]
paumenulstKIOSK=["Continue VM", "VM Help", "About", "Extras Menu", "Stop VM"]
#selection codes:
paumenucode=["CONTINUE", "QHELP", "CREDIT", "EXTRAS", "VMSTOP"]
paumenudesc=["Continue running VM", "Get Help On SBTCVM's VM", "About SBTCVM Mark 2", "Extra stuff", "Stop VM"]
paumenudescKIOSK=["Continue running VM", "Get Help On SBTCVM's VM", "About SBTCVM Mark 2", "Extras", "Stop VM"]
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
	if mode==4:
		screensurf.blit(vmbg, (0, 0))
		screensurf.blit(vmlaunchbg, (0, 0))
		dummyreadouts()
		menulabel=simplefontC.render("Credits", True, (0, 0, 0), (255, 255, 255))
		screensurf.blit(menulabel, (158, 4))
	if mode==5:
		screensurf.blit(vmbg, (0, 0))
		screensurf.blit(vmlaunchbg, (0, 0))
		dummyreadouts()
		menulabel=simplefontC.render("Help", True, (0, 0, 0), (255, 255, 255))
		screensurf.blit(menulabel, (158, 4))

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
	global screensurf
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
				subprocess.Popen(["python", "helpview.py", "vmhelp.xml"])
			if curmenucode[menuhighnum - 1]=="CREDIT":
				creditsscroll()
			if curmenucode[menuhighnum - 1]=="CLOCK":
				#BTCLOCKDATE()
				import VMSYSTEM.libbttools as bttool
				bttool.initui(screensurf, 1)
				bttool.BTCLOCKDATE()
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
	#global GNDlamp
	#global POSlamp
	#global NEGlamp
	global CPULEDSTANDBY
	global LEDGREENOFF
	global GFXLOGO
	global CREDITHBAR
	global vmtoolsbg
	global vmtoolsbgfull
	global vmbg
	global sbtccat
	global diagbtnok
	global diagbtnyes
	global diagbtnno
	KIOSKMODE=kiomode
	vmtoolsbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-TOOLS.png')).convert_alpha()
	vmtoolsbgfull=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-TOOLS_FULL.png')).convert()
	vmbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VMBG.png')).convert()
	vmlaunchbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-PAUSEMASK.png')).convert_alpha()
	#GNDlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampGND.png')).convert()
	#POSlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampPOS.png')).convert()
	#NEGlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampNEG.png')).convert()
	GFXLOGO=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'GFXLOGO-CAT.png')).convert()
	CREDITHBAR=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'CREDITHBAR.png')).convert()
	#indicator lamps
	#GREEN
	#LEDGREENON=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-GREEN.png')).convert()
	LEDGREENOFF=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-GREEN-OFF.png')).convert()
	#CPU
	#CPULEDACT=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-BLUE.png')).convert()
	CPULEDSTANDBY=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-ORANGE.png')).convert()
	sbtccat=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'SBTCCAT34.png')).convert()
	
	diagbtnok=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'diagbtnok.png')).convert()
	diagbtnyes=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'diagbtnyes.png')).convert()
	diagbtnno=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'diagbtnno.png')).convert()

	

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

#basic context help screen. called by programs through MK2-TOOLS.py
def helpscreen(flookup):
	abt = open(flookup)
	pixcnt1=70
	pixjmp=16
	
	for fnx in abt:
		fnx=fnx.replace('\n', '')
		abttextB=simplefontB.render(fnx, True, (255, 255, 255))
		screensurf.blit(abttextB, (9, pixcnt1))
		pixcnt1 += pixjmp
	pixcnt1 += pixjmp
	fnx="Press enter or click to close"
	abttextB=simplefontB.render(fnx, True, (0, 0, 0), (255, 255, 255))
	screensurf.blit(abttextB, (9, pixcnt1))
	pygame.display.update()
	evhappenflg2=0
	while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-helpview.png')))
					break
				elif event.type == KEYDOWN and event.key == K_RETURN:
					evhappenflg2=1
					break
				elif event.type == MOUSEBUTTONDOWN and event.button==1:
					evhappenflg2=1
					break
				elif event.type == QUIT:
					evhappenflg2=1
					break

#textinput can be used to input text graphically.
#use the acceptchars argument to specify a string of permitted chars. ex "abc" would only allow a, b, and c
#specify textstring to have the input prepopulated with an existing string.
#i.e. the user's previous input or a default input.
#the textcol, bgcol, and fontsize do what one may expect.
#set bgcol to None for transparent text background.
#upon mousebutton 1 press down event, it should return, and have placed said event back into pygame event queue

#support functions for text input.
#used to remove characters at the curoffset when backspace is pressed
def charremove(string, indexq):
	if indexq==0:
		return string
	else:
		return (string[:(indexq-1)] + string[(indexq):])
#used to add characters at the curoffset, and place the "curser" (in reality a vertical bar) in the correct place.
def charinsert(string, char, indexq):
	if indexq==0:
		return char + string
	else:
		return (string[:(indexq-1)] + char + string[(indexq-1):])

def textinput(xpos, ypos, textcol=(0, 0, 0), bgcol=(255, 255, 255),  fontsize=20, textstring="", acceptchars=""):
	global screensurf
	scbak=screensurf.copy()
	textfnt = pygame.font.SysFont(None, fontsize)
	curstatus=1
	curcnt=0
	#number of loops between changing cursor blink state.
	curpoint=20
	redraw=1
	curoffset=len(textstring)
	pygame.key.set_repeat(250, 50)
	while True:
		time.sleep(.03)
		screensurf.blit(scbak, (0, 0))
		#cursor blinking counter
		if curcnt<curpoint:
			curcnt += 1
		else:
			curcnt=0
			if curstatus==1:
				curstatus=0
				redraw=1
			else:
				curstatus=1
				redraw=1
		#drawing operations
		if redraw==1:
			redraw=0
			#add in cursor
			if curstatus==1:
				textstringD=charinsert(textstring, "|", (curoffset + 1))
			else:
				textstringD=charinsert(textstring, " ", (curoffset + 1))
			#draw text
			if bgcol!=None:
				abttextB=textfnt.render(textstringD, True, textcol, bgcol)
			else:
				abttextB=textfnt.render(textstringD, True, textcol)
			screensurf.blit(abttextB, (xpos, ypos))
			pygame.display.update()
		#event processor
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-vmuiinput1.png')))
				break
			elif event.type == KEYDOWN and event.key == K_RETURN:
				return textstring
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return textstring
			#home/end support.
			elif event.type == KEYDOWN and event.key == K_HOME:
				if curoffset!=0:
					curoffset=0
					redraw=1
			elif event.type == KEYDOWN and event.key == K_END:
				if curoffset!=len(textstring):
					curoffset=len(textstring)
					redraw=1
			#cursor movement
			elif event.type == KEYDOWN and event.key == K_LEFT:
				if curoffset!=0:
					curoffset -= 1
					redraw=1
			elif event.type == KEYDOWN and event.key == K_RIGHT:
				if curoffset!=len(textstring):
					curoffset += 1
					redraw=1
			#backspace code (also see charremove function)
			elif event.type == KEYDOWN and event.key == K_BACKSPACE:
				if len(textstring)!=0 and curoffset!=0:
					textstring=charremove(textstring, curoffset)
					curoffset -= 1
					redraw=1
				break
			#character input processing (also see charinsert function)
			elif event.type == KEYDOWN and event.key != K_TAB:
				if str(event.unicode) in acceptchars or len(acceptchars)==0:
					curoffset += 1
					textstring=charinsert(textstring, str(event.unicode), curoffset)
					redraw=1
				break
			elif event.type == MOUSEBUTTONDOWN and event.button==1:
				#Place event back into queue, so the calling program can use it.
				#this should let the program act more seamless.
				pygame.event.clear()
				pygame.event.post(event)
				return textstring
			elif event.type == QUIT:
				return textstring
#menuitem class used to make menu item entries for menuset
#label=item label
#retstring=string or other item returned when clicked.
#noclick= wether to make item clickable
#icon= pygame surface to be used as an icon. (note: no resizing of icon preformed)
class menuitem:
	def __init__(self, label, retstring, noclick=0, icon=None, box=None, labelsurf=None):
		self.label=label
		self.retstring=retstring
		self.icon=icon
		self.box=box
		self.labelsurf=labelsurf
		self.noclick=noclick

#menu system.
#draws menu at xpos, ypos
#uses menuitem instances in menulist to create menu.
#reclick controls wether to repost a click outside the menu area:
# -reclick=1 returns and reposts upon click outside menu (default
# -reclick=0 just returns upon click outside menu
# -reclick=2 ignores click outside menu
# (menuset will return None upon returning due to click outside menu)
def menuset(menulist, xpos, ypos, reclick=1, textcol=(0, 0, 0), unavcol=(100, 100, 100), linecol=(120, 120, 120), bgcol=(255, 255, 255),  fontsize=20):
	global screensurf
	scbak=screensurf.copy()
	textfnt = pygame.font.SysFont(None, fontsize)
	yjump=fontsize
	#menuh=(len(menulist) * yjump)
	menuw=0
	menuh=0
	for item in menulist:
		if item.icon==None:
			itemsize=(textfnt.size(item.label)[0])
			if itemsize>menuw:
				menuw=itemsize
			menuh += yjump
		else:
			iconwidth=(item.icon).get_width()
			iconheight=((item.icon).get_height() + 4)
			itemsize=(textfnt.size(item.label)[0] + iconwidth + 2)
			if itemsize>menuw:
				menuw=itemsize
			if iconheight>yjump:
				menuh += iconheight
			else:
				menuh += yjump
			
	menuw += 4
	menubox=pygame.Surface((menuw, menuh))
	dropshadow=pygame.Surface((menuw, menuh))
	menushad=dropshadow.get_rect()
	menushad.x = (4 + xpos)
	menushad.y = (4 + ypos)
	dropshadow.set_alpha(80)
	dropshadow.fill((0, 0, 0))
	screensurf.blit(dropshadow, menushad)
	#pygame.draw.rect(screensurf, (0, 0, 0, 50), menushad, 0)
	#itembox=pygame.Surface((menuw, yjump))
	menubox.fill(bgcol)
	menugx=screensurf.blit(menubox, (xpos, ypos))
	pygame.draw.rect(screensurf, linecol, menugx, 1)
	menuy=ypos
	menux=xpos + 2
	for item in menulist:
		if item.labelsurf==None:
			if item.noclick==0:
				itemtext=textfnt.render(item.label, True, textcol)
				item.labelsurf=itemtext
			else:
				itemtext=textfnt.render(item.label, True, unavcol)
				item.labelsurf=itemtext
		else:
			itemtext=item.labelsurf
		if item.icon==None:
			screensurf.blit(itemtext, (menux, menuy))
			gx=Rect(xpos, menuy, menuw, yjump)
			menuy += yjump
		elif (item.icon).get_height()>yjump:
			screensurf.blit(item.icon, (menux, (menuy + 2)))
			screensurf.blit(itemtext, ((menux + 2 + (item.icon).get_width()), menuy))
			gx=Rect(xpos, menuy, menuw, (item.icon).get_height())
			menuy += ((item.icon).get_height() + 2)
		else:
			screensurf.blit(item.icon, (menux, (menuy + 2)))
			screensurf.blit(itemtext, ((menux + 2 + (item.icon).get_width()), menuy))
			gx=Rect(xpos, menuy, menuw, yjump)
			menuy += yjump
		#pygame.draw.rect(screensurf, (255, 0, 0), gx, 1)
		
		
		item.box=gx
		pygame.draw.line(screensurf, linecol, ((0 + xpos), menuy), ((menuw + xpos - 1), menuy))
	pygame.display.update()
	while True:
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-vmuimenuset.png')))
			if event.type == MOUSEBUTTONDOWN and event.button==1:
				clickblock=0
				
				for item in menulist:
					#print "ERG"
					if (item.box).collidepoint(event.pos):
						#print "ORG"
						if item.noclick==0:
							#print "ARG"
							screensurf.blit(scbak, (0, 0))
							pygame.display.update()
							return item.retstring
						else:
							clickblock=1
				if clickblock==0 and reclick!=2:
					if reclick==1:
						pygame.event.clear()
						pygame.event.post(event)
					screensurf.blit(scbak, (0, 0))
					pygame.display.update()
					return None
		
#returns list of lines contained in textstring)
def listline(textstring):
	textcont=(textstring + "\n")
	textchunk=""
	chunklist=list()
	for texch in textcont:
		if texch=="\n":
			chunklist.extend([textchunk])
			textchunk=""
		else:
			textchunk=(textchunk + texch)
	return chunklist

#textstring is a body of text, (can be multiple lines) that will show in the dialog
#okdiag will return "OK" upon user clicking the "OK" button.
#reclick controls wether to repost a click outside the dialog area:
# -reclick=1 returns and reposts upon click outside dialog
# -reclick=0 just returns upon click outside dialog
# -reclick=2 ignores click outside dialog (default)
# (okdiag will return None upon returning due to click outside dialog)
#
#SPECIAL NOTE ABOUT DIALOGS: they will CENTER on xpos, ypos!
def okdiag(textstring, xpos, ypos, reclick=2, textcol=(0, 0, 0), linecol=(120, 120, 120), bgcol=(255, 255, 255),  fontsize=20):
	global screensurf
	scbak=screensurf.copy()
	btnw=100
	btnh=30
	textfnt = pygame.font.SysFont(None, fontsize)
	yjump=fontsize
	textlist=listline(textstring)
	textbodyh=(len(textlist)*yjump)
	ypad=5
	xpad=5
	textbtnpad=10
	dialogh=(textbodyh + ypad + ypad + btnh + textbtnpad)
	textwidest=0
	minwid=(btnw)
	for item in textlist:
		itemsize=textfnt.size(item)[0]
		if itemsize>textwidest:
			textwidest=itemsize
	if textwidest<minwid:
		textwidest=minwid
	dialogw=(textwidest + xpad + xpad)
	xpos -= (dialogw // 2)
	ypos -= (dialogh // 2)
	menubox=pygame.Surface((dialogw, dialogh))
	menubox.fill(bgcol)
	dropshadow=pygame.Surface((dialogw, dialogh))
	menushad=dropshadow.get_rect()
	menushad.x = (4 + xpos)
	menushad.y = (4 + ypos)
	dropshadow.set_alpha(80)
	dropshadow.fill((0, 0, 0))
	screensurf.blit(dropshadow, menushad)
	menugx=screensurf.blit(menubox, (xpos, ypos))
	pygame.draw.rect(screensurf, linecol, menugx, 1)
	texty=(ypos+ypad)
	for item in textlist:
		itemtext=textfnt.render(item, True, textcol)
		#itemxpos=((xpos + xpad)  (itemtext.get_width() // 2))
		itembox=itemtext.get_rect()
		itembox.centerx=menugx.centerx
		itembox.y=texty
		screensurf.blit(itemtext, itembox)
		texty += yjump
	btny=(texty + textbtnpad)
	btnx1=((dialogw // 2)-(btnw // 2) + xpos)
	btnokx=screensurf.blit(diagbtnok, (btnx1, btny))
	pygame.display.update()
	while True:
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-vmuiokdialog.png')))
			if event.type == MOUSEBUTTONDOWN and event.button==1:
				if menugx.collidepoint(event.pos):
					if btnokx.collidepoint(event.pos):
						screensurf.blit(scbak, (0, 0))
						pygame.display.update()
						return "OK"
				elif reclick!=2:
					if reclick==1:
						pygame.event.clear()
						pygame.event.post(event)
					return None
					
#textstring is a body of text, (can be multiple lines) that will show in the dialog
#okdiag will return "YES" upon user clicking the "Yes" button.
#okdiag will return "NO" upon user clicking the "No" button.
#reclick controls wether to repost a click outside the dialog area:
# -reclick=1 returns and reposts upon click outside dialog
# -reclick=0 just returns upon click outside dialog
# -reclick=2 ignores click outside dialog (default)
# (okdiag will return None upon returning due to click outside dialog)
#
#SPECIAL NOTE ABOUT DIALOGS: they will CENTER on xpos, ypos!
def yndiag(textstring, xpos, ypos, reclick=2, textcol=(0, 0, 0), linecol=(120, 120, 120), bgcol=(255, 255, 255),  fontsize=20):
	global screensurf
	scbak=screensurf.copy()
	btnw=100
	btnh=30
	textfnt = pygame.font.SysFont(None, fontsize)
	yjump=fontsize
	textlist=listline(textstring)
	textbodyh=(len(textlist)*yjump)
	ypad=5
	xpad=5
	btnsep=20
	btnoffset=(btnw+btnsep)
	textbtnpad=10
	dialogh=(textbodyh + ypad + ypad + btnh + textbtnpad)
	textwidest=0
	minwid=(btnw + btnw + btnsep)
	for item in textlist:
		itemsize=textfnt.size(item)[0]
		if itemsize>textwidest:
			textwidest=itemsize
	if textwidest<minwid:
		textwidest=minwid
	dialogw=(textwidest + xpad + xpad)
	xpos -= (dialogw // 2)
	ypos -= (dialogh // 2)
	menubox=pygame.Surface((dialogw, dialogh))
	menubox.fill(bgcol)
	dropshadow=pygame.Surface((dialogw, dialogh))
	menushad=dropshadow.get_rect()
	menushad.x = (4 + xpos)
	menushad.y = (4 + ypos)
	dropshadow.set_alpha(80)
	dropshadow.fill((0, 0, 0))
	screensurf.blit(dropshadow, menushad)
	menugx=screensurf.blit(menubox, (xpos, ypos))
	pygame.draw.rect(screensurf, linecol, menugx, 1)
	texty=(ypos+ypad)
	for item in textlist:
		itemtext=textfnt.render(item, True, textcol)
		#itemxpos=((xpos + xpad)  (itemtext.get_width() // 2))
		itembox=itemtext.get_rect()
		itembox.centerx=menugx.centerx
		itembox.y=texty
		screensurf.blit(itemtext, itembox)
		texty += yjump
	btny=(texty + textbtnpad)
	btnx1=((dialogw // 2)-(btnw // 2) + xpos - (btnoffset // 2))
	btnx2=((dialogw // 2)-(btnw // 2) + xpos + (btnoffset // 2))
	btnyesx=screensurf.blit(diagbtnyes, (btnx1, btny))
	btnnox=screensurf.blit(diagbtnno, (btnx2, btny))
	pygame.display.update()
	while True:
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-vmuiyndialog.png')))
			if event.type == MOUSEBUTTONDOWN and event.button==1:
				if menugx.collidepoint(event.pos):
					if btnyesx.collidepoint(event.pos):
						screensurf.blit(scbak, (0, 0))
						pygame.display.update()
						return "YES"
					if btnnox.collidepoint(event.pos):
						screensurf.blit(scbak, (0, 0))
						pygame.display.update()
						return "NO"
				elif reclick!=2:
					if reclick==1:
						pygame.event.clear()
						pygame.event.post(event)
					return None


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

#


#text viewer

def textview(textfile):
	global screensurf
	pygame.display.set_caption(("textview - " + textfile), ("textview - " + textfile))
	simplefontmono = pygame.font.SysFont("monospace", 15, bold=True)
	textoff=0
	yjump=22
	yoff=0
	textx=0
	fontsize=15
	ptexty=1
	redraw=0
	qflg=0
	#get screen width and height
	screenw=screensurf.get_width()
	screenh=screensurf.get_height()
	#resizeflg is set to 1 upon a window resize event.
	resizeflg=0
	
	#open file
	abt = open(textfile)
	#set key repeat.
	pygame.key.set_repeat(250, 50)
	while qflg==0:
		#set texty to yoff offset
		texty=yoff
		time.sleep(0.05)
		#resize operations
		if resizeflg==1:
			resizeflg=2	
		elif resizeflg==2:
			screensurf=pygame.display.set_mode((resw, resh), pygame.RESIZABLE)
			redraw=1
			resizeflg=0	
			screenh=resh
			screenw=resw
		#only redraw when needed.
		if texty!=ptexty or redraw==1:
			ptexty=texty
			if redraw==1:
				redraw=0
			#seek 0
			abt.seek(0)
			#fill screen
			screensurf.fill((255, 255, 255))
			#text iterator
			for f in abt:
				if (texty+yjump)>0:
					abttext=simplefontmono.render(f.replace("\n", ""), True, (0,0,0), (255, 255, 255))
					screensurf.blit(abttext, (textx, texty))
				texty += yjump
				if texty>screenh:
					break
			pygame.display.update()
			#store a copy of texty for use in scrolling handling.
			qtexty=texty
		for event in pygame.event.get():
			if event.type == QUIT:
				qflg=1
				break
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-textview.png')))
				break
			if event.type == KEYDOWN and event.key == K_DOWN:
				if qtexty>(yjump + yjump):
					yoff -= yjump
			if event.type == KEYDOWN and event.key == K_UP:
				yoff += yjump
				if yoff>0:
					yoff=0
			if event.type == KEYDOWN and event.key == K_PAGEUP:
				yoff += (yjump * 20)
				if yoff>0:
					yoff=0
			if event.type == KEYDOWN and event.key == K_PAGEDOWN:
				if qtexty>(yjump + yjump):
					yoff -= (yjump * 20)
				#if qtexty<0:
				#	yoff=0
			if event.type == KEYDOWN and event.key == K_LEFT:
				textx += yjump
				redraw=1
			if event.type == KEYDOWN and event.key == K_RIGHT:
				textx -= yjump
				redraw=1
			if event.type == KEYDOWN and event.key == K_F1:
				subprocess.Popen(["python", "helpview.py", "textview.xml"])
			if event.type == KEYDOWN and (event.key == K_PLUS or event.key == K_EQUALS or event.key == K_KP_PLUS):
				yjump += 1
				fontsize += 1
				simplefontmono = pygame.font.SysFont("monospace", fontsize, bold=True)
				redraw=1
			if event.type == KEYDOWN and (event.key == K_MINUS or event.key == K_KP_MINUS):
				yjump -= 1
				fontsize -= 1
				if yjump<=0:
					yjump=1
				if fontsize<=0:
					fontsize=1
				simplefontmono = pygame.font.SysFont("monospace", fontsize, bold=True)
				redraw=1
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				qflg=1
				break
			if event.type == KEYDOWN and event.key == K_SPACE:
				yoff=0
				textx=0
				redraw=1
			if event.type==MOUSEBUTTONDOWN:
				if event.button==5:
					if qtexty>(yjump + yjump):
						yoff -= yjump
				if event.button==4:
					yoff += yjump
					if yoff>0:
						yoff=0
				if event.button==3:
					yoff=0
					textx=0
					redraw=1
			if event.type==VIDEORESIZE:
				resizeflg=1
				resw=event.w
				resh=event.h
				time.sleep(0.1)
				break
				
#code viewer

def codeview(textfile):
	global screensurf
	pygame.display.set_caption(("codeview - " + textfile), ("codeview - " + textfile))
	simplefontmono = pygame.font.SysFont("monospace", 15, bold=True)
	textoff=0
	yjump=22
	yoff=0
	textx=0
	fontsize=15
	ptexty=1
	redraw=0
	qflg=0
	if (textfile.lower()).endswith(".tasm"):
		tasmflg=1
	else:
		tasmflg=0
	screenw=screensurf.get_width()
	screenh=screensurf.get_height()
	resizeflg=0
	abt = open(textfile)
	pygame.key.set_repeat(250, 50)
	while qflg==0:
		texty=yoff
		time.sleep(0.05)
		if resizeflg==1:
			resizeflg=2	
		elif resizeflg==2:
			screensurf=pygame.display.set_mode((resw, resh), pygame.RESIZABLE)
			redraw=1
			resizeflg=0	
			screenh=resh
			screenw=resw
		if texty!=ptexty or redraw==1:
			ptexty=texty
			if redraw==1:
				redraw=0
			abt.seek(0)
			screensurf.fill((255, 255, 255))
			linecnt=1
			textblk=0
			for f in abt:
				
				if f.startswith("textstop"):
					textblk=0
				if (texty+yjump)>0:
					if tasmflg==1:
						if textblk==1:
							
							abttext=simplefontmono.render(("{:<5}".format(str(linecnt)) + " " + f.replace("\n", "")), True, (0,0,150), (230, 230, 230))
						else:
							if f.startswith("#"):
								abttext=simplefontmono.render(("{:<5}".format(str(linecnt)) + " " + f.replace("\n", "")), True, (150,0,0), (230, 230, 230))
							elif "|>" in (f.replace(";", "|")):
								abttext=simplefontmono.render(("{:<5}".format(str(linecnt)) + " " + f.replace("\n", "")), True, (0,0,0), (230, 255, 230))
							elif (f.replace(";", "|")).count("|")==2:
								abttext=simplefontmono.render(("{:<5}".format(str(linecnt)) + " " + f.replace("\n", "")), True, (0,0,0), (230, 230, 255))

							else:
								abttext=simplefontmono.render(("{:<5}".format(str(linecnt)) + " " + f.replace("\n", "")), True, (0,0,0), (255, 255, 255))
					else:
						abttext=simplefontmono.render(("{:<5}".format(str(linecnt)) + " " + f.replace("\n", "")), True, (0,0,0), (255, 255, 255))
					screensurf.blit(abttext, (textx, texty))
				if f.startswith("textstart") and tasmflg==1:
					textblk=1
				
				texty += yjump
				linecnt += 1
				if texty>screenh:
					break
			pygame.display.update()
			qtexty=texty
		for event in pygame.event.get():
			if event.type == QUIT:
				qflg=1
				break
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-codeview.png')))
				break
			if event.type == KEYDOWN and event.key == K_DOWN:
				if qtexty>(yjump + yjump):
					yoff -= yjump
			if event.type == KEYDOWN and event.key == K_UP:
				yoff += yjump
				if yoff>0:
					yoff=0
			if event.type == KEYDOWN and event.key == K_PAGEUP:
				yoff += (yjump * 20)
				if yoff>0:
					yoff=0
			if event.type == KEYDOWN and event.key == K_PAGEDOWN:
				if qtexty>(yjump + yjump):
					yoff -= (yjump * 20)
				#if qtexty<0:
				#	yoff=0
			if event.type == KEYDOWN and event.key == K_LEFT:
				textx += yjump
				redraw=1
			if event.type == KEYDOWN and event.key == K_RIGHT:
				textx -= yjump
				redraw=1
			if event.type == KEYDOWN and event.key == K_F1:
				subprocess.Popen(["python", "helpview.py", "codeview.xml"])
			if event.type == KEYDOWN and (event.key == K_PLUS or event.key == K_EQUALS or event.key == K_KP_PLUS):
				yjump += 1
				fontsize += 1
				simplefontmono = pygame.font.SysFont("monospace", fontsize, bold=True)
				redraw=1
			if event.type == KEYDOWN and (event.key == K_MINUS or event.key == K_KP_MINUS):
				yjump -= 1
				fontsize -= 1
				if yjump<=0:
					yjump=1
				if fontsize<=0:
					fontsize=1
				simplefontmono = pygame.font.SysFont("monospace", fontsize, bold=True)
				redraw=1
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				qflg=1
				break
			if event.type == KEYDOWN and event.key == K_SPACE:
				yoff=0
				textx=0
				redraw=1
			if event.type==MOUSEBUTTONDOWN:
				if event.button==5:
					if qtexty>(yjump + yjump):
						yoff -= yjump
				if event.button==4:
					yoff += yjump
					if yoff>0:
						yoff=0
				if event.button==3:
					yoff=0
					textx=0
					redraw=1
			if event.type==VIDEORESIZE:
				resizeflg=1
				resw=event.w
				resh=event.h
				time.sleep(0.1)
				break


#image viewer
	
def imgview(imgfile):
	global screensurf
	#load image
	img=pygame.image.load(imgfile).convert_alpha()
	#set window caption
	pygame.display.set_caption(("imgview - " + imgfile), ("imgview - " + imgfile))
	#set inital scale factor
	scalefact=float(1.0)
	#0.9 IS CORRECT
	pscalefact=float(0.9)
	qflg=0
	#set inital offset
	xoff=(screensurf.get_rect().centerx)
	yoff=(screensurf.get_rect().centery)
	roto=0.1
	resizeflg=0
	followmouse=0
	pygame.key.set_repeat(250, 50)
	#get size of image
	imgx=img.get_width()
	imgy=img.get_height()
	#some basic intelegent inital scale logic
	if imgx<=400 and imgy<=300:
		scalefact=float(2.0)
	if imgx<=266 and imgy<=200:
		scalefact=float(3.0)	
	if imgx<=200 and imgy<=150:
		scalefact=float(4.0)
	if imgx<=133 and imgy<=100:
		scalefact=float(6.0)
	if imgx<=50 and imgy<=75:
		scalefact=float(8.0)
	if imgx<=66 and imgy<=50:
		scalefact=float(12.0)
	if imgx<=25 and imgy<=38:
		scalefact=float(16.0)
	defscale=scalefact
	#main loop
	scupdate=1
	while qflg==0:
		#resize logic. (the extra loop before resizing is to keep resizing smooth on certain window managers that "stop" resizing operations when set_mode is called.
		if resizeflg==1:
			resizeflg=2	
		elif resizeflg==2:
			screensurf=pygame.display.set_mode((resw, resh), pygame.RESIZABLE)
			xoff=(screensurf.get_rect().centerx)
			yoff=(screensurf.get_rect().centery)
			resizeflg=0
			scupdate=1
		if scupdate==1:
			scupdate=0
			screensurf.fill((151, 178, 208))
			#imgsc=pygame.transform.rotozoom(img, 0.0, scalefact)
			#if scale factor is different from the previous scale factor, rescale image.
			if scalefact!=pscalefact:
				imgsc=pygame.transform.scale(img, ((int(imgx * scalefact)), (int(imgy * scalefact))))
				pscalefact=scalefact
			#create draw box and draw image
			imgbox = imgsc.get_rect()
			imgbox.centerx = xoff
			imgbox.centery = yoff
			screensurf.blit(imgsc, imgbox)
			pygame.display.update()
		time.sleep(0.05)
		#move image in relation to mouse when followmouse is set to 1 (see event handler below)
		if followmouse==1:
			ppos=mpos
			mpos=pygame.mouse.get_pos()
			xoff -=(ppos[0] - mpos[0])
			yoff -=(ppos[1] - mpos[1])
			scupdate=1
		
		for event in pygame.event.get():
			if event.type == QUIT:
				qflg=1
				break
			if event.type == KEYDOWN and (event.key == K_MINUS or event.key == K_KP_MINUS):
				scalefact -= roto
				if scalefact<=0:
					scalefact=0.1
				scupdate=1
			if event.type == KEYDOWN and (event.key == K_PLUS or event.key == K_EQUALS or event.key == K_KP_PLUS):
				scalefact += roto
				scupdate=1
			if event.type == KEYDOWN and event.key == K_DOWN:
				yoff -= 10
				scupdate=1
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-imgview.png')))
				break
			if event.type == KEYDOWN and event.key == K_UP:
				yoff += 10
				scupdate=1
			if event.type == KEYDOWN and event.key == K_LEFT:
				xoff += 10
				scupdate=1
			if event.type == KEYDOWN and event.key == K_RIGHT:
				xoff -= 10
				scupdate=1
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				qflg=1
				break
			if event.type == KEYDOWN and event.key == K_F1:
				subprocess.Popen(["python", "helpview.py", "imgview.xml"])
			if event.type == KEYDOWN and event.key == K_SPACE:
				roto = 0.1
				scalefact = defscale
				xoff=(screensurf.get_rect().centerx)
				yoff=(screensurf.get_rect().centery)
				scupdate=1
			if event.type==MOUSEBUTTONDOWN:
				if event.button==5:
					#roto -= 0.1
					#if roto<=0:
					#	roto=0.1
					scalefact -= roto
					if scalefact<=0:
						scalefact=0.1
					scupdate=1
				if event.button==4:
				#	roto += 0.1
				#	if roto>1:
				#		roto=1.0
					scalefact += roto
					scupdate=1
				#this resets the offset & scale factor
				if event.button==3:
					roto = 0.1
					scalefact = defscale
					xoff=(screensurf.get_rect().centerx)
					yoff=(screensurf.get_rect().centery)
					scupdate=1
				#sets followmouse to 1 for image moving
				if event.button==1:
					followmouse=1
					mpos=pygame.mouse.get_pos()
			if event.type==MOUSEBUTTONUP:
				#sets followmouse to 0 to stop image moving
				if event.button==1:
					followmouse=0
			#sets resizeflg to 1 to start screen resizing process.
			if event.type==VIDEORESIZE:
				resizeflg=1
				resw=event.w
				resh=event.h
				time.sleep(0.1)
				break
				
				
#credits scroller

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
				elif qlid=="-<SBTCCAT>-":
					abttextbox=sbtccat.get_rect()
					abttextbox.centerx=scrollsurf.get_rect().centerx
					abttextbox.y=pixcnt1
					scrollsurf.blit(sbtccat, abttextbox)
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
				elif event.type == KEYDOWN and event.key == K_RETURN:
					return()
				elif event.type == MOUSEBUTTONDOWN and event.button==1:
					return()
				elif event.type == QUIT:
					return()



