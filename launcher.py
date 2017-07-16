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
# load dzulib1 Desutezeoid support library
import launcher_data.dzulib1 as dzulib

#THIS COPY OF DESUTEZEOID HAS BEEN MODIFIED.
#Data is hardcoded to subdirectory "launcher_data"
#plus other changes.
#
#


from pygame.locals import *
import xml.etree.ElementTree as ET
pygame.display.init()
pygame.font.init()
pygame.mixer.init()
print "SBTCVM tutorial"
print "Based On The Desutezeoid arbitrary point and click engine v1.5.1"
print "parsing ENGSYSTEM.xml"
conftree = ET.parse(os.path.join("launcher_data", "ENGSYSTEM.xml"))
confroot = conftree.getroot()

screentag=confroot.find("screen")
uitag=confroot.find("ui")
uicolorstag=uitag.find("main")
uifgcolor=pygame.Color(uicolorstag.attrib.get("FGCOLOR", "#000000"))
uibgcolor=pygame.Color(uicolorstag.attrib.get("BGCOLOR", "#FFFFFF"))
uifgcolorstr=uicolorstag.attrib.get("FGCOLOR", "#000000")
uibgcolorstr=uicolorstag.attrib.get("BGCOLOR", "#FFFFFF")
uitextsize=int(uicolorstag.attrib.get("textsize", "24"))

uiquittag=uitag.find("quit")
uiquitmsg=uiquittag.attrib.get("MSG", "Are you sure you want to quit?")
#load main.sav. if IOError, Attempt to initalize main.sav, then try to load main.sav again.
try:
	mainsavtree = ET.parse(os.path.join("launcher_data", "main.sav"))
	mainsavroot = mainsavtree.getroot()
except IOError:
	print ('main.sav not found.')
	dzulib.initmainsave()
	mainsavtree = ET.parse(os.path.join("launcher_data", "main.sav"))
	mainsavroot = mainsavtree.getroot()
	
print "main.sav loaded"

pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN])

filedict={}
textdict={}

def filelookup(filename):
	global filedict
	if filename in filedict:
		return filedict[filename]
	else:
		if (filename.lower()).endswith(".jpg") or (filename.lower()).endswith(".jpeg") or (filename.lower()).startswith("no-tr"):
			imgret=pygame.image.load(os.path.join("launcher_data", filename)).convert()
		else:
			imgret=pygame.image.load(os.path.join("launcher_data", filename)).convert_alpha()
		filedict[filename]=imgret
		return imgret

def textrender(text, size, fgcolor, bgcolor, transp):
	global textdict
	keyx=(text + str(size) + fgcolor + bgcolor + str(transp))
	if keyx in textdict:
		return textdict[keyx]
	else:
		fgcolor=pygame.Color(fgcolor)
		bgcolor=pygame.Color(bgcolor)
		texfnt=pygame.font.SysFont(None, size)
		if transp==0:
			texgfx=texfnt.render(text, True, fgcolor, bgcolor)
		else:
			texgfx=texfnt.render(text, True, fgcolor)
		textdict[keyx]=texgfx
		return texgfx
			
	

print "populate keylist with null keyid, add any keys in initkeys."
initkeystag=confroot.find("initkeys")
savkeystag=confroot.find("savkeys")

keylist=list(["0"])
for initk in initkeystag.findall("k"):
	if (initk.attrib.get("keyid"))!="0":
		keylist.extend([initk.attrib.get("keyid")])
print "add any keyids from main.sav"
keysav=mainsavroot.find('keysav')
for savk in keysav.findall("k"):
	if (savk.attrib.get("keyid"))!="0":
		keylist.extend([savk.attrib.get("keyid")])

scrnx=int(screentag.attrib.get("x", "800"))
scrny=int(screentag.attrib.get("y", "600"))
titletag=confroot.find("title")
debugtag=confroot.find("debug")
DEBUG=int(debugtag.attrib.get("debug", "1"))
printkeys=int(debugtag.attrib.get("printkeys", "1"))
clickfields=int(debugtag.attrib.get("clickfields", "0"))
cfcolor=pygame.Color(debugtag.attrib.get("cfcolor", "#888888"))

beginref=(confroot.find("beginref")).text

globalcoretag=confroot.find("globalcore")
globalforkstag=confroot.find("globalforks")
icontag=titletag.attrib.get("icon", "NULL")
if icontag!="NULL":
	windowicon=pygame.image.load(os.path.join("launcher_data", icontag))
	pygame.display.set_icon(windowicon)
	
print "config parsed."
titlebase=titletag.attrib.get("base", "Desutezeoid: ")
class clicktab:
	def __init__(self, box, reftype, ref, keyid, takekey, sfxclick, sound, quitab=0):
		self.box=box
		self.ref=ref
		self.keyid=keyid
		self.takekey=takekey
		self.reftype=reftype
		self.sfxclick=sfxclick
		self.sound=sound
		self.quitab=quitab
class timeouttab:
	def __init__(self, seconds, keyid, postkey):
		self.keyid=keyid
		self.regtime=time.time()
		self.seconds=seconds
		self.postkey=postkey

class uimenutab:
	def __init__(self, con, keyid, stay=0, noact=0, surfrender=None):
		self.keyid=keyid
		self.con=con
		self.surfrender=surfrender
		self.stay=stay
		self.noact=noact




#class keyobj:
#	def __init__(self, keyid):
#		self=keyid
def debugmsg(msg):
	if DEBUG==1:
		print msg
def keyprint():
	if printkeys==1:
		print keylist
keyprint()
prevpage="NULL"
curpage=beginref

screensurf=pygame.display.set_mode((scrnx, scrny))
screensurf.set_alpha(None)
quitflag=0
clicklist=list()

#menu dialog function
def qmenu(xpos, ypos, itemlist, fgcol=uifgcolorstr, bgcol=uibgcolorstr, uipoptextsize=uitextsize):
	#qfnt=pygame.font.SysFont(None, uipoptextsize)
	texty=3
	textx=100
	fgc=pygame.Color(fgcol)
	bgc=pygame.Color(bgcol)
	itemlistB=list()
	for itm in itemlist:
		texty += uipoptextsize
		if itm.noact==1:
			#qtext1=qfnt.render(itm.con, True, fgcol, bgcol)
			qtext1=textrender(itm.con, uipoptextsize, fgcol, bgcol, 0)
		else:
			#qtext1=qfnt.render(itm.con, True, bgcol, fgcol)
			qtext1=textrender(itm.con, uipoptextsize, bgcol, fgcol, 0)
		#print itm.con
		itmB=uimenutab(itm.con, itm.keyid, itm.stay, itm.noact, qtext1)
		if (qtext1.get_width())>textx:
			textx=qtext1.get_width()
		itemlistB.extend([itmB])
	
	xpos=((xpos - int(textx / 2)) - 3)
	ypos=((ypos - int(texty / 2)) - 3)
	qboxwidth=(6 + textx)
	qboxhight=(texty + 20)
	if qboxwidth<100:
		qboxwidth=100
	qbox=pygame.Surface((qboxwidth, qboxhight))
	qbox.fill((bgc))
	boxtrace=screensurf.blit(qbox, (xpos, ypos))

	
	texreny=(ypos + 3)
	texrenx=(xpos + 3)
	retlist=list()
	for itm in itemlistB:
		itmclick=screensurf.blit(itm.surfrender, (texrenx, (texreny)))
		texreny += uipoptextsize
		if itm.noact==0:
			if itm.stay==0:
				itmclicktab=clicktab(itmclick, "key", "none", itm.keyid, "0", 0, "none", quitab=3)
			else:
				itmclicktab=clicktab(itmclick, "key", "none", itm.keyid, "0", 0, "none")
			retlist.extend([itmclicktab])
	#screensurf.blit(qtext1, ((xpos + 3), (ypos + 3)))
	pygame.draw.rect(screensurf, fgc, boxtrace, 3)
	return(retlist)

	


#simple dialog popup generator. used by uipop forks and the engine quit dialogs.
def qpop(qmsg, xpos, ypos, keyid="0", nokey="0", quyn=0, specialquit=0, fgcol=uifgcolorstr, bgcol=uibgcolorstr, uipoptextsize=uitextsize, img="none"):
	#qfnt=pygame.font.SysFont(None, uipoptextsize)
	fgc=pygame.Color(fgcol)
	bgc=pygame.Color(bgcol)
	if img!="none":
		qimg=filelookup(img)
		qimgflg=1
		qimgy=qimg.get_height()
		qimgx=qimg.get_width()
	else:
		qimgflg=0
		qimgy=0
		qimgx=0
	prevxpos=xpos
	#qtext1=qfnt.render(qmsg, True, fgcol, bgcol)
	qtext1=textrender(qmsg, uipoptextsize, fgcol, bgcol, 0)
	xpos=((xpos - int(qtext1.get_width() / 2)) - 3)
	if qimgflg==1:
		#if image is present, center ypos on image
		ypos=((ypos - int(qimgy / 2)))
	qboxwidth=(6 + (qtext1.get_width()))
	qboxhight=(uipoptextsize + qimgy + uipoptextsize + 20)
	if qboxwidth<100:
		qboxwidth=100
	if qboxwidth<qimgx:
		qboxwidth=(qimgx + 6)
		#if image is wider than text, center xpos on image
		xpos=((prevxpos - int(qimgx / 2)) - 3)
	qbox=pygame.Surface((qboxwidth, qboxhight))
	qbox.fill((bgc))
	boxtrace=screensurf.blit(qbox, (xpos, ypos))
	if qimgflg==1:
		screensurf.blit(qimg, ((xpos + 3), (ypos + 3)))
	screensurf.blit(qtext1, ((xpos + 3), (ypos + qimgy + 3)))
	pygame.draw.rect(screensurf, fgc, boxtrace, 3)
	if quyn==1:
		#qytext=qfnt.render("Yes", True, bgcol, fgcol)
		#qntext=qfnt.render("No", True, bgcol, fgcol)
		qytext=textrender("Yes", uipoptextsize, bgcol, fgcol, 0)
		qntext=textrender("No", uipoptextsize, bgcol, fgcol, 0)
		yesclick=screensurf.blit(qytext, ((xpos + 10), (ypos + qimgy + 10 + uipoptextsize)))
		noclick=screensurf.blit(qntext, ((xpos + 50 + qytext.get_width()), (ypos + qimgy + 10 + uipoptextsize)))
		ref="none"
		takekey="0"
		clicksoundflg=0
		soundname=0
		if specialquit==1:
			yesdat=clicktab(yesclick, "quitx", ref, keyid, takekey, clicksoundflg, soundname)
			nodat=clicktab(noclick, "key", ref, nokey, takekey, clicksoundflg, soundname, quitab=1)
		else:
			yesdat=clicktab(yesclick, "key", ref, keyid, takekey, clicksoundflg, soundname, quitab=2)
			nodat=clicktab(noclick, "key", ref, nokey, takekey, clicksoundflg, soundname, quitab=2)
		retclicks=([])
		retclicks.extend([yesdat])
		retclicks.extend([nodat])

		return(retclicks, quyn)
	else:
		#qytext=qfnt.render("Ok", True, bgcol, fgcol)
		qytext=textrender("Ok", uipoptextsize, bgcol, fgcol, 0)
		yesclick=screensurf.blit(qytext, ((xpos + 10), (ypos + qimgy + 10 + uipoptextsize)))
		ref="none"
		takekey="0"
		clicksoundflg=0
		soundname=0
		yesdat=clicktab(yesclick, "key", ref, keyid, takekey, clicksoundflg, soundname, quitab=2)
		retclicks=([])
		retclicks.extend([yesdat])
		return(retclicks, quyn)

	
	

timeoutlist=list()
keybak=list(keylist)
forksanitycheck=0
forksanity=0
cachepage=prevpage
print "done. begin mainloop."
uiquit=0
qpopflg=0
qmenuflg=0
while quitflag==0:
	huris=0
	clicklist=list()
	#Engine Speed
	time.sleep(0.05)
	pos = pygame.mouse.get_pos()
	#print "tic"
	if curpage!=prevpage:
		print "flushing image cache"
		del filedict
		filedict={}
		del textdict
		textdict={}
		print "preparsing page"
		tree = ET.parse(os.path.join("launcher_data", curpage))
		root = tree.getroot()
		cachepage=prevpage
		prevpage=curpage
		coretag=root.find('core')
		forktag=root.find('forks')
		print "parsing global core objects into page structure..."
		for glb in globalcoretag:
			coretag.append(copy.deepcopy(glb))
		print "parsing global fork objects into page structure..."
		for glb in globalforkstag:
			forktag.append(copy.deepcopy(glb))
		pageconf=root.find('pageconf')
		pagetitle=(pageconf.find('title')).text
		BGMstop=int(pageconf.attrib.get("BGMstop", "1"))
		pagekeysflg=int(pageconf.attrib.get("pagekeys", "0"))
		if pagekeysflg==1:
			pagekeytag=root.find("pagekeys")
			for pagekey in pagekeytag.findall("k"):
				pagekeyid=pagekey.attrib.get("keyid")
				if not pagekeyid in keylist:
					keylist.extend([pagekeyid])
					#print keylist
					keyprint()
		if BGMstop==1:
			pygame.mixer.music.stop()
		BGon=int(pageconf.attrib.get("BGimg", "0"))
		BGMon=int(pageconf.attrib.get("BGM", "0"))
		if BGMon==1:
			BGMtrack=(pageconf.find('BGM')).text
			pygame.mixer.music.load(BGMtrack)
			pygame.mixer.music.play(-1)
		pygame.display.set_caption((titlebase + pagetitle), (titlebase + pagetitle))
		print ("Page title: '" + pagetitle + "'")
		if BGon==1:
			BGfile=(pageconf.find('BG')).text
			BG=pygame.image.load(os.path.join("launcher_data", BGfile)).convert()
		screensurf.fill((170, 170, 170))
		print "done. begin mainloop"
	if BGon==1:
		screensurf.blit(BG, (0, 0))
	for fork in forktag.findall("ortrig"):
		#print "batchtrig"
		masterkey=fork.attrib.get("keyid")
		orflg=0
		for keyif in fork.findall("k"):
			ifpol=keyif.attrib.get("if")
			subkey=keyif.attrib.get("keyid")
			if subkey in keylist:
				if ifpol=="1":
					orflg=1
			elif not subkey in keylist:
				if ifpol=="0":
					orflg=1
		if orflg == 1:
			if not masterkey in keylist:
				keylist.extend([masterkey])
				#print keylist
				keyprint()
				forksanity=1
		else:
			if masterkey in keylist:
				keylist.remove(masterkey)
				#print keylist
				keyprint()
				forksanity=1
	for fork in forktag.findall("batchtrig"):
		#print "batchtrig"
		masterkey=fork.attrib.get("keyid")
		complist=[1] 
		for keyif in fork.findall("k"):
			ifpol=keyif.attrib.get("if")
			subkey=keyif.attrib.get("keyid")
			if subkey in keylist:
				if ifpol=="1":
					complist.extend([1])
				else:
					complist.extend([0])
			elif not subkey in keylist:
				if ifpol=="0":
					complist.extend([1])
				else:
					complist.extend([0])
		if len(set(complist)) == 1:
			if not masterkey in keylist:
				keylist.extend([masterkey])
				#print keylist
				keyprint()
				forksanity=1
		else:
			if masterkey in keylist:
				keylist.remove(masterkey)
				#print keylist
				keyprint()
				forksanity=1
	for fork in forktag.findall("batchset"):
		#print "batch"
		#print fork
		masterkey=fork.attrib.get("keyid")
		toggpol=fork.attrib.get("set")
		if masterkey in keylist:
			keylist.remove(masterkey)
			if toggpol=="1":
				for subkey in fork.findall("k"):
					subkeyid=subkey.attrib.get("keyid")
					if not subkeyid in keylist:
						keylist.extend([subkeyid])
						#print keylist
						keyprint()
				forksanity=1
			elif toggpol=="2":
				for subkey in fork.findall("k"):
					subkeyid=subkey.attrib.get("keyid")
					if not subkeyid in keylist:
						keylist.extend([subkeyid])
						#print keylist
						keyprint()
					elif subkeyid in keylist:
						keylist.remove(subkeyid)
						#print keylist
						keyprint()
			else:
				for subkey in fork.findall("k"):
					subkeyid=subkey.attrib.get("keyid")
					if subkeyid in keylist:
						keylist.remove(subkeyid)
						#print keylist
						keyprint()
				forksanity=1
	pagejumpflag=0
	for fork in forktag.findall("pagejump"):
		masterkey=fork.attrib.get("keyid")
		if masterkey in keylist:
			keylist.remove(masterkey)
			useprvpge=int(fork.attrib.get('useprev', '0'))
			curpage=fork.attrib.get("page")
			if useprvpge==1 and cachepage!="NULL":
				curpage=cachepage
				
			
			print ("iref: loading page '" + curpage + "'")
			pagejumpflag=1
			break
	for fork in forktag.findall("music"):
		masterkey=fork.attrib.get("keyid")
		if masterkey in keylist:
			keylist.remove(masterkey)
			xmusstop=int(fork.attrib.get('stop', '0'))
			xmusplay=int(fork.attrib.get('play', '0'))
			if xmusstop==1:
				pygame.mixer.music.stop()
			elif xmusplay==1:
				pygame.mixer.music.play(-1)
			else:
				mustrack=fork.attrib.get("track")
				pygame.mixer.music.load(mustrack)
				pygame.mixer.music.play(-1)
			
	for fork in forktag.findall("uipop"):
		masterkey=fork.attrib.get("keyid")
		msg=fork.attrib.get("msg")
		qpopx=int(fork.attrib.get("x",(screensurf.get_rect().centerx)))
		qpopy=int(fork.attrib.get("y",(screensurf.get_rect().centery)))
		#FGCOL=pygame.Color(fork.attrib.get("FGCOLOR", uifgcolorstr))
		#BGCOL=pygame.Color(fork.attrib.get("BGCOLOR", uibgcolorstr))
		FGCOL=fork.attrib.get("FGCOLOR", uifgcolorstr)
		BGCOL=fork.attrib.get("BGCOLOR", uibgcolorstr)
		QFNTSIZE=int(fork.attrib.get("textsize", uitextsize))
		uiimg=fork.attrib.get("img", "none")

		if masterkey in keylist:
			keylist.remove(masterkey)
			ynflag=int(fork.attrib.get("ynflag", "0"))
			if ynflag==1:
				yeskey=fork.attrib.get("yeskey", "0")
				nokey=fork.attrib.get("nokey", "0")
				#poppost=qpop(msg, qpopx, qpopy, keyid=yeskey, nokey=nokey, quyn=1)
				qpopdat=(msg, qpopx, qpopy, yeskey, nokey, 1, FGCOL, BGCOL, QFNTSIZE, uiimg)
				qpopflg=1
			else:
				okkey=fork.attrib.get("okkey", "0")
				#poppost=qpop(msg, qpopx, qpopy, keyid=okkey, quyn=0)
				qpopdat=(msg, qpopx, qpopy, okkey, "0", 0, FGCOL, BGCOL, QFNTSIZE, uiimg)
				qpopflg=1
				
	for fork in forktag.findall("uimenu"):
		masterkey=fork.attrib.get("keyid")
		qpopx=int(fork.attrib.get("x",(screensurf.get_rect().centerx)))
		qpopy=int(fork.attrib.get("y",(screensurf.get_rect().centery)))
		#FGCOL=pygame.Color(fork.attrib.get("FGCOLOR", uifgcolorstr))
		#BGCOL=pygame.Color(fork.attrib.get("BGCOLOR", uibgcolorstr))
		FGCOL=fork.attrib.get("FGCOLOR", uifgcolorstr)
		BGCOL=fork.attrib.get("BGCOLOR", uibgcolorstr)
		QFNTSIZE=int(fork.attrib.get("textsize", uitextsize))
		if masterkey in keylist:
			keylist.remove(masterkey)
			itemlist=list()
			for itmf in fork.findall("item"):
				itmftab=uimenutab(itmf.attrib.get("con"), itmf.attrib.get("keyid", "0"), stay=int(itmf.attrib.get("stay", "0")), noact=int(itmf.attrib.get("noact", "0")))
				itemlist.extend([itmftab])
			qmenudat=(qpopx, qpopy, itemlist, FGCOL, BGCOL, QFNTSIZE)
			qmenuflg=1
	for fork in forktag.findall("timeout"):
		masterkey=fork.attrib.get("keyid")
		if masterkey in keylist:
			notinlist=1
			for tif in timeoutlist:
				if tif.keyid==masterkey:
					notinlist=0
			if notinlist==1:
				seconds=float(fork.attrib.get("seconds"))
				postkey=fork.attrib.get("post", "0")
				timeoutlist.extend([timeouttab(seconds, masterkey, postkey)])
	for fork in forktag.findall("triggerlock"):
		masterkey=fork.attrib.get("keyid")
		triggerkey=fork.attrib.get("trigger")
		lockkey=fork.attrib.get("lock")
		if masterkey in keylist:
			#keylist.remove(masterkey)
			if lockkey not in keylist:
				if triggerkey not in keylist:
					keylist.extend([triggerkey])
					keylist.extend([lockkey])
	
				
	for fork in forktag.findall("quit"):
		masterkey=fork.attrib.get("keyid")
		if masterkey in keylist:
			keylist.remove(masterkey)
			uiquit=1
	for fork in forktag.findall("menulaunch"):
		masterkey=fork.attrib.get("keyid")
		if masterkey in keylist:
			keylist.remove(masterkey)
			subprocess.Popen(["python", "MK2-MENU.py"])
	for fork in forktag.findall("tutlaunch"):
		masterkey=fork.attrib.get("keyid")
		if masterkey in keylist:
			keylist.remove(masterkey)
			subprocess.Popen(["python", "SBTCVM_tutorial.py"])
	for fork in forktag.findall("gttlaunch"):
		masterkey=fork.attrib.get("keyid")
		if masterkey in keylist:
			keylist.remove(masterkey)
			subprocess.Popen(["python", "MK2-RUN.py", "gtt.streg"])
	for fork in forktag.findall("introlaunch"):
		masterkey=fork.attrib.get("keyid")
		if masterkey in keylist:
			keylist.remove(masterkey)
			subprocess.Popen(["python", "MK2-RUN.py", "intro.streg"])
	for fork in forktag.findall("creditslaunch"):
		masterkey=fork.attrib.get("keyid")
		if masterkey in keylist:
			keylist.remove(masterkey)
			subprocess.Popen(["python", "MK2-TOOLS.py", "uicredits"])
	for fork in forktag.findall("fileviewlaunch"):
		masterkey=fork.attrib.get("keyid")
		if masterkey in keylist:
			keylist.remove(masterkey)
			subprocess.Popen(["python", "fileview.py"])
	for fork in forktag.findall("sound"):
		masterkey=fork.attrib.get("keyid")
		soundname=fork.attrib.get("sound")
		if masterkey in keylist:
			keylist.remove(masterkey)
			soundobj=pygame.mixer.Sound(os.path.join("launcher_data", soundname))
			soundobj.play()
	if forksanity==1:
		forksanitycheck=1
		forksanity=0
		#skiploop=1
	else:
		forksanitycheck=0
	
	for tif in timeoutlist:
		if tif.keyid not in keylist:
			
			timeoutlist.remove(tif)
		elif ((time.time()) - tif.regtime) > tif.seconds:
			keylist.remove(tif.keyid)
			if tif.postkey not in keylist:
				if tif.postkey!="0":
					keylist.extend([tif.postkey])
			#print keylist
			keyprint()
			timeoutlist.remove(tif)		
		
	keybak=list(keylist)
	#print keylist
	#core object render-parser
	for labref in coretag.findall("*"):
		if labref.tag=="img":
			keyid=labref.attrib.get('keyid', "0")
			takekey=labref.attrib.get('takekey', "0")
			onkey=labref.attrib.get('onkey', "0")
			offkey=labref.attrib.get('offkey', "0")
			hoverkey=labref.attrib.get('hoverkey', "0")
			clicksoundflg=int(labref.attrib.get('sfxclick', "0"))
			soundname=(labref.attrib.get('sound', "0"))
			vscrollval=int(labref.attrib.get('vscroll', "0"))
			hscrollval=int(labref.attrib.get('hscroll', "0"))
			vscfl=int(labref.attrib.get('vscINT', "0"))
			hscfl=int(labref.attrib.get('hscINT', "0"))
			folmousehflg=int(labref.attrib.get('mouseh', "0"))
			folmousevflg=int(labref.attrib.get('mousev', "0"))
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				imgx=int(labref.attrib.get("x"))
				imgy=int(labref.attrib.get("y"))
				imgcon=(labref.find("con")).text
				hovpic=int(labref.attrib.get("hovpic", "0"))
				act=labref.find("act")
				acttype=act.attrib.get("type", "none")
				pos = pygame.mouse.get_pos()
				#scrolling operation init code. (variables are stored inside xml tree in ram)
				if vscfl==0 and vscrollval!=0:
					vscfl=1
					labref.set('vscINT', "1")
					labref.set('vscINTOF', str(vscrollval))
				if hscfl==0 and hscrollval!=0:
					hscfl=1
					labref.set('hscINT', "1")
					labref.set('hscINTOF', str(hscrollval))
				vscoffset=int(labref.attrib.get('vscINTOF', "0"))
				hscoffset=int(labref.attrib.get('hscINTOF', "0"))
				imggfx=filelookup(imgcon)
				if folmousehflg==1:
					imgx=pos[0]
				if folmousevflg==1:
					imgy=pos[1]
				if folmousehflg==2:
					imgx=(pos[0] - int(imggfx.get_width() / 2))
				if folmousevflg==2:
					imgy=(pos[1] - int(imggfx.get_height() / 2))
				if folmousehflg==3:
					moux1=(abs(pos[0] - screensurf.get_width()) - int(imggfx.get_width() / 2))
					imgx=moux1
					#print "x" + str(imgx)
				if folmousevflg==3:
					mouy1=(abs(pos[1] - screensurf.get_height()) - int(imggfx.get_height() / 2))
					imgy=mouy1
					#print "y" + str(imgy)
				if vscfl==1:
					vscoffset += vscrollval
					if imggfx.get_height()<vscoffset:
						vscoffset=0
					if imggfx.get_height()<(vscoffset * -1):
						vscoffset=0
					labref.set('vscINTOF', str(vscoffset))
				if hscfl==1:
					hscoffset += hscrollval
					if imggfx.get_width()<hscoffset:
						hscoffset=0
					if imggfx.get_width()<(hscoffset * -1):
						hscoffset=0
					labref.set('hscINTOF', str(hscoffset))
				#imggfx=pygame.image.load(imgcon)
				
				if hscfl==1:
					imggfx=dzulib.hscroll(hscoffset, imggfx)
				if vscfl==1:
					imggfx=dzulib.vscroll(vscoffset, imggfx)
				clickref=screensurf.blit(imggfx, (imgx, imgy))
				if hoverkey!="0":
					if clickref.collidepoint(pos)==1:
						if not hoverkey in keylist:
							keylist.extend([hoverkey])
					else:
						if hoverkey in keylist:
							keylist.remove(hoverkey)
				if hovpic==1:
					hovcon=(labref.find("altcon")).text
					hovgfx=filelookup(hovcon)
					if clickref.collidepoint(pos)==1:
						clickref=screensurf.blit(hovgfx, (imgx, imgy))
			
				if acttype!="none":
					pos = pygame.mouse.get_pos()
					if acttype=="iref":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "iref", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="prev":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "prev", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="quit":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "quit", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="key":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "key", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
		if labref.tag=="box":
			keyid=labref.attrib.get('keyid', "0")
			takekey=labref.attrib.get('takekey', "0")
			onkey=labref.attrib.get('onkey', "0")
			offkey=labref.attrib.get('offkey', "0")
			hoverkey=labref.attrib.get('hoverkey', "0")
			clicksoundflg=int(labref.attrib.get('sfxclick', "0"))
			soundname=(labref.attrib.get('sound', "0"))
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				imgx=int(labref.attrib.get("x"))
				imgy=int(labref.attrib.get("y"))
				sizex=int(labref.attrib.get("sizex"))
				sizey=int(labref.attrib.get("sizey"))
				onhov=int(labref.attrib.get("onhov", "0"))
				hovcolor=pygame.Color(labref.attrib.get("HOVCOLOR", "#FFFFFF"))
				hovalpha=int(labref.attrib.get("hovalpha", "140"))
				boxalpha=int(labref.attrib.get("alpha", "100"))
				boxcolor=pygame.Color(labref.attrib.get("COLOR", "#FFFFFF"))
				#imgcon=(labref.find("con")).text
				act=labref.find("act")
				acttype=act.attrib.get("type", "none")
				pos = pygame.mouse.get_pos()
				#imggfx=pygame.image.load(imgcon)
				boxgfx=pygame.Surface((sizex, sizey))
				boxgfx.convert_alpha()
				#imggfx.fill(boxcolor)
				boxgfx.set_alpha(0)
				clickref=screensurf.blit(boxgfx, (imgx, imgy))
				if onhov==1 and clickref.collidepoint(pos)==1:
					
					#skip blitting a second time if alpha is 0.
					if hovalpha!=0:
						boxgfx.fill(hovcolor)
						boxgfx.set_alpha(hovalpha)
						clickref=screensurf.blit(boxgfx, (imgx, imgy))
				else:
					
					#skip blitting a second time if alpha is 0.
					if boxalpha!=0:
						boxgfx.fill(boxcolor)
						boxgfx.set_alpha(boxalpha)
						clickref=screensurf.blit(boxgfx, (imgx, imgy))
				if hoverkey!="0":
					if clickref.collidepoint(pos)==1:
						if not hoverkey in keylist:
							keylist.extend([hoverkey])
					else:
						if hoverkey in keylist:
							keylist.remove(hoverkey)		
				if acttype!="none":
					pos = pygame.mouse.get_pos()
					if acttype=="iref":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "iref", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="prev":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "prev", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="quit":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "quit", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
					if acttype=="key":
						ref=act.attrib.get("ref")
						datstr=clicktab(clickref, "key", ref, keyid, takekey, clicksoundflg, soundname)
						clicklist.extend([datstr])
		if labref.tag=="text":
			onkey=labref.attrib.get('onkey', "0")
			offkey=labref.attrib.get('offkey', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				labx=int(labref.attrib.get("x"))
				laby=int(labref.attrib.get("y"))
				size=int(labref.attrib.get("size"))
				#FGCOL=pygame.Color(labref.attrib.get("FGCOLOR", "#FFFFFF"))
				#BGCOL=pygame.Color(labref.attrib.get("BGCOLOR", "#000000"))
				FGCOL=labref.attrib.get("FGCOLOR", "#FFFFFF")
				BGCOL=labref.attrib.get("BGCOLOR", "#000000")
				transp=int(labref.attrib.get("transp", "0"))
				#texfnt=pygame.font.SysFont(None, size)
				pixcnt1=laby
				pixjmp=(size+0)
				textcont=(labref.text + "\n")
				textchunk=""
				#this draws the text body line-per-line
				for texch in textcont:
					if texch=="\n":
						#if at newline, render line of text, clear textchunk, and add to pixcnt1
						#if transp==0:
						#	texgfx=texfnt.render(textchunk, True, FGCOL, BGCOL)
						#else:
						#	texgfx=texfnt.render(textchunk, True, FGCOL)
						texgfx=textrender(textchunk, size, FGCOL, BGCOL, transp)
						screensurf.blit(texgfx, (labx, pixcnt1))
						pixcnt1 += pixjmp
						textchunk=""
					else:
						#if not at a newline yet, keep building textchunk.
						textchunk=(textchunk + texch)
				
				#clickref=screensurf.blit(labgfx, (labx, laby))
		if labref.tag=="label":
			keyid=labref.attrib.get('keyid', "0")
			takekey=labref.attrib.get('takekey', "0")
			onkey=labref.attrib.get('onkey', "0")
			offkey=labref.attrib.get('offkey', "0")
			hoverkey=labref.attrib.get('hoverkey', "0")
			clicksoundflg=int(labref.attrib.get('sfxclick', "0"))
			soundname=(labref.attrib.get('sound', "0"))
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				labx=int(labref.attrib.get("x"))
				laby=int(labref.attrib.get("y"))
				size=int(labref.attrib.get("size"))
				#FGCOL=pygame.Color(labref.attrib.get("FGCOLOR", "#FFFFFF"))
				#BGCOL=pygame.Color(labref.attrib.get("BGCOLOR", "#000000"))
				FGCOL=labref.attrib.get("FGCOLOR", "#FFFFFF")
				BGCOL=labref.attrib.get("BGCOLOR", "#000000")
				labcon=(labref.find("con")).text
				act=labref.find("act")
				acttype=act.attrib.get("type", "none")
				transp=int(labref.attrib.get("transp", "0"))
				#labfnt=pygame.font.SysFont(None, size)
				#if transp==0:
				#	labgfx=labfnt.render(labcon, True, FGCOL, BGCOL)
				#else:
				#	labgfx=labfnt.render(labcon, True, FGCOL)
				labgfx=textrender(labcon, size, FGCOL, BGCOL, transp)
				
				#textrender
				clickref=screensurf.blit(labgfx, (labx, laby))
				if hoverkey!="0":
					if clickref.collidepoint(pos)==1:
						if not hoverkey in keylist:
							keylist.extend([hoverkey])
					else:
						if hoverkey in keylist:
							keylist.remove(hoverkey)
				if acttype!="none":
					pos = pygame.mouse.get_pos()
				if acttype=="iref":
					ref=act.attrib.get("ref")
					datstr=clicktab(clickref, "iref", ref, keyid, takekey, clicksoundflg, soundname)
					clicklist.extend([datstr])
				if acttype=="prev":
					ref=act.attrib.get("ref")
					datstr=clicktab(clickref, "prev", ref, keyid, takekey, clicksoundflg, soundname)
					clicklist.extend([datstr])
				if acttype=="quit":
					ref=act.attrib.get("ref")
					datstr=clicktab(clickref, "quit", ref, keyid, takekey, clicksoundflg, soundname)
					clicklist.extend([datstr])
				if acttype=="key":
					ref=act.attrib.get("ref")
					datstr=clicktab(clickref, "key", ref, keyid, takekey, clicksoundflg, soundname)
					clicklist.extend([datstr])
	
	if qmenuflg==1:
		#qmenudat=(qpopx, qpopy, itemlist, FGCOL, BGCOL, QFNTSIZE)
		menpost=qmenu(qmenudat[0], qmenudat[1], qmenudat[2], fgcol=qmenudat[3], bgcol=qmenudat[4], uipoptextsize=qmenudat[5])
		#qmenu(
		clicklist=(menpost)
	if qpopflg==1:
		poppost=qpop(qpopdat[0], qpopdat[1], qpopdat[2], keyid=(qpopdat[3]), nokey=(qpopdat[4]), quyn=(qpopdat[5]), fgcol=(qpopdat[6]), bgcol=(qpopdat[7]), uipoptextsize=(qpopdat[8]), img=(qpopdat[9]))
		clicklist=(poppost[0])
	if uiquit==1:
		quitxpos=screensurf.get_rect().centerx
		quitypos=screensurf.get_rect().centery
		poppost=qpop(uiquitmsg, quitxpos, quitypos, quyn=1, specialquit=1)
		clicklist=(poppost[0])
	
	if clickfields==1:
		for f in clicklist:
			pygame.draw.rect(screensurf, cfcolor, f.box, 1)
	eventhappen=0
	for event in pygame.event.get():
		#print "nominal"
		eventhappen=1
		if event.type == QUIT:
			uiquit=1
			break
		if event.type == KEYDOWN and event.key == K_F1:
				subprocess.Popen(["python", "MK2-TOOLS.py", "helpview", "launcher.txt"])
		if event.type==MOUSEBUTTONDOWN:
			#print "nominal2"
			for f in clicklist:
				#print "nominal3"
				if f.box.collidepoint(event.pos)==1 and event.button==1:
					if f.sfxclick==1:
						clicksound=pygame.mixer.Sound(os.path.join("launcher_data", f.sound))
						clicksound.play()
					if f.keyid!="0":
						if not f.keyid in keylist:
							keylist.extend([f.keyid])
							#print keylist
							keyprint()
					if f.takekey!="0":
						if takekey in keylist and f.takekey!="0":
							keylist.remove(f.takekey)
							#print keylist
							keyprint()
					
						
					if f.reftype=="iref":
						curpage=f.ref
						print ("iref: loading page '" + f.ref + "'")
						break
					if f.reftype=="prev" and cachepage!="NULL":
						curpage=cachepage
						print ("prev: go to previous page")
						break
					if f.reftype=="quit":
						uiquit=1
						break
					if f.reftype=="quitx":
						print ("quit: onclick quit")
						quitflag=1
						break
					if f.quitab==1:
						uiquit=0
					if f.quitab==2:
						qpopflg=0
					if f.quitab==3:
						qmenuflg=0
	#if eventhappen==0:
	#	time.sleep(0.01)

		
	pygame.display.flip()
	pygame.event.pump()

print "updating main.sav Please Wait."
#clear keysav section.
for savk in keysav:
	keysav.remove(savk)
#add existing tracked keyids as specified in savkeys in ENGSYSTEM.xml
for ksav in savkeystag:
	keyid=ksav.attrib.get('keyid')
	if keyid!='0':
		if keyid in keylist:
			keysav.append(copy.deepcopy(ksav))
mainsavtree.write(os.path.join("launcher_data", "main.sav"))
print "Done."
sys.exit()