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

print "SBTCVM FileView file browser. v1.2"
pygame.display.init()
pygame.font.init()
pygame.mixer.init()

pathlist=list()

windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fileview64.png'))
pygame.display.set_icon(windowicon)

class fileclick:
	def __init__(self, box, filename, ftype):
		self.box=box
		self.filename=filename
		self.ftype=ftype
screensurf=pygame.display.set_mode((800, 600))

filebg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fileview.jpg')).convert()
exitbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvquit.png')).convert()
helpbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvhelp.png')).convert()
fvstreg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvstreg.png')).convert()
fvtrom=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvtrom.png')).convert()
fvdir=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvdir.png')).convert()
fvup=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvup.png')).convert()
fvimg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvimg.png')).convert()
fvtext=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvtext.png')).convert()
fvtasm=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvtasm.png')).convert()
fvall=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvall.png')).convert()
quitflag=0
simplefontC = pygame.font.SysFont(None, 22)
simplefontB = pygame.font.SysFont(None, 19)
listyoff=0
listx=41
iconx=0
labelx=48
maskx=0
filterflg=0
filtertext="All"
yjump=42
iterfiles='.'
pygame.display.set_caption(("fileview - " + iterfiles), ("fileview - " + iterfiles))
quitx=filebg.blit(exitbtn, (708, 107))
ghelpx=filebg.blit(helpbtn, (749, 107))
fil0=filebg.blit(fvall, (430, 107))
fil1=filebg.blit(fvtrom, (471, 107))
fil2=filebg.blit(fvimg, (512, 107))
fil3=filebg.blit(fvstreg, (553, 107))
fil4=filebg.blit(fvtasm, (594, 107))
fil5=filebg.blit(fvtext, (635, 107))
fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
scupdate=1
while quitflag==0:
	if scupdate==1:
		scupdate=0
		screensurf.blit(filebg, (0, 0))
		listy=listyoff
		textit=simplefontB.render(".", True, (0, 0, 0), (255, 255, 255))
		
		#ix=screensurf.blit(fvdir, (iconx, listy))
		#gx=screensurf.blit(textit, (listx, listy))
		gxmask=pygame.Surface((410, 40))
		gxmask.fill((255, 255, 255))
		gxmask.blit(fvdir, (iconx, 0))
		gxmask.blit(textit, (labelx, 0))
		#gx=screensurf.blit(gxmask, (maskx, listy))
		mpos=pygame.mouse.get_pos()
		flist=list()
		#qx=fileclick(gx, ".", "dir")
		#flist.extend([qx])
		#listy += yjump
		if iterfiles!='.':
			#print iterfiles
			textit=simplefontB.render("..", True, (0, 0, 0), (255, 255, 255))
			gxmask=pygame.Surface((410, 40))
			gxmask.fill((255, 255, 255))
			gxmask.blit(fvup, (iconx, 0))
			gxmask.blit(textit, (labelx, 0))
			gx=screensurf.blit(gxmask, (maskx, listy))
			qx=fileclick(gx, "..", "dir")
			flist.extend([qx])
			listy += yjump
		for fname in sorted(os.listdir(iterfiles), key=str.lower):
			fnamelo=fname.lower()
			fileval=0
			if os.path.isdir(os.path.join(iterfiles, fname)):
				#if not os.path.basename(fname).startswith('.'):
				if not fname.endswith(".git"):
					#print fname
					textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
					gxmask=pygame.Surface((410, 40))
					gxmask.fill((255, 255, 255))
					gxmask.blit(fvdir, (iconx, 0))
					gxmask.blit(textit, (labelx, 0))
					gx=screensurf.blit(gxmask, (maskx, listy))
					qx=fileclick(gx, fname, "dir")
					fileval=1
			elif fnamelo.endswith(("." + "trom")) and (filterflg==0 or filterflg==1): 
				#print(os.path.join(iterfiles, fname))
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvtrom, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "trom")
				fileval=1
			elif (fnamelo.endswith(("." + "png")) or fnamelo.endswith(("." + "jpg")) or fnamelo.endswith(("." + "jpeg")) or fnamelo.endswith(("." + "gif"))) and (filterflg==0 or filterflg==2):
				#print(os.path.join(iterfiles, fname))
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvimg, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "img")
				fileval=1
			#elif fnamelo.endswith(("." + "tasm")): 
			##	print(os.path.join(iterfiles, fname))
			#	textit=simplefontB.render("{:<30}".format(fname), True, (0, 0, 0), (255, 200, 200))
			#	gx=screensurf.blit(textit, (listx, listy))
			#	qx=fileclick(gx, fname, "tasm")
			#	fileval=1
			elif fnamelo.endswith(("." + "streg")) and (filterflg==0 or filterflg==3) : 
				#print(os.path.join(iterfiles, fname))
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvstreg, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "streg")
				fileval=1
			elif fnamelo.endswith(("." + "tasm")) and (filterflg==0 or filterflg==4) : 
				#print(os.path.join(iterfiles, fname))
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvtasm, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "tasm")
				fileval=1
			elif (fnamelo.endswith(("." + "txt")) or fnamelo.endswith(("." + "md"))) and (filterflg==0 or filterflg==5) : 
				#print(os.path.join(iterfiles, fname))
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvtext, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "text")
				fileval=1
			#else:
			#	if not fname.startswith('.'):
			#		textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
			#		gx=screensurf.blit(textit, (listx, listy))
			#		fileval=1
			if fileval==1:
				flist.extend([qx])
				listy += yjump
		menulabel=simplefontC.render(("path: " + iterfiles), True, (0, 0, 0))
		screensurf.blit(menulabel, (430, 70))
	
		screensurf.blit(fillabel, (430, 88))
	
		#for hig in flist:
		#	if hig.box.collidepoint(mpos):
		#		pygame.draw.rect(screensurf, (41, 74, 185), hig.box, 1)
		pygame.display.update()
	#time.sleep(0.1)
	time.sleep(0.03)
	
	
	for event in pygame.event.get():
		if event.type == QUIT:
			quitflag=1
			break
		if event.type == KEYDOWN and event.key == K_F1:
			subprocess.Popen(["python", "MK2-TOOLS.py", "helpview", "fileview.txt"])
		if event.type == KEYDOWN and event.key == K_F8:
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-fileview.png')))
			break
		if event.type==MOUSEBUTTONDOWN:
			if quitx.collidepoint(event.pos)==1 and event.button==1:
				quitflag=1
				break
			if ghelpx.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "MK2-TOOLS.py", "helpview", "fileview.txt"])
			if fil0.collidepoint(event.pos)==1 and event.button==1:
				filterflg=0
				filtertext="All"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
			if fil1.collidepoint(event.pos)==1 and event.button==1:
				filterflg=1
				filtertext="TROM"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
			if fil2.collidepoint(event.pos)==1 and event.button==1:
				filterflg=2
				filtertext="Image"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
			if fil3.collidepoint(event.pos)==1 and event.button==1:
				filterflg=3
				filtertext="STREG"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
			if fil4.collidepoint(event.pos)==1 and event.button==1:
				filterflg=4
				filtertext="TASM"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
			if fil5.collidepoint(event.pos)==1 and event.button==1:
				filterflg=5
				filtertext="Text"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
			for f in flist:
				if f.box.collidepoint(event.pos)==1 and event.button==1:
					if f.ftype=="trom":
						subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="tasm":
						subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="streg":
						subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="img":
						subprocess.Popen(["python", "MK2-TOOLS.py", "imgview", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="text":
						subprocess.Popen(["python", "MK2-TOOLS.py", "textview", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="dir":
						listyoff=0
						scupdate=1
						if f.filename=='.':
							pathlist=list()
							iterfiles='.'
						if f.filename=='..':
							#print pathlist
							pathlist.remove(pathlist[(len(pathlist) -1)])
							#print pathlist
							if pathlist==list():
								iterfiles='.'
							else:
								iterfiles=os.path.join(*pathlist)
						else:
							pathlist.extend([f.filename])
							iterfiles=os.path.join(*pathlist)
						pygame.display.set_caption(("fileview - " + iterfiles), ("fileview - " + iterfiles))
						break
						
				if event.button==4:
					if listyoff<0:
						listyoff += yjump
						scupdate=1
					break
					
				if event.button==5:
					if listy>600:
						listyoff -= yjump
						scupdate=1
					if listyoff>0:
						listyoff=0
						scupdate=1
					break
					
				
		time.sleep(0.01)
			