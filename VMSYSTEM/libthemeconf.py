#!/usr/bin/env python
import xml.etree.ElementTree as ET
import os
import sys
import time
import pygame
from pygame.locals import *
import VMSYSTEM.libvmui as vmui



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


def bgmake(programbgoverlay):
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
	bg.blit(programbgoverlay, (0, 0))
	return bg


mbg0=vmui.menuitem("Blue Gradient", "BG0")
mbg1=vmui.menuitem("Flower", "BG1")
mbg2=vmui.menuitem("Clouds", "BG2")

bgmenu=[mbg0, mbg1, mbg2]

def settheme(xpos, ypos):
	bgret=vmui.menuset(bgmenu, xpos, ypos, reclick=0, fontsize=26)
	if bgret=="BG0":
		setconf("desk", "bgtheme", "0")
		saveconf()
	if bgret=="BG1":
		setconf("desk", "bgtheme", "1")
		saveconf()
	if bgret=="BG2":
		setconf("desk", "bgtheme", "2")
		saveconf()