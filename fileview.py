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
exitbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'exit.png'))
fvstreg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvstreg.png'))
fvtrom=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvtrom.png'))
fvdir=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvdir.png'))
fvup=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvup.png'))
fvimg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'fvimg.png'))
quitflag=0
simplefontC = pygame.font.SysFont(None, 22)
simplefontB = pygame.font.SysFont(None, 19)
listyoff=0
listx=41
iconx=0
labelx=48
maskx=0
yjump=42
iterfiles='.'
pygame.display.set_caption(("fileview - " + iterfiles), ("fileview - " + iterfiles))
while quitflag==0:
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
		elif fnamelo.endswith(("." + "trom")): 
			#print(os.path.join(iterfiles, fname))
			textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
			gxmask=pygame.Surface((410, 40))
			gxmask.fill((255, 255, 255))
			gxmask.blit(fvtrom, (iconx, 0))
			gxmask.blit(textit, (labelx, 0))
			gx=screensurf.blit(gxmask, (maskx, listy))
			qx=fileclick(gx, fname, "trom")
			fileval=1
		elif fnamelo.endswith(("." + "png")) or fnamelo.endswith(("." + "jpg")) or fnamelo.endswith(("." + "jpeg")) or fnamelo.endswith(("." + "gif")): 
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
		elif fnamelo.endswith(("." + "streg")): 
			#print(os.path.join(iterfiles, fname))
			textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
			gxmask=pygame.Surface((410, 40))
			gxmask.fill((255, 255, 255))
			gxmask.blit(fvstreg, (iconx, 0))
			gxmask.blit(textit, (labelx, 0))
			gx=screensurf.blit(gxmask, (maskx, listy))
			qx=fileclick(gx, fname, "streg")
			fileval=1
		#else:
		#	if not fname.startswith('.'):
		#		textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
		#		gx=screensurf.blit(textit, (listx, listy))
		#		fileval=1
		if fileval==1:
			flist.extend([qx])
			listy += yjump
	#time.sleep(0.1)
	time.sleep(0.01)
	quitx=screensurf.blit(exitbtn, (430, 520))
	menulabel=simplefontC.render(("path: " + iterfiles), True, (255, 255, 255))
	screensurf.blit(menulabel, (430, 70))
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == QUIT:
			quitflag=1
			break
		if event.type==MOUSEBUTTONDOWN:
			for f in flist:
				if quitx.collidepoint(event.pos)==1 and event.button==1:
					quitflag=1
					break
				if f.box.collidepoint(event.pos)==1 and event.button==1:
					if f.ftype=="trom":
						subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="tasm":
						print "run tasm"
					if f.ftype=="streg":
						subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="img":
						subprocess.Popen(["python", "MK2-TOOLS.py", "imgview", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="dir":
						listyoff=0
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
					break
				if event.button==5:
					if listy>600:
						listyoff -= yjump
					if listyoff>0:
						listyoff=0
					break
				
		time.sleep(0.01)
			