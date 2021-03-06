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
import VMSYSTEM.libthemeconf as libthemeconf
import VMSYSTEM.libfilevirtual as libfilevirtual

from pygame.locals import *

print "SBTCVM FileView file browser. v2.0"
pygame.display.init()
pygame.font.init()
pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN])

pathlist=["."]
pathlist2=["."]
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
vmui.initui(screensurf, 1)
#image data loading

#filehud=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fileviewhud.png')).convert_alpha()
#filehud=pygame.Surface((screenx, screeny), SRCALPHA)


fvbadge=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvbadge.png')).convert_alpha()
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

panefilter1=vmui.makerotbtn("Pane 1", "Filter")
panefilter2=vmui.makerotbtn("Pane 2", "Filter")
#fvfilemenu=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvfilemenu.png')).convert()
fmicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'filemenuicon.png')).convert_alpha()
fvfilemenu=vmui.makemenubtn("FILE", icon=fmicon)

#fvrunsw=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvrunsw.png')).convert()
#fvviewsw=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvviewsw.png')).convert()
fvrunview=vmui.makeswitchbtn("RUN", "VIEW")
fvrunsw=fvrunview[0]
fvviewsw=fvrunview[1]

#fvpane1=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvpane1.png')).convert()
#fvpane2=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX', "fv"), 'fvpane2.png')).convert()

fvpane=vmui.makeswitchbtn("1 PANE", "2 PANE")
fvpane1=fvpane[0]
fvpane2=fvpane[1]


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
hudfont = pygame.font.SysFont(None, 19)
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
filterflg2=0
filtertext="All"
#vertical jump between tiles (remember to account for tile size!)
yjump=42
#inital iterfiles state
iterfiles='.'
iterfiles2='.'
#used in event handler and drawing system. MAKE SURE THESE ARE THE SAME AS SCREEN SIZE!
screenx=420
screeny=600

runexec=0

pygame.display.set_caption(("fileview - " + iterfiles), ("fileview - " + iterfiles))
#blit fixed on-screen buttons to filebg.

#ghelpx=filebg.blit(helpbtn, (44, 5))
#gneww=filebg.blit(newbtn, (85, 5))
#runx=filebg.blit(fvrun, (136, 5))
#viewx=filebg.blit(fvview, (177, 5))

#filebg=(libthemeconf.bgmake(filehud)).convert()
filebg=(libthemeconf.bgmake(None)).convert()
panemode=1

listy2=0

fillabel=simplefontC.render(("Type Filter: " + filtertext), True, (0, 0, 0))
#set scupdate to one at start, so it will draw the screen on startup
#(screen updating is done only when what is shown would actually change)
scupdate=1


#filemenu
fmnew=vmui.menuitem("New Window", "NEW")
fmhelp=vmui.menuitem("Help (F1)", "HELP")
fmabout=vmui.menuitem("About Fileview", "ABOUT")
fmbg=vmui.menuitem("Background", "SETBG")
fmquit=vmui.menuitem("Quit", "QUIT")
filemenu=[fmnew, fmhelp, fmabout, fmbg, fmquit]


#create gxmask only once. just reuse it.

menuitrun=vmui.menuitem("Run", "RUN")
menuitasm=vmui.menuitem("Assemble", "RUN")
menuitview=vmui.menuitem("View", "VIEW")
menuitinfo=vmui.menuitem("Info", "INFO")
menuittrom=vmui.menuitem("Trom file", "TROM", noclick=1, icon=fvtrom)
menuitstreg=vmui.menuitem("Streg file", "TROM", noclick=1, icon=fvstreg)
menuitimage=vmui.menuitem("Image file", "TROM", noclick=1, icon=fvimg)
menuittasm=vmui.menuitem("Tasm file", "TROM", noclick=1, icon=fvtasm)
menuittext=vmui.menuitem("Text file", "TROM", noclick=1, icon=fvtext)
menuitlog=vmui.menuitem("Log file", "TROM", noclick=1, icon=fvlog)
menuitdmp=vmui.menuitem("Dmp file", "TROM", noclick=1, icon=fvdmp)
fil0=vmui.menuitem("All", 0, icon=fvall)
fil1=vmui.menuitem("Trom", 1, icon=fvtrom)
fil2=vmui.menuitem("Image", 2, icon=fvimg)
fil3=vmui.menuitem("Streg", 3, icon=fvstreg)
fil4=vmui.menuitem("Tasm", 4, icon=fvtasm)
fil5=vmui.menuitem("Text", 5, icon=fvtext)
fil6=vmui.menuitem("Log", 6, icon=fvlog)
fil7=vmui.menuitem("Dmp", 7, icon=fvdmp)

filtermenu=[fil0, fil1, fil2, fil3, fil4, fil5, fil6, fil7]
iconlist=[fvall, fvtrom, fvimg, fvstreg, fvtasm, fvtext, fvlog, fvdmp]


#right click menus:
trommenu=[menuittrom, menuitrun, menuitview, menuitinfo]
stregmenu=[menuitstreg, menuitrun, menuitview, menuitinfo]
imgmenu=[menuitimage, menuitview, menuitinfo]
tasmmenu=[menuittasm, menuitasm, menuitview, menuitinfo]
textmenu=[menuittext, menuitview, menuitinfo]
logmenu=[menuitlog, menuitview, menuitinfo]
dmpmenu=[menuitdmp, menuitview, menuitinfo]

tromdesc="""SBTCVM Balanced Ternary ROM image."""
stregdesc="""Sbtcvm TRom Ececute Group
configuration file."""
imagedesc="""image filetype that SBTCVM's
image viewer can show."""
tasmdesc="""SBTCVM assembly source file."""
textdesc="""plain text file"""
logdesc="""SBTCVM log file."""
dmpdesc="""SBTCVM Virtualized Memory Dump"""

diagabt="""Fileview v2.0
Part of the SBTCVM Project
Copyright (c) 2016-2018 Thomas Leathers and Contributors 

See README.md for more information."""

def getdesc(filetype, fname, path):
	if filetype=="trom":
		return (fname + "\n-" + "\n" + tromdesc)
	if filetype=="streg":
		return (fname + "\n-" + "\n" + stregdesc)
	if filetype=="img":
		return (fname + "\n-" + "\n" + imagedesc)
	if filetype=="text":
		return (fname + "\n-" + "\n" + textdesc)
	if filetype=="tasm":
		return (fname + "\n-" + "\n" + tasmdesc)
	if filetype=="log":
		return (fname + "\n-" + "\n" + logdesc)
	if filetype=="dmp":
		return (fname + "\n-" + "\n" + dmpdesc)


hudupdate=1
#pane1upt=1
#pane1upt=1

tilebgcolor=libthemeconf.tilecolor

gxmask=pygame.Surface((410, 40), SRCALPHA)
gxmask2=pygame.Surface((390, 40), SRCALPHA)
box1rect=pygame.Rect(433, 17, 349, 23)
box2rect=pygame.Rect(433, 71, 349, 23)
engtimer=pygame.time.Clock()
updint=30
updcnt=0
while quitflag==0:
	#update dispay once every 30 frames
	if updcnt==updint:
		updcnt=0
		scupdate=1
	else:
		updcnt+=1
	#check to save needlessly redrawing display
	if scupdate==1:
		scupdate=0
		#blit background
		screensurf.blit(filebg, (0, 0))
		panerect=pygame.Rect(0, 109, screenx, (screeny-109))
		uptlist=[panerect]
		if hudupdate==1:
			hudrect=pygame.Rect(0, 0, screenx, 109)
			
			filehud=pygame.Surface((screenx, screeny), SRCALPHA).convert_alpha()
			pygame.draw.rect(filehud, libthemeconf.hudbg, hudrect, 0)
			pygame.draw.rect(filehud, libthemeconf.textboxbg, box1rect, 0)
			pygame.draw.rect(filehud, libthemeconf.textboxline, box1rect, 1)
			pygame.draw.rect(filehud, libthemeconf.textboxbg, box2rect, 0)
			pygame.draw.rect(filehud, libthemeconf.textboxline, box2rect, 1)
			pygame.draw.line(filehud, libthemeconf.huddiv, (420, 0), (420, screeny), 2)
			pygame.draw.line(filehud, libthemeconf.huddiv, (420, 50), (screenx, 50), 2)
			filemenux=filehud.blit(fvfilemenu, (3, 5))
			filp1=filehud.blit(panefilter1, (2, 56))
			filp2=filehud.blit(panefilter2, (94, 56))
			filehud.blit(fvbadge, (338, 14))
			hudt=hudfont.render("Fileview", True, libthemeconf.hudtext)
			filehud.blit(hudt, (340, 88))
			hudt2=hudfont.render("Pane 1", True, libthemeconf.hudtext)
			filehud.blit(hudt2, (433, 1))
			hudt3=hudfont.render("Pane 2", True, libthemeconf.hudtext)
			filehud.blit(hudt3, (433, 56))
		#set list vertical draw to listyoff offset. note that listy is used to blit gxmask
		listy=listyoff
		#reset list of fileclick objects.
		flist=list()
		for fname in libfilevirtual.diriterate(pathlist):
			fnamelo=fname.lower()
			fileval=0
			#directory check
			if libfilevirtual.isdir(fname, pathlist):
				if listy<listydef or listy>screeny:
					fileval=2
				else:
					textit=simplefontB.render(fname, True, libthemeconf.tiletext)
					#a small surface is used to create the "tiles" look of the file list. (it also simplifies the click areas to 1 per item)
					gxmask.fill(tilebgcolor)
					if fname=="..":
						gxmask.blit(fvup, (iconx, 0))
					else:
						gxmask.blit(fvdir, (iconx, 0))
					gxmask.blit(textit, (labelx, 0))
					gx=screensurf.blit(gxmask, (maskx, listy))
					#filecheck class works as such: (pygame box, base filename, filetype string)
					qx=fileclick(gx, fname, "dir")
					fileval=1
			for typ in typelist:
				if fnamelo.endswith(("." + typ.ext)) and (filterflg==0 or filterflg==typ.filterflg): 
					if listy<listydef or listy>screeny:
						fileval=2
						break
					else:
						textit=simplefontB.render(fname, True, libthemeconf.tiletext)
						#gxmask=pygame.Surface((410, 40))
						gxmask.fill(tilebgcolor)
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
			for fname in libfilevirtual.diriterate(pathlist2):
				fnamelo=fname.lower()
				fileval=0
				#directory check
				if libfilevirtual.isdir(fname, pathlist2):
					if listy2<listydef2 or listy2>screeny:
						fileval=2
					else:
						textit=simplefontB.render(fname, True, libthemeconf.tiletext)
						#a small surface is used to create the "tiles" look of the file list. (it also simplifies the click areas to 1 per item)
						gxmask2.fill(tilebgcolor)
						if fname=="..":
							gxmask2.blit(fvup, (iconx, 0))
						else:
							gxmask2.blit(fvdir, (iconx, 0))
						gxmask2.blit(textit, (labelx, 0))
						gx=screensurf.blit(gxmask2, (maskx2, listy2))
						#filecheck class works as such: (pygame box, base filename, filetype string)
						qx=fileclick(gx, fname, "dir", 2)
						fileval=1
				for typ in typelist:
					if fnamelo.endswith(("." + typ.ext)) and (filterflg2==0 or filterflg2==typ.filterflg): 
						if listy2<listydef2 or listy2>screeny:
							fileval=2
							break
						else:
							textit=simplefontB.render(fname, True, libthemeconf.tiletext)
							#gxmask=pygame.Surface((410, 40))
							gxmask2.fill(tilebgcolor)
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
		
		#draw paths and add hud rect to update list if needed.
		if panemode==2 and hudupdate==1:
			uptlist.extend([hudrect])
			hudupdate==0
			menulabel=simplefontC.render(("path: " + iterfiles), True, libthemeconf.textboxtext)
			filehud.blit(menulabel, (435, 20))
			menulabel2=simplefontC.render(("path: " + iterfiles2), True, libthemeconf.textboxtext)
			filehud.blit(menulabel2, (435, 74))
			screensurf.blit(filehud, (0, 0))
		elif hudupdate==1:
			hudupdate==0
			uptlist.extend([hudrect])
			screensurf.blit(filehud, (0, 0))
		#pane mode and run/view mode switches:
		if panemode==1:
			panex=screensurf.blit(fvpane1, (89, 5))
		else:
			panex=screensurf.blit(fvpane2, (89, 5))
		if runexec==0:
			runviewx=screensurf.blit(fvrunsw, (46, 5))
		else:
			runviewx=screensurf.blit(fvviewsw, (46, 5))
		screensurf.blit(iconlist[filterflg], (43, 57))
		screensurf.blit(iconlist[filterflg2], (135, 57))
		pygame.display.update(uptlist)
	#time.sleep(0.05)
	engtimer.tick(30)
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
				
			#help button
			
			if filemenux.collidepoint(event.pos)==1 and event.button==1:
				menuret=vmui.menuset(filemenu, 3, 45, reclick=0, fontsize=26)
				if menuret=="HELP":
					subprocess.Popen(["python", "helpview.py", "fileview.xml"])
				if menuret=="QUIT":
					quitflag=1
					break
				if menuret=="ABOUT":
					if panemode==2:
						vmui.aboutdiag(diagabt, (screenx // 2), (screeny // 2))
					else:
						vmui.okdiag(diagabt, (screenx // 2), (screeny // 2))
				if menuret=="SETBG":
					vmui.settheme(3, 45)
					scupdate=1
					filebg=(libthemeconf.bgmake(filehud)).convert()
				if menuret=="NEW":
					subprocess.Popen(["python", "fileview2.py"])
			if panex.collidepoint(event.pos)==1 and event.button==1:
				if panemode==1:
					panemode=2
					screensurf=pygame.display.set_mode((800, 600))
					scupdate=1
					screenx=800
					screeny=600
					hudupdate=1
				else:
					panemode=1
					screensurf=pygame.display.set_mode((420, 600))
					scupdate=1
					screenx=420
					screeny=600
					hudupdate=1
			if runviewx.collidepoint(event.pos)==1 and event.button==1:
				if runexec==1:
					runexec=0
				else:
					runexec=1
				scupdate=1
				hudupdate=1
			#if gneww.collidepoint(event.pos)==1 and event.button==1:
			#	subprocess.Popen(["python", "fileview2.py"])
			#if runx.collidepoint(event.pos)==1 and event.button==1:
			#	runexec=0
			#	scupdate=1
			#if viewx.collidepoint(event.pos)==1 and event.button==1:
			#	runexec=1
			#	scupdate=1
			if filp1.collidepoint(event.pos)==1 and event.button==1:
				filterbak=filterflg
				filterflg=vmui.menuset(filtermenu, 3, 97, reclick=0)
				if filterflg==None:
					filterflg=filterbak
				else:
					listyoff=110
				scupdate=1
				hudupdate=1
			if filp2.collidepoint(event.pos)==1 and event.button==1:
				filterbak=filterflg2
				filterflg2=vmui.menuset(filtermenu, 95, 97, reclick=0)
				if filterflg2==None:
					filterflg2=filterbak
				else:
					listyoff2=110
				scupdate=1
				hudupdate=1
			#filelist clickbox checker.
			for f in flist:
				if f.pane==1:
					iterfilesq=iterfiles
				else:
					iterfilesq=iterfiles2
				if f.box.collidepoint(event.pos)==1 and event.button==3:
					if f.ftype=="trom":
						menuret=vmui.menuset(trommenu, event.pos[0], event.pos[1], reclick=0, fontsize=25)
						if menuret=="RUN":
							subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfilesq, f.filename))])
						if menuret=="VIEW":
							subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfilesq, f.filename))])
						if menuret=="INFO":
							vmui.okdiag(getdesc("trom", f.filename, iterfilesq), (screenx // 2), (screeny // 2))
					if f.ftype=="streg":
						menuret=vmui.menuset(stregmenu, event.pos[0], event.pos[1], reclick=0, fontsize=25)
						if menuret=="RUN":
							subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfilesq, f.filename))])
						if menuret=="VIEW":
							subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfilesq, f.filename))])
						if menuret=="INFO":
							vmui.okdiag(getdesc("streg", f.filename, iterfilesq), (screenx // 2), (screeny // 2))
					if f.ftype=="tasm":
						menuret=vmui.menuset(tasmmenu, event.pos[0], event.pos[1], reclick=0, fontsize=25)
						if menuret=="RUN":
							subprocess.Popen(["python", "MK2-TOOLS.py", "guiasm", (os.path.join(iterfilesq, f.filename))])
						if menuret=="VIEW":
							subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfilesq, f.filename))])
						if menuret=="INFO":
							vmui.okdiag(getdesc("tasm", f.filename, iterfilesq), (screenx // 2), (screeny // 2))
					if f.ftype=="log":
						menuret=vmui.menuset(logmenu, event.pos[0], event.pos[1], reclick=0, fontsize=25)
						if menuret=="VIEW":
							subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfilesq, f.filename))])
						if menuret=="INFO":
							vmui.okdiag(getdesc("log", f.filename, iterfilesq), (screenx // 2), (screeny // 2))
					if f.ftype=="dmp":
						menuret=vmui.menuset(dmpmenu, event.pos[0], event.pos[1], reclick=0, fontsize=25)
						if menuret=="VIEW":
							subprocess.Popen(["python", "MK2-TOOLS.py", "codeview", (os.path.join(iterfilesq, f.filename))])
						if menuret=="INFO":
							vmui.okdiag(getdesc("dmp", f.filename, iterfilesq), (screenx // 2), (screeny // 2))
					if f.ftype=="img":
						menuret=vmui.menuset(imgmenu, event.pos[0], event.pos[1], reclick=0, fontsize=25)
						if menuret=="VIEW":
							subprocess.Popen(["python", "MK2-TOOLS.py", "imgview", (os.path.join(iterfilesq, f.filename))])
						if menuret=="INFO":
							vmui.okdiag(getdesc("img", f.filename, iterfilesq), (screenx // 2), (screeny // 2))
					if f.ftype=="text":
						menuret=vmui.menuset(textmenu, event.pos[0], event.pos[1], reclick=0, fontsize=25)
						if menuret=="VIEW":
							subprocess.Popen(["python", "MK2-TOOLS.py", "textview", (os.path.join(iterfilesq, f.filename))])
						if menuret=="INFO":
							vmui.okdiag(getdesc("text", f.filename, iterfilesq), (screenx // 2), (screeny // 2))
				if f.box.collidepoint(event.pos)==1 and event.button==1:
					#program launchers
					if runexec==0:
						if f.ftype=="trom":
							subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfilesq, f.filename))])
						if f.ftype=="streg":
							subprocess.Popen(["python", "MK2-RUN.py", (os.path.join(iterfilesq, f.filename))])
						if f.ftype=="tasm":
							subprocess.Popen(["python", "MK2-TOOLS.py", "guiasm", (os.path.join(iterfilesq, f.filename))])
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
						hudupdate=1
						if f.pane==1:
							listyoff=110
							scupdate=1
							pathlist=libfilevirtual.dir_cd(pathlist, f.filename)
							iterfiles=os.path.join(*pathlist)
							pygame.display.set_caption(("fileview - " + iterfiles), ("fileview - " + iterfiles))
							break
						else:
							listyoff2=110
							scupdate=1
							pathlist2=libfilevirtual.dir_cd(pathlist2, f.filename)
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
			