#!/usr/bin/env python
import time
import os
import sys
import pygame
from pygame.locals import *
import VMSYSTEM.libvmconf as libvmconf
import xml.etree.ElementTree as ET


clicklist=list()

datapath=os.path.join("VMSYSTEM", "HELP")
pageref="helpindex.xml"

try:
	cmd=sys.argv[1]
except:
	cmd=None
if cmd=="-h" or cmd=="--help" or cmd=="help":
	print '''This is helpview.py, SBTCVM's integrated help system
commands:
MK2-RUN.py -h (--help) (help): this text
MK2-RUN.py -v (--version)    : version information.
MK2-RUN.py -a (--about)      : about MK2-RUN.py
MK2-RUN.py [pagexml]         : xml page to view (for use with context help)
'''
	sys.exit()
elif cmd=="-v" or cmd=="--version":
	print "SBTCVM MK2-TOOLS tool launcher v2.0.3"
	sys.exit()

elif cmd=="-a" or cmd=="--about":
	print '''#SBTCVM Mark 2 helpview


v2.0.3

Copyright (c) 2016-2017 Thomas Leathers and Contributors

  SBTCVM Mark 2 helpview is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Mark 2 helpview is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Mark 2 helpview. If not, see <http://www.gnu.org/licenses/>
'''
	sys.exit()
elif cmd!=None:
	pageref=cmd


pygame.display.init()
pygame.font.init()
filedict={}

def filelookup(filename):
	global filedict
	if filename in filedict:
		return filedict[filename]
	else:
		if (filename.lower()).endswith(".jpg") or (filename.lower()).endswith(".jpeg") or (filename.lower()).startswith("no-tr"):
			imgret=pygame.image.load(os.path.join(datapath, filename)).convert()
		else:
			imgret=pygame.image.load(os.path.join(datapath, filename)).convert_alpha()
		filedict[filename]=imgret
		return imgret


class clicktab:
	def __init__(self, box, link):
		self.box=box
		self.link=link

windowicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'helpicon.png'))
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((648, 486), pygame.RESIZABLE)
logooverlay=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'helpbgover.png')).convert_alpha()
iconhelp=pygame.image.load(os.path.join(datapath, 'iconhelp.png')).convert()
iconindex=pygame.image.load(os.path.join(datapath, 'iconindex.png')).convert()
iconquit=pygame.image.load(os.path.join(datapath, 'iconquit.png')).convert()

pygame.display.set_caption(("SBTCVM Help"), ("SBTCVM Help"))

textcol=(0, 0, 0)
bgcol=(210, 230, 255)
linkcol=(0, 0, 255)
screenh=486
screenw=648
yoff=0
xoff=5
yjump=22
fontsize=21
simplefont = pygame.font.SysFont(None, fontsize)
qflg=0
resizeflg=0
prevpage=None
scupdate=1
followmouse=0

pygame.key.set_repeat(250, 50)

while qflg==0:
	#handles resize operations when videoresize events are detected.
	if resizeflg==1:
		resizeflg=2	
	elif resizeflg==2:
		screensurf=pygame.display.set_mode((resw, resh), pygame.RESIZABLE)
		scupdate=1
		resizeflg=0	
		screenh=resh
		screenw=resw
	#Init page on startup and page change
	if pageref!=prevpage:
		prevpage=pageref
		tree = ET.parse(os.path.join(datapath, pageref))
		root = tree.getroot()
		headtag=root.find('head')
		pagename=headtag.attrib.get("title", "")
		pygame.display.set_caption(("SBTCVM Help - " + pagename), ("SBTCVM Help - " + pagename))
		screensurf.fill(bgcol)
		scupdate=1
		filedict={}
	#display drawing code
	if scupdate==1:
		scupdate=0
		yval=yoff
		screensurf.fill(bgcol)
		clicklist=list()
		#draw logo overlay first so as not to be over images
		screensurf.blit(logooverlay, (((screenw - 250), (screenh - 250))))
		for itmtype in root.findall("*"):
			#print "foo0"
			if itmtype.tag=="text":
				textcont=(itmtype.text + "\n")
				textchunk=""
				#this draws the text body line-per-line
				for texch in textcont:
					if texch=="\n":
						texgfx=simplefont.render(textchunk, True, textcol, bgcol)
						screensurf.blit(texgfx, (xoff, yval))
						yval += yjump
						textchunk=""
					else:
						#if not at a newline yet, keep building textchunk.
						textchunk=(textchunk + texch)
			if itmtype.tag=="lnk":
				lnkref=itmtype.text
				simplefont.set_underline(1)
				texgfx=simplefont.render(itmtype.attrib.get("label"), True, linkcol, bgcol)
				simplefont.set_underline(0)
				lnkbx=screensurf.blit(texgfx, (xoff, yval))
				yval += yjump
				clickobj=clicktab(lnkbx, lnkref)
				clicklist.extend([clickobj])
			if itmtype.tag=="img":
				imgfile=itmtype.text
				imgdat=filelookup(imgfile)
				screensurf.blit(imgdat, (xoff, yval))
				yval += imgdat.get_height()
		#if screenw>=640 and screenh>=480:
			#screensurf.blit(logooverlay, (((screenw - 200), (screenh - 200))))
		
		helpq=screensurf.blit(iconhelp, (((screenw - 44), (0))))
		quitq=screensurf.blit(iconquit, (((screenw - 44), (88))))
		indexq=screensurf.blit(iconindex, (((screenw - 44), (44))))
		pygame.display.update()
		qtexty=yval
	#handles "click and drag" scrolling
	if followmouse==1:
		ppos=mpos
		mpos=pygame.mouse.get_pos()
		#xoff -=(ppos[0] - mpos[0])
		yoff -=(ppos[1] - mpos[1])
		if yoff>0:
			yoff=0
		scupdate=1
	time.sleep(0.05)
	for event in pygame.event.get():
		if event.type == QUIT:
			qflg=1
			break
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			qflg=1
			break
		if event.type == KEYDOWN and event.key == K_F1:
			pageref="helponhelp.xml"
			yoff=0
			break
		if event.type == KEYDOWN and event.key == K_F8:
			pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-helpview.png')))
			break
		if event.type == KEYDOWN and event.key == K_DOWN:
			if qtexty>(yjump + yjump):
				yoff -= yjump
			scupdate=1
		if event.type == KEYDOWN and event.key == K_UP:
			yoff += yjump
			if yoff>0:
				yoff=0
			scupdate=1
		if event.type == KEYDOWN and event.key == K_PAGEUP:
			yoff += (yjump * 20)
			if yoff>0:
				yoff=0
			scupdate=1
		if event.type == KEYDOWN and event.key == K_PAGEDOWN:
			if qtexty>(yjump + yjump):
				yoff -= (yjump * 20)
			#if qtexty<0:
			#	yoff=0
			scupdate=1
		if event.type == KEYDOWN and event.key == K_LEFT:
			xoff += yjump
			scupdate=1
		if event.type == KEYDOWN and event.key == K_RIGHT:
			xoff -= yjump
			scupdate=1
		if event.type == KEYDOWN and (event.key == K_PLUS or event.key == K_EQUALS or event.key == K_KP_PLUS):
			yjump += 1
			fontsize += 1
			simplefont = pygame.font.SysFont(None, fontsize)
			
			scupdate=1
		if event.type == KEYDOWN and (event.key == K_MINUS or event.key == K_KP_MINUS):
			yjump -= 1
			fontsize -= 1
			if yjump<=0:
				yjump=1
			if fontsize<=0:
				fontsize=1
			simplefont = pygame.font.SysFont(None, fontsize)
			scupdate=1
		if event.type==MOUSEBUTTONDOWN:
			if helpq.collidepoint(event.pos)==1 and event.button==1:
				pageref="helponhelp.xml"
				yoff=0
				break
			if indexq.collidepoint(event.pos)==1 and event.button==1:
				pageref="helpindex.xml"
				yoff=0
				break
			if quitq.collidepoint(event.pos)==1 and event.button==1:
				qflg=1
				break
			#mouse wheel scrolling
			if event.button==5:
				if qtexty>(yjump + yjump):
					yoff -= yjump
					scupdate=1
					#break
			if event.button==4:
				yoff += yjump
				if yoff>0:
					yoff=0
				scupdate=1
				#break
			#parses clickboxes generated by links
			clickdrag=1
			for clint in clicklist:
				if (clint.box).collidepoint(event.pos)==1 and event.button==1:
					pageref=clint.link
					yoff=0
					clickdrag=0
					break
			if event.button==1 and clickdrag==1:
				followmouse=1
				mpos=pygame.mouse.get_pos()
		if event.type==MOUSEBUTTONUP:
			#sets followmouse to 0 to stop image moving
			if event.button==1:
				followmouse=0
		if event.type==VIDEORESIZE:
			resizeflg=1
			resw=event.w
			resh=event.h
					