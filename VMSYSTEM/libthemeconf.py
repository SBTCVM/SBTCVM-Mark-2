#!/usr/bin/env python
import xml.etree.ElementTree as ET
import os
import sys
import time
import pygame
from pygame.locals import *
#import VMSYSTEM.libvmui as vmui



if os.path.isfile(os.path.join("VMUSER", "CFG", "theme.xml")):
	conftree = ET.parse(os.path.join("VMUSER", "CFG", "theme.xml"))
	confroot = conftree.getroot()
elif os.path.isfile(os.path.join("VMSYSTEM", "CFG", "theme.xml")):
	conftreedef = ET.parse(os.path.join("VMSYSTEM", "CFG", "theme.xml"))
	confrootdef = conftreedef.getroot()
	makeconf=open(os.path.join("VMUSER", "CFG", "theme.xml"), "w")
	conftreedef.write(makeconf)
	makeconf.close()
	conftree = ET.parse(os.path.join("VMUSER", "CFG", "theme.xml"))
	confroot = conftree.getroot()
else:
	sys.exit("ERROR: libthemeconf: UNABLE TO LOAD: theme.xml")
	

def getconf(category, attrib):
	cattag=confroot.find(category)
	return cattag.attrib.get(attrib)
def setconf(category, attrib, value):
	cattag=confroot.find(category)
	cattag.set(attrib, value)
def saveconf():
	conftree.write(os.path.join("VMUSER", "CFG", "theme.xml"))
def resetconf():
	if os.path.isfile(os.path.join("VMSYSTEM", "CFG", "theme.xml")):
		global conftree
		global confroot
		conftree = ET.parse(os.path.join("VMSYSTEM", "CFG", "theme.xml"))
		confroot = conftree.getroot()
	else:
		sys.exit("ERROR: libthemeconf: UNABLE TO LOAD: theme.xml")


def bgmake(programbgoverlay=None):
	themebg0=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'THEME-BG0.jpg'))
	themebg1=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'THEME-BG1.jpg'))
	themebg2=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'THEME-BG2.jpg'))
	BGNUM=int(getconf("desk", "bgtheme"))
	if BGNUM==0:
		bg=themebg0
	if BGNUM==1:
		bg=themebg1
	if BGNUM==2:
		bg=themebg2
	if programbgoverlay!=None:
		bg.blit(programbgoverlay, (0, 0))
	return bg





hudbg=(229, 229, 229)
hudtext=(0, 0, 0)
deskcolor=(44, 71, 100)
tilecolor=(255, 255, 255, 200)
tiletext=(0, 0, 0)
diagbg=(255, 255, 255)
diagtext=(0, 0, 0)
diaginact=(100, 100, 100)
diagline=(120, 120, 120)
