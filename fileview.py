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

print "SBTCVM FileView file browser. v1.3"
pygame.display.init()
pygame.font.init()
pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN])

pathlist=list()

windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fileview64.png'))
pygame.display.set_icon(windowicon)

class fileclick:
	def __init__(self, box, filename, ftype):
		self.box=box
		self.filename=filename
		self.ftype=ftype
screensurf=pygame.display.set_mode((800, 600))
#image data loading
filebg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fileview.jpg')).convert()
exitbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvquit.png')).convert()
helpbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvhelp.png')).convert()
fvstreg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvstreg.png')).convert()
fvtrom=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvtrom.png')).convert()
fvdir=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvdir.png')).convert()
fvup=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvup.png')).convert()
fvimg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvimg.png')).convert()
fvtext=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvtext.png')).convert()
fvtasm=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvtasm.png')).convert()
fvall=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvall.png')).convert()
fvlog=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvlog.png')).convert()
fvdmp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvdmp.png')).convert()
fvdummy=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvdummy.png')).convert()
fvrun=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvrun.png')).convert()
fvview=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvview.png')).convert()
fvswon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvsw-on.png')).convert_alpha()
fvswoff=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvsw-off.png')).convert_alpha()
#flag set to 1 when the program should quit.
quitflag=0
#fonts
simplefontC = pygame.font.SysFont(None, 22)
simplefontB = pygame.font.SysFont(None, 19)
#inital scroll offset.
listyoff=0
#icon x pos within gxmask
iconx=0
#label x pos within gxmask
labelx=48
#screen x position of gxmask "tiles"
maskx=0
#set inital filter to "all"
filterflg=0
filtertext="All"
#vertical jump between tiles (remember to account for tile size!)
yjump=42
#inital iterfiles state
iterfiles='.'
#used in event handler and drawing system. MAKE SURE THESE ARE THE SAME AS SCREEN SIZE!
screenx=800
screeny=600

runexec=0

pygame.display.set_caption(("fileview - " + iterfiles), ("fileview - " + iterfiles))
#blit fixed on-screen buttons to filebg.
quitx=filebg.blit(exitbtn, (708, 107))
ghelpx=filebg.blit(helpbtn, (749, 107))
fil0=filebg.blit(fvall, (430, 107))
fil1=filebg.blit(fvtrom, (471, 107))
fil2=filebg.blit(fvimg, (512, 107))
fil3=filebg.blit(fvstreg, (553, 107))
fil4=filebg.blit(fvtasm, (594, 107))
fil5=filebg.blit(fvtext, (635, 107))
#-----
runx=filebg.blit(fvrun, (708, 157))
viewx=filebg.blit(fvview, (749, 157))

fil6=filebg.blit(fvlog, (430, 157))
fil7=filebg.blit(fvdmp, (471, 157))
#unused
fil8=filebg.blit(fvdummy, (512, 157))
fil9=filebg.blit(fvdummy, (553, 157))
fil10=filebg.blit(fvdummy, (594, 157))
fil11=filebg.blit(fvdummy, (635, 157))

#draw switch off states to background, later draw over them on surface as needed.
filebg.blit(fvswoff, (430, 107))
filebg.blit(fvswoff, (471, 107))
filebg.blit(fvswoff, (512, 107))
filebg.blit(fvswoff, (553, 107))
filebg.blit(fvswoff, (594, 107))
filebg.blit(fvswoff, (635, 107))
filebg.blit(fvswoff, (708, 157))
filebg.blit(fvswoff, (749, 157))
filebg.blit(fvswoff, (430, 157))
filebg.blit(fvswoff, (471, 157))
#unused
#filebg.blit(fvswoff, (512, 157))
#filebg.blit(fvswoff, (553, 157))
#filebg.blit(fvswoff, (594, 157))
#filebg.blit(fvswoff, (635, 157))



fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
#set scupdate to one at start, so it will draw the screen on startup
#(screen updating is done only when what is shown would actually change)
scupdate=1
#create gxmask only once. just reuse it.
gxmask=pygame.Surface((410, 40))
while quitflag==0:
	#check to save needlessly redrawing display
	if scupdate==1:
		scupdate=0
		#blit background
		screensurf.blit(filebg, (0, 0))
		#set list vertical draw to listyoff offset. note that listy is used to blit gxmask
		listy=listyoff
		#reset list of fileclick objects.
		flist=list()
		if iterfiles!='.':
			textit=simplefontB.render("..", True, (0, 0, 0), (255, 255, 255))
			#gxmask=pygame.Surface((410, 40))
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
			#directory check
			if os.path.isdir(os.path.join(iterfiles, fname)):
				#if check to hide hidden git directory. 
				if not fname.endswith(".git"):
					textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
					#a small surface is used to create the "tiles" look of the file list. (it also simplifies the click areas to 1 per item)
					gxmask.fill((255, 255, 255))
					gxmask.blit(fvdir, (iconx, 0))
					gxmask.blit(textit, (labelx, 0))
					gx=screensurf.blit(gxmask, (maskx, listy))
					#filecheck class works as such: (pygame box, base filename, filetype string)
					qx=fileclick(gx, fname, "dir")
					fileval=1
			elif fnamelo.endswith(("." + "trom")) and (filterflg==0 or filterflg==1): 
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				#gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvtrom, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "trom")
				fileval=1
			elif (fnamelo.endswith(("." + "png")) or fnamelo.endswith(("." + "jpg")) or fnamelo.endswith(("." + "jpeg")) or fnamelo.endswith(("." + "gif"))) and (filterflg==0 or filterflg==2):
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				#gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvimg, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "img")
				fileval=1
			elif fnamelo.endswith(("." + "streg")) and (filterflg==0 or filterflg==3) : 
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				#gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvstreg, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "streg")
				fileval=1
			elif fnamelo.endswith(("." + "tasm")) and (filterflg==0 or filterflg==4) : 
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				#gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvtasm, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "tasm")
				fileval=1
			elif (fnamelo.endswith(("." + "txt")) or fnamelo.endswith(("." + "md"))) and (filterflg==0 or filterflg==5) : 
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				#gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvtext, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "text")
				fileval=1
			elif fnamelo.endswith(("." + "log")) and (filterflg==0 or filterflg==6) : 
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				#gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvlog, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "log")
				fileval=1
			elif fnamelo.endswith(("." + "dmp")) and (filterflg==0 or filterflg==7) : 
				textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
				#gxmask=pygame.Surface((410, 40))
				gxmask.fill((255, 255, 255))
				gxmask.blit(fvdmp, (iconx, 0))
				gxmask.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask, (maskx, listy))
				qx=fileclick(gx, fname, "dmp")
				fileval=1
			if fileval==1:
				flist.extend([qx])
				listy += yjump
			#break from file iteration when future gxmask tiles would be completely off-screen.
			if listy>screeny:
				break
		if filterflg==0:
			screensurf.blit(fvswon, (430, 107))
		elif filterflg==1:
			screensurf.blit(fvswon, (471, 107))
		elif filterflg==2:
			screensurf.blit(fvswon, (512, 107))
		elif filterflg==3:
			screensurf.blit(fvswon, (553, 107))
		elif filterflg==4:
			screensurf.blit(fvswon, (594, 107))
		elif filterflg==5:
			screensurf.blit(fvswon, (635, 107))
		elif filterflg==6:
			screensurf.blit(fvswon, (430, 157))
		elif filterflg==7:
			screensurf.blit(fvswon, (471, 157))
		if runexec==0:
			screensurf.blit(fvswon, (708, 157))
		elif runexec==1:
			screensurf.blit(fvswon, (749, 157))
		#draw path and filter status
		menulabel=simplefontC.render(("path: " + iterfiles), True, (0, 0, 0))
		screensurf.blit(menulabel, (430, 70))
		#screensurf.blit(fillabel, (430, 88))
		pygame.display.update()
	time.sleep(0.05)
	
	#event handler
	for event in pygame.event.get():
		if event.type == QUIT:
			quitflag=1
			break
		if event.type == KEYDOWN and event.key == K_F1:
			subprocess.Popen(["python", "helpview.py", "fileview.xml"])
		if event.type == KEYDOWN and event.key == K_F8:
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-fileview.png')))
			break
		if event.type==MOUSEBUTTONDOWN:
			#onscreen button handler (blitted to background image during startup)
			if quitx.collidepoint(event.pos)==1 and event.button==1:
				quitflag=1
				break
			#help button
			if ghelpx.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "helpview.py", "fileview.xml"])
			if runx.collidepoint(event.pos)==1 and event.button==1:
				runexec=0
				scupdate=1
			if viewx.collidepoint(event.pos)==1 and event.button==1:
				runexec=1
				scupdate=1
			#filter buttons
			if fil0.collidepoint(event.pos)==1 and event.button==1:
				filterflg=0
				filtertext="All"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
				listyoff=0
			if fil1.collidepoint(event.pos)==1 and event.button==1:
				filterflg=1
				filtertext="TROM"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
				listyoff=0
			if fil2.collidepoint(event.pos)==1 and event.button==1:
				filterflg=2
				filtertext="Image"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
				listyoff=0
			if fil3.collidepoint(event.pos)==1 and event.button==1:
				filterflg=3
				filtertext="STREG"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
				listyoff=0
			if fil4.collidepoint(event.pos)==1 and event.button==1:
				filterflg=4
				filtertext="TASM"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
				listyoff=0
			if fil5.collidepoint(event.pos)==1 and event.button==1:
				filterflg=5
				filtertext="Text"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
				listyoff=0
			if fil6.collidepoint(event.pos)==1 and event.button==1:
				filterflg=6
				filtertext="log"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
				listyoff=0
			if fil7.collidepoint(event.pos)==1 and event.button==1:
				filterflg=7
				filtertext="Mem Dump"
				fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
				scupdate=1
				listyoff=0
			#filelist clickbox checker.
			for f in flist:
				if f.box.collidepoint(event.pos)==1 and event.button==1:
					#program launchers
					if runexec==0:
						if f.ftype=="trom":
							subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfiles, f.filename))])
						if f.ftype=="streg":
							subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfiles, f.filename))])
					else:
						if f.ftype=="trom":
							subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfiles, f.filename))])
						if f.ftype=="streg":
							subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="tasm":
						subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="log":
						subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="dmp":
						subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfiles, f.filename))])
					
					if f.ftype=="img":
						subprocess.Popen(["python", "MK2-TOOLS.py", "imgview", (os.path.join(iterfiles, f.filename))])
					if f.ftype=="text":
						subprocess.Popen(["python", "MK2-TOOLS.py", "textview", (os.path.join(iterfiles, f.filename))])
					#special directory handler
					if f.ftype=="dir":
						listyoff=0
						scupdate=1
						#home directory (SBTCVM's repository root directory)
						if f.filename=='.':
							pathlist=list()
							iterfiles='.'
						#previous directory
						if f.filename=='..':
							pathlist.remove(pathlist[(len(pathlist) -1)])
							if pathlist==list():
								iterfiles='.'
							else:
								iterfiles=os.path.join(*pathlist)
						#if normal subdirectory, add it to end of pathlist
						else:
							pathlist.extend([f.filename])
							iterfiles=os.path.join(*pathlist)
						pygame.display.set_caption(("fileview - " + iterfiles), ("fileview - " + iterfiles))
						break
				#scroll wheel handling
				if event.button==4:
					if listyoff<0:
						listyoff += yjump
						scupdate=1
					break
					
				if event.button==5:
					if listy>screeny:
						listyoff -= yjump
						scupdate=1
					if listyoff>0:
						listyoff=0
						scupdate=1
					break
			