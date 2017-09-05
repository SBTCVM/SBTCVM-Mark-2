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

print "SBTCVM FileView file browser. v2.0"
pygame.display.init()
pygame.font.init()
pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN])

pathlist=list()
pathlist2=list()
windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fileview64.png'))
pygame.display.set_icon(windowicon)

class fileclick:
	def __init__(self, box, filename, ftype, pane=1):
		self.box=box
		self.filename=filename
		self.ftype=ftype
		self.pane=pane
class filetyp:
	def __init__(self, ext, typeicon, qxtype, filterflg):
		self.ext=ext
		self.typeicon=typeicon
		self.qxtype=qxtype
		self.filterflg=filterflg

screensurf=pygame.display.set_mode((420, 600))
#image data loading
filebg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fileview2.jpg')).convert()
exitbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvquit.png')).convert()
helpbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvhelp.png')).convert()
newbtn=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvneww.png')).convert()
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
fvpane1=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvpane1.png')).convert()
fvpane2=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvpane2.png')).convert()
#definitions of all non-directory file types...
typ_png=filetyp("png", fvimg, "img", 2)
typ_jpg=filetyp("jpg", fvimg, "img", 2)
typ_jpeg=filetyp("jpeg", fvimg, "img", 2)
typ_gif=filetyp("gif", fvimg, "img", 2)
typ_streg=filetyp("streg", fvstreg, "streg", 3)
typ_trom=filetyp("trom", fvtrom, "trom", 1)
typ_tasm=filetyp("tasm", fvtasm, "tasm", 4)
typ_txt=filetyp("txt", fvtext, "text", 5)
typ_md=filetyp("md", fvtext, "text", 5)
typ_log=filetyp("log", fvlog, "log", 6)
typ_dmp=filetyp("dmp", fvdmp, "dmp", 7)
typelist=[typ_png, typ_jpg, typ_jpeg, typ_gif, typ_streg, typ_trom, typ_tasm, typ_txt, typ_md, typ_log, typ_dmp]




#flag set to 1 when the program should quit.
quitflag=0
#fonts
simplefontC = pygame.font.SysFont(None, 22)
simplefontB = pygame.font.SysFont(None, 19)
#inital scroll offset.
listyoff=110
listyoff2=110
listydef=listyoff
listydef2=listyoff2
#icon x pos within gxmask
iconx=0
#label x pos within gxmask
labelx=48
#screen x position of gxmask "tiles"
maskx=0
maskx2=423
#set inital filter to "all"
filterflg=0
filtertext="All"
#vertical jump between tiles (remember to account for tile size!)
yjump=42
#inital iterfiles state
iterfiles='.'
iterfiles2='.'
#used in event handler and drawing system. MAKE SURE THESE ARE THE SAME AS SCREEN SIZE!
screenx=800
screeny=600

runexec=0

pygame.display.set_caption(("fileview - " + iterfiles), ("fileview - " + iterfiles))
#blit fixed on-screen buttons to filebg.
quitx=filebg.blit(exitbtn, (3, 5))
ghelpx=filebg.blit(helpbtn, (44, 5))
gneww=filebg.blit(newbtn, (85, 5))
runx=filebg.blit(fvrun, (136, 5))
viewx=filebg.blit(fvview, (177, 5))

fil0=filebg.blit(fvall, (3, 57))
fil1=filebg.blit(fvtrom, (44, 57))
fil2=filebg.blit(fvimg, (85, 57))
fil3=filebg.blit(fvstreg, (126, 57))
fil4=filebg.blit(fvtasm, (167, 57))
fil5=filebg.blit(fvtext, (208, 57))
fil6=filebg.blit(fvlog, (249, 57))
fil7=filebg.blit(fvdmp, (290, 57))
#unused
#fil8=filebg.blit(fvdummy, (512, 5))
#fil9=filebg.blit(fvdummy, (553, 5))
#fil10=filebg.blit(fvdummy, (594, 5))
#fil11=filebg.blit(fvdummy, (635, 5))

#draw switch off states to background, later draw over them on surface as needed.
filebg.blit(fvswoff, (3, 57))
filebg.blit(fvswoff, (44, 57))
filebg.blit(fvswoff, (85, 57))
filebg.blit(fvswoff, (126, 57))
filebg.blit(fvswoff, (167, 57))
filebg.blit(fvswoff, (208, 57))
filebg.blit(fvswoff, (249, 57))
filebg.blit(fvswoff, (290, 57))
filebg.blit(fvswoff, (136, 5))
filebg.blit(fvswoff, (177, 5))
#unused
#filebg.blit(fvswoff, (512, 157))
#filebg.blit(fvswoff, (553, 157))
#filebg.blit(fvswoff, (594, 157))
#filebg.blit(fvswoff, (635, 157))

panemode=1

listy2=0

fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
#set scupdate to one at start, so it will draw the screen on startup
#(screen updating is done only when what is shown would actually change)
scupdate=1
#create gxmask only once. just reuse it.
gxmask=pygame.Surface((410, 40))
gxmask2=pygame.Surface((390, 40))
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
		if iterfiles!='.' and listy>=listydef:
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
					if listy<listydef:
						fileval=2
					else:
						textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
						#a small surface is used to create the "tiles" look of the file list. (it also simplifies the click areas to 1 per item)
						gxmask.fill((255, 255, 255))
						gxmask.blit(fvdir, (iconx, 0))
						gxmask.blit(textit, (labelx, 0))
						gx=screensurf.blit(gxmask, (maskx, listy))
						#filecheck class works as such: (pygame box, base filename, filetype string)
						qx=fileclick(gx, fname, "dir")
						fileval=1
			for typ in typelist:
				if fnamelo.endswith(("." + typ.ext)) and (filterflg==0 or filterflg==typ.filterflg): 
					if listy<listydef:
						fileval=2
						break
					else:
						textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
						#gxmask=pygame.Surface((410, 40))
						gxmask.fill((255, 255, 255))
						gxmask.blit(typ.typeicon, (iconx, 0))
						gxmask.blit(textit, (labelx, 0))
						gx=screensurf.blit(gxmask, (maskx, listy))
						qx=fileclick(gx, fname, typ.qxtype)
						fileval=1
						break
			if fileval==1:
				flist.extend([qx])
				listy += yjump
			if fileval==2:
				listy += yjump
			#break from file iteration when future gxmask tiles would be completely off-screen.
			#if listy>screeny:
				#break
		if panemode==2:
			listy2=listyoff2
			#reset list of fileclick objects.
			if iterfiles2!='.' and listy2>=listydef2:
				textit=simplefontB.render("..", True, (0, 0, 0), (255, 255, 255))
				#gxmask=pygame.Surface((410, 40))
				gxmask2.fill((255, 255, 255))
				gxmask2.blit(fvup, (iconx, 0))
				gxmask2.blit(textit, (labelx, 0))
				gx=screensurf.blit(gxmask2, (maskx2, listy2))
				qx=fileclick(gx, "..", "dir", 2)
				flist.extend([qx])
				listy2 += yjump
			for fname in sorted(os.listdir(iterfiles2), key=str.lower):
				fnamelo=fname.lower()
				fileval=0
				#directory check
				if os.path.isdir(os.path.join(iterfiles2, fname)):
					#if check to hide hidden git directory. 
					if not fname.endswith(".git"):
						if listy2<listydef2:
							fileval=2
						else:
							textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
							#a small surface is used to create the "tiles" look of the file list. (it also simplifies the click areas to 1 per item)
							gxmask2.fill((255, 255, 255))
							gxmask2.blit(fvdir, (iconx, 0))
							gxmask2.blit(textit, (labelx, 0))
							gx=screensurf.blit(gxmask2, (maskx2, listy2))
							#filecheck class works as such: (pygame box, base filename, filetype string)
							qx=fileclick(gx, fname, "dir", 2)
							fileval=1
				for typ in typelist:
					if fnamelo.endswith(("." + typ.ext)) and (filterflg==0 or filterflg==typ.filterflg): 
						if listy2<listydef2:
							fileval=2
							break
						else:
							textit=simplefontB.render(fname, True, (0, 0, 0), (255, 255, 255))
							#gxmask=pygame.Surface((410, 40))
							gxmask2.fill((255, 255, 255))
							gxmask2.blit(typ.typeicon, (iconx, 0))
							gxmask2.blit(textit, (labelx, 0))
							gx=screensurf.blit(gxmask2, (maskx2, listy2))
							qx=fileclick(gx, fname, typ.qxtype, 2)
							fileval=1
							break
				if fileval==1:
					flist.extend([qx])
					listy2 += yjump
				if fileval==2:
					listy2 += yjump
				#break from file iteration when future gxmask tiles would be completely off-screen.
				if listy2>screeny:
					break
		if panemode==1:
			panex=screensurf.blit(fvpane1, (225, 5))
		else:
			panex=screensurf.blit(fvpane2, (225, 5))
		if filterflg==0:
			screensurf.blit(fvswon, (3, 57))
		elif filterflg==1:
			screensurf.blit(fvswon, (44, 57))
		elif filterflg==2:
			screensurf.blit(fvswon, (85, 57))
		elif filterflg==3:
			screensurf.blit(fvswon, (126, 57))
		elif filterflg==4:
			screensurf.blit(fvswon, (167, 57))
		elif filterflg==5:
			screensurf.blit(fvswon, (208, 57))
		elif filterflg==6:
			screensurf.blit(fvswon, (249, 57))
		elif filterflg==7:
			screensurf.blit(fvswon, (290, 57))
		if runexec==0:
			screensurf.blit(fvswon, (136, 5))
		elif runexec==1:
			screensurf.blit(fvswon, (177, 5))
		#draw path and filter status
		if panemode==2:
			menulabel=simplefontC.render(("path: " + iterfiles), True, (0, 0, 0))
			screensurf.blit(menulabel, (435, 20))
			menulabel2=simplefontC.render(("path: " + iterfiles2), True, (0, 0, 0))
			screensurf.blit(menulabel2, (435, 74))
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
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-fileview2.png')))
			break
		if event.type==MOUSEBUTTONDOWN:
			#onscreen button handler (blitted to background image during startup)
			if quitx.collidepoint(event.pos)==1 and event.button==1:
				quitflag=1
				break
			#help button
			if ghelpx.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "helpview.py", "fileview.xml"])
			if panex.collidepoint(event.pos)==1 and event.button==1:
				if panemode==1:
					panemode=2
					screensurf=pygame.display.set_mode((800, 600))
					scupdate=1
				else:
					panemode=1
					screensurf=pygame.display.set_mode((420, 600))
					scupdate=1
			if gneww.collidepoint(event.pos)==1 and event.button==1:
				subprocess.Popen(["python", "fileview2.py"])
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
				scupdate=1
				listyoff=110
				listyoff2=110
			if fil1.collidepoint(event.pos)==1 and event.button==1:
				filterflg=1
				filtertext="TROM"
				scupdate=1
				listyoff=110
				listyoff2=110
			if fil2.collidepoint(event.pos)==1 and event.button==1:
				filterflg=2
				filtertext="Image"
				scupdate=1
				listyoff=110
				listyoff2=110
			if fil3.collidepoint(event.pos)==1 and event.button==1:
				filterflg=3
				filtertext="STREG"
				scupdate=1
				listyoff=110
				listyoff2=110
			if fil4.collidepoint(event.pos)==1 and event.button==1:
				filterflg=4
				filtertext="TASM"
				scupdate=1
				listyoff=110
				listyoff2=110
			if fil5.collidepoint(event.pos)==1 and event.button==1:
				filterflg=5
				filtertext="Text"
				scupdate=1
				listyoff=110
				listyoff2=110
			if fil6.collidepoint(event.pos)==1 and event.button==1:
				filterflg=6
				filtertext="log"
				scupdate=1
				listyoff=110
				listyoff2=110
			if fil7.collidepoint(event.pos)==1 and event.button==1:
				filterflg=7
				filtertext="Mem Dump"
				scupdate=1
				listyoff=110
				listyoff2=110
			#filelist clickbox checker.
			for f in flist:
				if f.box.collidepoint(event.pos)==1 and event.button==1:
					#program launchers
					if f.pane==1:
						iterfilesq=iterfiles
					else:
						iterfilesq=iterfiles2
					if runexec==0:
						if f.ftype=="trom":
							subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfilesq, f.filename))])
						if f.ftype=="streg":
							subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfilesq, f.filename))])
					else:
						if f.ftype=="trom":
							subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfilesq, f.filename))])
						if f.ftype=="streg":
							subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfilesq, f.filename))])
					if f.ftype=="tasm":
						subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfilesq, f.filename))])
					if f.ftype=="log":
						subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfilesq, f.filename))])
					if f.ftype=="dmp":
						subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfilesq, f.filename))])
					
					if f.ftype=="img":
						subprocess.Popen(["python", "MK2-TOOLS.py", "imgview", (os.path.join(iterfilesq, f.filename))])
					if f.ftype=="text":
						subprocess.Popen(["python", "MK2-TOOLS.py", "textview", (os.path.join(iterfilesq, f.filename))])
					#special directory handler
					if f.ftype=="dir":
						if f.pane==1:
							listyoff=110
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
						else:
							listyoff2=110
							scupdate=1
							#home directory (SBTCVM's repository root directory)
							if f.filename=='.':
								pathlist2=list()
								iterfiles2='.'
							#previous directory
							if f.filename=='..':
								pathlist2.remove(pathlist2[(len(pathlist2) -1)])
								if pathlist2==list():
									iterfiles2='.'
								else:
									iterfiles2=os.path.join(*pathlist2)
							#if normal subdirectory, add it to end of pathlist
							else:
								pathlist2.extend([f.filename])
								iterfiles2=os.path.join(*pathlist2)
							#pygame.display.set_caption(("fileview - " + iterfiles), ("fileview - " + iterfiles))
							break
						
				#scroll wheel handling
				if event.button==4:
					if event.pos[1]>110:
						if (event.pos[0])<420 or panemode==1:
							if listyoff<110:
								listyoff += yjump
								scupdate=1
							break
						else:
							if listyoff2<110:
								listyoff2 += yjump
								scupdate=1
							break
				if event.button==5:
					if event.pos[1]>110:
						if (event.pos[0])<420 or panemode==1:
							if listy>screeny:
								listyoff -= yjump
								scupdate=1
							if listyoff>110:
								listyoff=110
								scupdate=1
							break
						else:
							if listy2>screeny:
								listyoff2 -= yjump
								scupdate=1
							if listyoff2>110:
								listyoff2=110
								scupdate=1
							break
			