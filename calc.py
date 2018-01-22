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
import VMSYSTEM.libvmui as vmui
import VMSYSTEM.libbaltcalc as libbaltcalc
from pygame.locals import *
import VMSYSTEM.libthemeconf as libthemeconf

pygame.display.init()
pygame.font.init()

simplefont = pygame.font.SysFont(None, 22)
btnfont = pygame.font.SysFont(None, 21)
pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN])
pygame.display.set_caption(("Ternary Calculator"), ("Ternary Calculator"))

windowicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'calc.png'))
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((450, 450))

vmui.initui(screensurf, 1)

def makebtn(text, text2=None):
	btn=pygame.Surface((60, 60))
	btnlocrec=pygame.Rect(0, 0, 60, 60)
	btn.fill(libthemeconf.calcpadbg)
	pygame.draw.rect(btn, libthemeconf.calcpadline, btnlocrec, 1)
	texgfx=btnfont.render(text, True, libthemeconf.calcpadtext, libthemeconf.calcpadbg)
	btn.blit(texgfx, ((30 - (texgfx.get_width() // 2)), 2))
	if text2!=None:
		texgfx=btnfont.render(text2, True, libthemeconf.calcpadtext, libthemeconf.calcpadbg)
		btn.blit(texgfx, ((30 - (texgfx.get_width() // 2)), 30))
	return btn

#bg=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'bg.jpg')).convert()
bg=pygame.Surface((450, 500))
#lockon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'lockon.png')).convert_alpha()
#lockoff=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'lockoff.png')).convert_alpha()
lockon=pygame.Surface((60, 60), SRCALPHA)
lockoff=pygame.Surface((60, 60), SRCALPHA)
lockrect=pygame.Rect(0, 48, 60, 12)

pygame.draw.rect(lockon, libthemeconf.calclockon, lockrect, 0)
pygame.draw.rect(lockon, libthemeconf.calcpadline, lockrect, 1)
pygame.draw.rect(lockoff, libthemeconf.calclockoff, lockrect, 0)
pygame.draw.rect(lockoff, libthemeconf.calcpadline, lockrect, 1)
#row 1 gfx
add=makebtn("ADD")
sub=makebtn("SUB")
div=makebtn("DIV")
mul=makebtn("MUL")
copyab=makebtn("COPY", "A>B")
inverta=makebtn("INVERT", "A")
#row 2 gfx
copyba=makebtn("COPY", "B>A")
invertb=makebtn("INVERT", "B")
mpi=makebtn("mpi")
mcv=makebtn("mcv")
resa=makebtn("res>A")
resb=makebtn("res>B")
#row 3 gfx
swap=makebtn("swap")
mni=makebtn("mni")
quitg=makebtn("QUIT")
helpg=makebtn("HELP")

scupdate=1
qflg=0


bgrect1=pygame.Rect(0, 0, 450, 256)
bg.fill(libthemeconf.hudbg)
pygame.draw.rect(bg, libthemeconf.deskcolor, bgrect1, 0)

#clickboxes for user text inputs
tritabx=pygame.Rect(20, 95, 404, 24)
decabx=pygame.Rect(20, 119, 404, 24)
tritbbx=pygame.Rect(20, 159, 404, 24)
decbbx=pygame.Rect(20, 183, 404, 24)
resbx=pygame.Rect(20, 19, 404, 64)

#draw input boxes and result box...
pygame.draw.rect(bg, libthemeconf.textboxbg, resbx, 0)
pygame.draw.rect(bg, libthemeconf.textboxline, resbx, 1)

pygame.draw.rect(bg, libthemeconf.textboxbg, tritabx, 0)
pygame.draw.rect(bg, libthemeconf.textboxline, tritabx, 1)

pygame.draw.rect(bg, libthemeconf.textboxbg, decabx, 0)
pygame.draw.rect(bg, libthemeconf.textboxline, decabx, 1)

pygame.draw.rect(bg, libthemeconf.textboxbg, tritbbx, 0)
pygame.draw.rect(bg, libthemeconf.textboxline, tritbbx, 1)

pygame.draw.rect(bg, libthemeconf.textboxbg, decbbx, 0)
pygame.draw.rect(bg, libthemeconf.textboxline, decbbx, 1)

#draw buttons onto background.
padx=22
pady=260
#row 1
addx=bg.blit(add, (padx, pady))
padx += 60
subx=bg.blit(sub, (padx, pady))
padx += 60
mulx=bg.blit(mul, (padx, pady))
padx += 60
divx=bg.blit(div, (padx, pady))
padx += 60
copyabx=bg.blit(copyab, (padx, pady))
padx += 60
invertax=bg.blit(inverta, (padx, pady))
padx = 22
pady += 60
#row 2
mpix=bg.blit(mpi, (padx, pady))
padx += 60
mcvx=bg.blit(mcv, (padx, pady))
padx += 60
resa=bg.blit(resa, (padx, pady))
resax=padx
resay=pady
padx += 60
resb=bg.blit(resb, (padx, pady))
resbx=padx
resby=pady
padx += 60
copybax=bg.blit(copyba, (padx, pady))
padx += 60
invertbx=bg.blit(invertb, (padx, pady))
padx = 22
pady += 60
#row 3
mnix=bg.blit(mni, (padx, pady))
padx += 60
swapx=bg.blit(swap, (padx, pady))
padx += 60
helpx=bg.blit(helpg, (padx, pady))
padx += 60
quitx=bg.blit(quitg, (padx, pady))
padx += 60

terncalc=simplefont.render("SBTCVM Ternary Calculator", True, libthemeconf.desktext)
bg.blit(terncalc, (2, 230))
slab=simplefont.render("s.", True, libthemeconf.desktext)
bg.blit(slab, (2, 20))
tlab=simplefont.render("T", True, libthemeconf.desktext)
bg.blit(tlab, (2, 40))
bg.blit(tlab, (2, 97))
bg.blit(tlab, (2, 161))

dlab=simplefont.render("D", True, libthemeconf.desktext)
bg.blit(dlab, (2, 60))
bg.blit(dlab, (2, 121))
bg.blit(dlab, (2, 186))

#inital register values
TA="0"
DA=0
TB="0"
DB=0
TR="0"
DR=0
#inital status
STAT="SBTCVM T.C. V2.0.3 Ready."
#limits the mpi, mcv, and mni calculations. too high numbers can take WAYYY too long
mcalclimit=36
#result copy locks
resalock=0
resblock=0
docopy=0
#inputtextcol=(0, 0, 0)
#bgcol=(255, 255, 255)
engtimer=pygame.time.Clock()
while qflg==0:
	if scupdate==1:
		scupdate=0
		screensurf.blit(bg, (0, 0))
		#readout text
		texgfx=simplefont.render(TA, True, libthemeconf.textboxtext, libthemeconf.textboxbg)
		screensurf.blit(texgfx, (22, 97))
		texgfx=simplefont.render(str(DA), True, libthemeconf.textboxtext, libthemeconf.textboxbg)
		screensurf.blit(texgfx, (22, 121))
		texgfx=simplefont.render(TB, True, libthemeconf.textboxtext, libthemeconf.textboxbg)
		screensurf.blit(texgfx, (22, 161))
		texgfx=simplefont.render(str(DB), True, libthemeconf.textboxtext, libthemeconf.textboxbg)
		screensurf.blit(texgfx, (22, 186))
		texgfx=simplefont.render(STAT, True, libthemeconf.textboxtext, libthemeconf.textboxbg)
		screensurf.blit(texgfx, (22, 20))
		texgfx=simplefont.render(TR, True, libthemeconf.textboxtext, libthemeconf.textboxbg)
		screensurf.blit(texgfx, (22, 40))
		texgfx=simplefont.render(str(DR), True, libthemeconf.textboxtext, libthemeconf.textboxbg)
		screensurf.blit(texgfx, (22, 60))
		#result copy lock overlays:
		if resalock==1:
			screensurf.blit(lockon, (resax, resay))
		else:
			screensurf.blit(lockoff, (resax, resay))
		if resblock==1:
			screensurf.blit(lockon, (resbx, resby))
		else:
			screensurf.blit(lockoff, (resbx, resby))
		
		pygame.display.update()
	#time.sleep(0.1)
	engtimer.tick(30)	
	#event handler
	for event in pygame.event.get():
		keymods=pygame.key.get_mods()
		if event.type == QUIT:
			qflg=1
			break
		if event.type == KEYDOWN and event.key == K_F1:
			subprocess.Popen(["python", "helpview.py", "calc.xml"])
		if event.type == KEYDOWN and event.key == K_F8:
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-calc.png')))
			break
		if event.type==MOUSEBUTTONDOWN:
			#button Operations code
			#first ROW
			if addx.collidepoint(event.pos)==1 and event.button==1:
				DR=DA + DB
				TR=libbaltcalc.DECTOBT(DR)
				STAT="SUM A & B"
				scupdate=1
				docopy=1
			if subx.collidepoint(event.pos)==1 and event.button==1:
				DR=DA - DB
				TR=libbaltcalc.DECTOBT(DR)
				STAT="SUBTRACT A & B"
				scupdate=1
				docopy=1
			if divx.collidepoint(event.pos)==1 and event.button==1:
				try:
					DR=DA // DB
					STAT="DIVIDE A & B"
				except ZeroDivisionError:
					STAT="DIVIDE BY ZERO ERROR"
				TR=libbaltcalc.DECTOBT(DR)
				docopy=1
				scupdate=1
			if mulx.collidepoint(event.pos)==1 and event.button==1:
				DR=DA * DB
				TR=libbaltcalc.DECTOBT(DR)
				STAT="MULTIPLY A & B"
				scupdate=1
				docopy=1
			if copyabx.collidepoint(event.pos)==1 and event.button==1:
				DB=DA
				TB=libbaltcalc.DECTOBT(DB)
				STAT="COPY A TO B"
				scupdate=1
				
			if invertax.collidepoint(event.pos)==1 and event.button==1:
				DA=( - DA)
				TA=libbaltcalc.DECTOBT(DA)
				STAT="INVERT A"
				scupdate=1
			#row 2
			if mpix.collidepoint(event.pos)==1 and event.button==1:
				if abs(DA)<=mcalclimit:
					DR=libbaltcalc.mpi(abs(DA))
					TR=libbaltcalc.DECTOBT(DR)
					STAT="mpi of A (DEC)"
					scupdate=1
					docopy=1
				else:
					STAT="mpi of over 36 is too large"
					scupdate=1
			if mcvx.collidepoint(event.pos)==1 and event.button==1:
				if abs(DA)<=mcalclimit:
					DR=libbaltcalc.mcv(abs(DA))
					TR=libbaltcalc.DECTOBT(DR)
					STAT="mcv of A (DEC)"
					scupdate=1
					docopy=1
				else:
					STAT="mcv of over 36 is too large"
					scupdate=1
			
			if resa.collidepoint(event.pos)==1 and event.button==1 and keymods & KMOD_SHIFT:
				if resalock==1:
					resalock=0
				else:
					resalock=1
				scupdate=1
			elif resa.collidepoint(event.pos)==1 and event.button==1:
				DA=DR
				TA=libbaltcalc.DECTOBT(DA)
				STAT="copy RESULT to A"
				scupdate=1
			if resb.collidepoint(event.pos)==1 and event.button==1 and keymods & KMOD_SHIFT:
				if resblock==1:
					resblock=0
				else:
					resblock=1
				scupdate=1
			elif resb.collidepoint(event.pos)==1 and event.button==1:
				DB=DR
				TB=libbaltcalc.DECTOBT(DB)
				STAT="copy RESULT to B"
				scupdate=1
			if copybax.collidepoint(event.pos)==1 and event.button==1:
				DA=DB
				TA=libbaltcalc.DECTOBT(DA)
				STAT="COPY B TO A"
				scupdate=1
			if invertbx.collidepoint(event.pos)==1 and event.button==1:
				DB=( - DB)
				TB=libbaltcalc.DECTOBT(DB)
				STAT="INVERT B"
				scupdate=1
			#row 3
			if mnix.collidepoint(event.pos)==1 and event.button==1:
				if abs(DA)<=mcalclimit:
					DR=libbaltcalc.mni(abs(DA))
					TR=libbaltcalc.DECTOBT(DR)
					STAT="mni of A (DEC)"
					scupdate=1
					docopy=1
				else:
					STAT="mni of over 36 is too large"
					scupdate=1
			if swapx.collidepoint(event.pos)==1 and event.button==1:
				TEMPD=DA
				DA=DB
				DB=TEMPD
				TA=libbaltcalc.DECTOBT(DA)
				TB=libbaltcalc.DECTOBT(DB)
				STAT="swap A & B"
				scupdate=1
			if helpx.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "helpview.py", "calc.xml"])
			if quitx.collidepoint(event.pos)==1 and event.button==1:
				qflg=1
				break
			if docopy==1:
				docopy=0
				if resalock==1:
					DA=DR
					TA=libbaltcalc.DECTOBT(DA)
				if resblock==1:
					DB=DR
					TB=libbaltcalc.DECTOBT(DB)
			#special button locks - event process
			if resa.collidepoint(event.pos)==1 and event.button==3:
				if resalock==1:
					resalock=0
				else:
					resalock=1
				scupdate=1
			if resb.collidepoint(event.pos)==1 and event.button==3:
				if resblock==1:
					resblock=0
				else:
					resblock=1
				scupdate=1
			#data input handlers (powered by vmui's textinput function)
			if tritabx.collidepoint(event.pos)==1 and event.button==1:
				texgfx=simplefont.render(TA, True, (255, 255, 255), (255, 255, 255))
				screensurf.blit(texgfx, (22, 97))
				TA=vmui.textinput(22, 97, fontsize=22, textstring=TA, acceptchars="-0+")
				scupdate=1
				DA=libbaltcalc.BTTODEC(TA)
			if decabx.collidepoint(event.pos)==1 and event.button==1:
				texgfx=simplefont.render(str(DA), True, (255, 255, 255), (255, 255, 255))
				screensurf.blit(texgfx, (22, 121))
				try:
					DA=int(vmui.textinput(22, 121, fontsize=22, textstring=str(DA), acceptchars="0987654321-"))
				except ValueError:
					print "SYNTAX ERROR IN DECIMAL INPUT A"
					STAT="SYNTAX ERROR IN DECIMAL INPUT A"
				scupdate=1
				TA=libbaltcalc.DECTOBT(DA)
			if tritbbx.collidepoint(event.pos)==1 and event.button==1:
				texgfx=simplefont.render(TB, True, (255, 255, 255), (255, 255, 255))
				screensurf.blit(texgfx, (22, 161))
				TB=vmui.textinput(22, 161, fontsize=22, textstring=TB, acceptchars="-0+")
				scupdate=1
				DB=libbaltcalc.BTTODEC(TB)
			if decbbx.collidepoint(event.pos)==1 and event.button==1:
				texgfx=simplefont.render(str(DB), True, (255, 255, 255), (255, 255, 255))
				screensurf.blit(texgfx, (22, 186))
				try:
					DB=int(vmui.textinput(22, 186, fontsize=22, textstring=str(DB), acceptchars="0987654321-"))
				except ValueError:
					print "SYNTAX ERROR IN DECIMAL INPUT B"
					STAT="SYNTAX ERROR IN DECIMAL INPUT B"
				scupdate=1
				TB=libbaltcalc.DECTOBT(DB)
				
