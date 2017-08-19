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

pygame.display.init()
pygame.font.init()

simplefont = pygame.font.SysFont(None, 22)
pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN])
pygame.display.set_caption(("Ternary Calculator"), ("Ternary Calculator"))

windowicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'icon.png'))
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((450, 500))

vmui.initui(screensurf, 1)

bg=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'bg.jpg')).convert()
lockon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'lockon.png')).convert_alpha()
lockoff=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'lockoff.png')).convert_alpha()
#row 1 gfx
add=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'add.png')).convert()
sub=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'sub.png')).convert()
div=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'div.png')).convert()
mul=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'mul.png')).convert()
copyab=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'copyab.png')).convert()
inverta=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'inverta.png')).convert()
#row 2 gfx
mpi=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'mpi.png')).convert()
mcv=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'mcv.png')).convert()
resa=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'resa.png')).convert()
resb=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'resb.png')).convert()
copyba=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'copyba.png')).convert()
invertb=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'invertb.png')).convert()
#row 3 gfx
swap=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'swap.png')).convert()
mni=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'mni.png')).convert()
quitg=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'quit.png')).convert()
helpg=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "calc", 'help.png')).convert()

scupdate=1
qflg=0

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

#clickboxes for user text inputs
tritabx=pygame.Rect(22, 97, 404, 24)
decabx=pygame.Rect(22, 121, 404, 24)
tritbbx=pygame.Rect(22, 161, 404, 24)
decbbx=pygame.Rect(22, 186, 404, 24)
#inital register values
TA="0"
DA=0
TB="0"
DB=0
TR="0"
DR=0
#inital status
STAT="Ready"
#limits the mpi, mcv, and mni calculations. too high numbers can take WAYYY too long
mcalclimit=36
#result copy locks
resalock=0
resblock=0
docopy=0
inputtextcol=(0, 0, 0)
bgcol=(210, 210, 255)
while qflg==0:
	if scupdate==1:
		scupdate=0
		screensurf.blit(bg, (0, 0))
		#readout text
		texgfx=simplefont.render(TA, True, (0, 0, 0), (255, 255, 255))
		screensurf.blit(texgfx, (22, 97))
		texgfx=simplefont.render(str(DA), True, (0, 0, 0), (255, 255, 255))
		screensurf.blit(texgfx, (22, 121))
		texgfx=simplefont.render(TB, True, (0, 0, 0), (255, 255, 255))
		screensurf.blit(texgfx, (22, 161))
		texgfx=simplefont.render(str(DB), True, (0, 0, 0), (255, 255, 255))
		screensurf.blit(texgfx, (22, 186))
		texgfx=simplefont.render(STAT, True, (0, 0, 0), (255, 255, 255))
		screensurf.blit(texgfx, (22, 20))
		texgfx=simplefont.render(TR, True, (0, 0, 0), (255, 255, 255))
		screensurf.blit(texgfx, (22, 40))
		texgfx=simplefont.render(str(DR), True, (0, 0, 0), (255, 255, 255))
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
	time.sleep(0.1)
		
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
				TA=vmui.textinput(22, 97, fontsize=22, textcol=inputtextcol, bgcol=bgcol, textstring=TA, acceptchars="-0+")
				scupdate=1
				DA=libbaltcalc.BTTODEC(TA)
			if decabx.collidepoint(event.pos)==1 and event.button==1:
				texgfx=simplefont.render(str(DA), True, (255, 255, 255), (255, 255, 255))
				screensurf.blit(texgfx, (22, 121))
				try:
					DA=int(vmui.textinput(22, 121, fontsize=22, textcol=inputtextcol, bgcol=bgcol, textstring=str(DA), acceptchars="0987654321-"))
				except ValueError:
					print "SYNTAX ERROR IN DECIMAL INPUT A"
					STAT="SYNTAX ERROR IN DECIMAL INPUT A"
				scupdate=1
				TA=libbaltcalc.DECTOBT(DA)
			if tritbbx.collidepoint(event.pos)==1 and event.button==1:
				texgfx=simplefont.render(TB, True, (255, 255, 255), (255, 255, 255))
				screensurf.blit(texgfx, (22, 161))
				TB=vmui.textinput(22, 161, fontsize=22, textcol=inputtextcol, bgcol=bgcol, textstring=TB, acceptchars="-0+")
				scupdate=1
				DB=libbaltcalc.BTTODEC(TB)
			if decbbx.collidepoint(event.pos)==1 and event.button==1:
				texgfx=simplefont.render(str(DB), True, (255, 255, 255), (255, 255, 255))
				screensurf.blit(texgfx, (22, 186))
				try:
					DB=int(vmui.textinput(22, 186, fontsize=22, textcol=inputtextcol, bgcol=bgcol, textstring=str(DB), acceptchars="0987654321-"))
				except ValueError:
					print "SYNTAX ERROR IN DECIMAL INPUT B"
					STAT="SYNTAX ERROR IN DECIMAL INPUT B"
				scupdate=1
				TB=libbaltcalc.DECTOBT(DB)
				
