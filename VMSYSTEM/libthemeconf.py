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

themetag=confroot.find("theme")
themefile=themetag.attrib.get("themefile")

if os.path.isfile(os.path.join("VMSYSTEM", "CFG", themefile)):
	themetree = ET.parse(os.path.join("VMSYSTEM", "CFG", themefile))
	themeroot = themetree.getroot()
elif os.path.isfile(os.path.join("VMUSER", "CFG", themefile)):
	themetree = ET.parse(os.path.join("VMUSER", "CFG", themefile))
	themeroot = themetree.getroot()
elif os.path.isfile(os.path.join("VMSYSTEM", "CFG", "default.thm")):
	themetree = ET.parse(os.path.join("VMSYSTEM", "CFG", themefile))
	themeroot = themetree.getroot()
else:
	sys.exit("ERROR: libthemeconf: UNABLE TO LOAD A .thm THEME FILE!")

internalformatvers=1.0

themeinfo=themeroot.find("info")
themename=themeinfo.attrib.get("name")
themedesc=themeinfo.attrib.get("description")
formatvers=float(themeinfo.attrib.get("formatvers"))


def getthemeinfo(themefilename):
	if os.path.isfile(os.path.join("VMSYSTEM", "CFG", themefilename)):
		thtree = ET.parse(os.path.join("VMSYSTEM", "CFG", themefilename))
		throot = thtree.getroot()
	elif os.path.isfile(os.path.join("VMUSER", "CFG", themefilename)):
		thtree = ET.parse(os.path.join("VMUSER", "CFG", themefilename))
		throot = thtree.getroot()
	thinfo=throot.find("info")
	thname=thinfo.attrib.get("name")
	thdescription=thinfo.attrib.get("description")
	return (thname, thdescription)
	



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




hudtag=themeroot.find("hud")
hudbg=pygame.Color(hudtag.attrib.get("bg"))
hudtext=pygame.Color(hudtag.attrib.get("text"))
huddiv=pygame.Color(hudtag.attrib.get("div"))


desktag=themeroot.find("desk")
deskcolor=pygame.Color(desktag.attrib.get("bg"))
desktext=pygame.Color(desktag.attrib.get("text"))


titleacttag=themeroot.find("titleact")
titleactbg=pygame.Color(titleacttag.attrib.get("bg"))
titleacttext=pygame.Color(titleacttag.attrib.get("text"))
titleinacttag=themeroot.find("titleinact")
titleinactbg=pygame.Color(titleinacttag.attrib.get("bg"))
titleinacttext=pygame.Color(titleinacttag.attrib.get("text"))

tiletag=themeroot.find("tile")
tilecolor=pygame.Color(tiletag.attrib.get("color"))
tilecolor.a=(int(tiletag.attrib.get("alpha")))
tiletext=pygame.Color(tiletag.attrib.get("text"))



diagtag=themeroot.find("diag")
diagbg=pygame.Color(diagtag.attrib.get("bg"))
diagtext=pygame.Color(diagtag.attrib.get("text"))
diaginact=pygame.Color(diagtag.attrib.get("inact"))
diagline=pygame.Color(diagtag.attrib.get("line"))


tbtag=themeroot.find("textbox")
textboxline=pygame.Color(tbtag.attrib.get("line"))
textboxbg=pygame.Color(tbtag.attrib.get("bg"))
textboxtext=pygame.Color(tbtag.attrib.get("text"))


calctag=themeroot.find("calc")

calcpadbg=pygame.Color(calctag.attrib.get("padbg"))
calcpadtext=pygame.Color(calctag.attrib.get("padtext"))
calcpadline=pygame.Color(calctag.attrib.get("padline"))
calclockon=pygame.Color(calctag.attrib.get("lockon"))
calclockoff=pygame.Color(calctag.attrib.get("lockoff"))


helptag=themeroot.find("help")

helpbg=pygame.Color(helptag.attrib.get("bg"))
helptext=pygame.Color(helptag.attrib.get("text"))
helplink=pygame.Color(helptag.attrib.get("link"))


tvtag=themeroot.find("textview")

textvbg=pygame.Color(tvtag.attrib.get("bg"))
textvtext=pygame.Color(tvtag.attrib.get("text"))
textvtextblk=pygame.Color(tvtag.attrib.get("textblock"))
textvhig1=pygame.Color(tvtag.attrib.get("hig1"))
textvcomment=pygame.Color(tvtag.attrib.get("comment"))
textvgotoref=pygame.Color(tvtag.attrib.get("gotoref"))
textvgotolabel=pygame.Color(tvtag.attrib.get("gotolabel"))

btntag=themeroot.find("btn")

btnbg1=pygame.Color(btntag.attrib.get("bg1"))
btnbg2=pygame.Color(btntag.attrib.get("bg2"))
btnactbg=pygame.Color(btntag.attrib.get("actbg"))
btnacttext=pygame.Color(btntag.attrib.get("acttext"))
btninactbg=pygame.Color(btntag.attrib.get("inactbg"))
btninacttext=pygame.Color(btntag.attrib.get("inacttext"))
btnline=pygame.Color(btntag.attrib.get("line"))
btntext=pygame.Color(btntag.attrib.get("text"))
btnok=pygame.Color(btntag.attrib.get("ok"))
btncancel=pygame.Color(btntag.attrib.get("cancel"))

vmtag=themeroot.find("vm")

vmstatbg=pygame.Color(vmtag.attrib.get("statbg"))
vmstattext=pygame.Color(vmtag.attrib.get("stattext"))
vmcurth=pygame.Color(vmtag.attrib.get("curth"))
vminst=pygame.Color(vmtag.attrib.get("inst"))
vmdata=pygame.Color(vmtag.attrib.get("data"))
vmreg1=pygame.Color(vmtag.attrib.get("reg1"))
vmreg2=pygame.Color(vmtag.attrib.get("reg2"))
vmaddr=pygame.Color(vmtag.attrib.get("addr"))
vmrom=pygame.Color(vmtag.attrib.get("rom"))
vmbg=pygame.Color(vmtag.attrib.get("bg"))

#vmstatbg=(0, 0, 0)
#vmstattext=(255, 255, 255)
#vmcurth=(127, 0, 255)
#vminst=(0, 255, 255)
#vmdata=(0, 255, 127)
#vmreg1=(255, 0, 127)
#vmreg2=(255, 127, 0)
#vmaddr=(0, 127, 255)
#vmrom=(255, 0, 255)
#vmbg=(5, 38, 121)
credittag=themeroot.find("credit")


credittext=pygame.Color(credittag.attrib.get("text"))
creditbg=pygame.Color(credittag.attrib.get("bg"))

