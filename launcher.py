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
import VMSYSTEM.libvmui as vmui
import VMSYSTEM.libvmconf as libvmconf
import VMSYSTEM.libthemeconf as libthemeconf
import VMSYSTEM.liblaunchutils2 as launchutils
import VMSYSTEM.libfilevirtual as libfilevirtual

import traceback

print "SBTCVM Desktop v3.0"
pygame.display.init()
pygame.font.init()

simplefontC = pygame.font.SysFont(None, 28)
simplefontB = pygame.font.SysFont(None, 19)
tilefont = pygame.font.SysFont(None, 19)
catfont = pygame.font.SysFont(None, 19)

pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN])
pygame.display.set_caption(("SBTCVM Desktop"), ("SBTCVM Desktop"))

windowicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'icon.png'))
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((800, 600), pygame.RESIZABLE)
screenx=800
screeny=600
vmui.initui(screensurf, 1)

diagabt="""SBTCVM Desktop v3.0
Part of the SBTCVM Project
Copyright (c) 2016-2017 Thomas Leathers and Contributors

See README.md for more information."""

#image data:
#bghud=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'launchhud.png')).convert_alpha()
#bghud=pygame.Surface((screenx, screeny), SRCALPHA)



bg=(libthemeconf.bgmake(None)).convert()

sbtcvmbadge=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'SBTCVMbadge.png')).convert()
bgoverlay=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'helpbgover.png')).convert_alpha()

gtticn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'gtt.png')).convert()
introicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'intro.png')).convert()

DUMMY=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'dummy.png')).convert()
helpicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'help.png')).convert()
fvicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'fileview.png')).convert()
filemanicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'fileman.png')).convert()
settingsicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'settings.png')).convert()
themeicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'theme.png')).convert()

calcicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'calc.png')).convert()
#creditsicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'credits.png')).convert()

romicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'ROM.png')).convert()
#miniscribble=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'miniscribble.png')).convert()
taskmanicn=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'taskman.png')).convert()
consoleicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'console.png')).convert()
sysshellicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'sysshell.png')).convert()

#fvfilemenu=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'fvfilemenu.png')).convert()
fmicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'filemenuicon.png')).convert_alpha()
fvfilemenu=vmui.makemenubtn("FILE", icon=fmicon).convert()
fvcatmenu=vmui.makemenubtn("CATEGORY", width=80).convert()
fvsystemmenu=vmui.makemenubtn("SYSTEM", width=60).convert()
#fvcatmenu=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'catmenu.png')).convert()

def errorreport(widtitle, area, err):
	global scupdate
	launchutils.consolewrite(">>ERROR in: \"" + widtitle + "\" terminating")
	launchutils.consolewrite(">>Area: " + area)
	print(traceback.format_exc())
	errdiagtxt=("Error In: \"" + widtitle + "\" terminating... \n Area: " + area + " \n see Standard output for traceback. \n\"" + str(err) + "\"")
	vmui.okdiag(errdiagtxt, (screenx // 2), (screeny // 2))
	for errline in vmui.listline(str(err)):
		launchutils.consolewrite(errline)
	scupdate=1

#"fake" program class passed to shell for system shell.
systemshellhelp="""SBTCVM Desktop - System Shell.
          help : this text
           dir : list current directory
            ls : list current directory
cd [directory] : change to specified directory
          cd.. : macro for moving up one directory.
        shtest : test shell
         tasks : list tasks
       taskman : start task manager
       console : start console"""
class sysshellque:
	def __init__(self):
		self.title="SYSTEM"
		#all system-level class objects have a taskid of -1.
		self.taskid=-1
		self.qstart=None
		self.pathlist=['.']
		self.pathstr='.'
		self.title="SYSTEM - " + self.pathstr
	def QSTART(self):
		self.qstartX=self.qstart
		self.qstart=None
		return self.qstartX
	def que(self, signal):
		if signal[0]==102:
			return ["System Shell ready. Type help for help."]
		if signal[0]==101:
			return
		if signal[0]==100:
			self.cmd=((signal[1]).split(" "))[0].lower()
			if self.cmd=="taskman":
				self.qstart="taskman"
				return ["Launching Taskman"]
			if self.cmd=="console":
				self.qstart="console"
				return ["Launching Console"]
			if self.cmd=="shtest":
				return ["Shell working."]
			if self.cmd=="help":
				return vmui.listline(systemshellhelp)
			#directory navigation
			if self.cmd=="dir" or self.cmd=="ls":
				return libfilevirtual.dirlist(self.pathlist)
			if self.cmd=="cd..":
				self.pathlist=libfilevirtual.dir_cdup(self.pathlist)
				self.pathstr=os.path.join(*self.pathlist)
				self.title="SYSTEM - " + self.pathstr
			if self.cmd=="cd":
				try:
					self.dirstr=((signal[1]).split(" "))[1]
				except IndexError:
					return ["Error: please specify path!"]
				self.tmplist=libfilevirtual.dir_cd(self.pathlist, self.dirstr)
				if self.tmplist==None:
					return ["Error: Path Not Found"]
				else:
					self.pathlist=self.tmplist
				self.pathstr=os.path.join(*self.pathlist)
				self.title="SYSTEM - " + self.pathstr
			#task listing
			if self.cmd=="tasks":
				self.retlist=[]
				for self.task in activewids:
					self.retlist.extend([("Name: " + self.task.title + " | Order: " + str(self.task.wo) + " | taskid: " + str(self.task.taskid))])
				return self.retlist
ShellSystem=sysshellque()
class launchtile:
	def __init__(self, label, icon, ltype, lref=None, lref2=None):
		self.label=label
		self.textren=tilefont.render(self.label, True, libthemeconf.tiletext)
		self.icon=icon
		self.ltype=ltype
		self.lref=lref
		self.lref2=lref2
		self.tileh=90
		self.tilew=90
		self.iconw=60
		self.iconh=60
		self.tilebox=pygame.Rect(0, 0, self.tileh, self.tilew)
		self.tilesurf=pygame.Surface((self.tilew, self.tileh), SRCALPHA).convert_alpha()
		self.tilesurf.fill(libthemeconf.tilecolor)
		self.textx=((self.tileh // 2) - (self.textren.get_width() // 2))
		self.iconx=((self.tileh // 2) - (self.icon.get_width() // 2))
		self.icony=3
		self.texty=(self.icony+self.iconh+3)
		self.tilesurf.blit(self.icon, (self.iconx, self.icony))
		self.tilesurf.blit(self.textren, (self.textx, self.texty))
		if ltype==5:
			self.plusrect1=pygame.Rect(6, 2, 4, 12)
			self.plusrect2=pygame.Rect(2, 6, 12, 4)
			pygame.draw.rect(self.tilesurf, libthemeconf.tiletext, self.plusrect1, 0)
			pygame.draw.rect(self.tilesurf, libthemeconf.tiletext, self.plusrect2, 0)
		
	def render(self, xpos, ypos):
		self.tilebox=bg.blit(self.tilesurf, (xpos, ypos))
	def act(self):
		if self.ltype==4:
			return "taskman"
		if self.lref!=None:
			if self.ltype==0:
				if self.lref2!=None:
					subprocess.Popen(["python", self.lref, self.lref2])
				else:
					subprocess.Popen(["python", self.lref])
			if self.ltype==3:
				if self.lref2!=None:
					return (self.lref, self.lref2)
				else:
					return (self.lref, None)
			if self.ltype==5:
				return (self.lref, None, None)
			if self.ltype==1:
				subprocess.Popen(["python", "MK2-RUN.py", "-k", self.lref])
			if self.ltype==2:
				subprocess.Popen(["python", "MK2-RUN.py", self.lref])
			
#create launchtile objects
helpt=launchtile("Help", helpicn, 0, lref="helpview.py")
filet=launchtile("FileView", fvicn, 0, lref="fileview2.py")
settingt=launchtile("Settings", settingsicn, 0, lref="settings.py")
themet=launchtile("Theme", themeicn, 0, lref="theme.py")

calct=launchtile("Calc", calcicn, 0, lref="calc.py")
#creditt=launchtile("Credits", creditsicn, 3, lref="credits")
introt=launchtile("intro", introicn, 1, lref="intro.streg")
gttt=launchtile("GTT", gtticn, 2, lref="gtt.streg")
starryt=launchtile("Starry", romicon, 2, lref="starry.streg")
rayburstt=launchtile("Ray Burst", romicon, 2, lref="rayburst.streg")
dazzlet=launchtile("Dazzle", romicon, 1, lref="dazzle.streg")
pixelpatt=launchtile("Pixel Patterns", romicon, 2, lref="pixelpat.streg")
#launch tools
#widtest=launchtile("Test tool", DUMMY, 3, lref="TEST")
#widscribble=launchtile("Scribble", miniscribble, 3, lref="scribble")
#widcred=launchtile("credits", DUMMY, 3, lref="credits")
TASKMAN=launchtile("Task Manager", taskmanicn, 4)
LAUNCHCON=launchtile("Console", consoleicon, 3, lref="LaunchConsole")
LAUNCHSHELL=launchtile("System Shell", sysshellicon, 3, lref="shell", lref2=ShellSystem)
LAUNCHFILE=launchtile("File Manager", filemanicon, 3, lref="fileman")

#testwid=launchutils.testwid(screensurf, 40, 40)

activewids=[]

#category lists
maincat=[filet, calct, settingt, themet, helpt]
gamescat=[gttt]
welcomecat=[introt]
democat=[introt, starryt, rayburstt, dazzlet, pixelpatt]
ltoolcat=[TASKMAN, LAUNCHCON, LAUNCHSHELL, LAUNCHFILE]
plugincat=[]

for plug in launchutils.pluglist:
	PLUGTILE=launchtile(plug.label, plug.icon, 5, lref=plug.classref)
	plugincat.extend([PLUGTILE])
	if 0 in plug.catid:
		maincat.extend([PLUGTILE])
	if 1 in plug.catid:
		gamescat.extend([PLUGTILE])
	if 2 in plug.catid:
		welcomecat.extend([PLUGTILE])
	if 3 in plug.catid:
		democat.extend([PLUGTILE])
	if 4 in plug.catid:
		ltoolcat.extend([PLUGTILE])

#category definitions
tilelist=maincat
catid=0
catname="Main"

#categoru menu
cmitem0=vmui.menuitem("Main", "MAIN")
cmitem1=vmui.menuitem("Games", "GAMES")
cmitem2=vmui.menuitem("Welcome", "WELCOME")
cmitem3=vmui.menuitem("Demos", "DEMOS")
cmitem4=vmui.menuitem("Mini Tools", "LTOOL")
cmitem5=vmui.menuitem("Plugins", "PLUG")
catmenu=[cmitem0, cmitem1, cmitem2, cmitem3, cmitem4, cmitem5]


#widitem0=vmui.menuitem("main", 

#file menu
fmhelp=vmui.menuitem("Help", "HELP")
fmabout=vmui.menuitem("About Desktop", "ABOUT")
fmabout2=vmui.menuitem("readme", "ABOUT2")
fmtask=vmui.menuitem("Task Manager", "TASKMAN")
fmcon=vmui.menuitem("Console", "CON")
fmbg=vmui.menuitem("Background", "SETBG")
fmquit=vmui.menuitem("Quit", "QUIT")
filemenu=[fmhelp, fmabout, fmabout2, fmbg, fmquit]

#system menu
sysyssh=vmui.menuitem("Shell", "SYSSHELL")
sytask=vmui.menuitem("Task Manager", "TASKMAN")
sycon=vmui.menuitem("Console", "CON")
syfile=vmui.menuitem("Fileman", "FILEMAN")
syscshot=vmui.menuitem("Screenshot", "SCSHOT")
systemmenu=[sysyssh, syfile, sytask, sycon, syscshot]

versnumgfx=simplefontB.render("v2.0.3", True, libthemeconf.hudtext)

bg.blit(bgoverlay, ((screenx - 250), (screeny - 250)))

pygame.key.set_repeat(250, 50)

movewid=0
widtomove=None

scupdate=1
qflg=0
resizeflg=0
uptcat=1
redrawhud=1
taskidcnt=0
fullredraw=0

#wids hidden from task switcher bar
hiddenwids=list()
uptlist=list()

hudtasksw=launchutils.hudswitch(screensurf, 0, 200, 0, [activewids, hiddenwids])
hudtasksw.taskid=taskidcnt
hudtaskswid=taskidcnt
activewids.extend([hudtasksw])
hiddenwids.extend([taskidcnt])
taskidcnt += 1

#keep track of taskman taskids. (to prevent sneaky programs from messing with things...)
taskmanlist=list()
launchutils.consolewrite(">>SBTCVM Desktop v3.0")
while qflg==0:
	#pygame window resize logic
	if resizeflg==1:
		resizeflg=2
	elif resizeflg==2:
		if resw<300:
			resw=300
		if resh<300:
			resh=300
		screensurf=pygame.display.set_mode((resw, resh), pygame.RESIZABLE)
		bg=(libthemeconf.bgmake(None)).convert()
		bg=pygame.transform.scale(bg, (resw, resh))
		scupdate=1
		resizeflg=0	
		screeny=resh
		screenx=resw
		bg.blit(bgoverlay, ((screenx - 250), (screeny - 250)))
		hudtasksw.resizet(0, 0)
		redrawhud=1
	elif fullredraw==1:
		fullredraw=0
		bg=(libthemeconf.bgmake(None)).convert()
		bg=pygame.transform.scale(bg, (screenx, screeny))
		bg.blit(bgoverlay, ((screenx - 250), (screeny - 250)))
		redrawhud=1
	#hud rendering. (draws onto bg)
	if redrawhud==1:
		redrawhud=0
		hudrect=pygame.Rect(0, 0, screenx, 44)
		pygame.draw.rect(bg, libthemeconf.hudbg, hudrect, 0)
		bg.blit(sbtcvmbadge, ((screenx-120), 0))
		bg.blit(versnumgfx, ((screenx - versnumgfx.get_width() - 10), 30))
		#
		filemx=bg.blit(fvfilemenu, (3, 3))
		sysmx=bg.blit(fvsystemmenu, (133, 3))
		uptcat=1
	#category button redraw (avoid full hud redraw on cat change
	if uptcat==1:
		uptcat=0
		catmx=bg.blit(fvcatmenu, (48, 3))
		menulabel=catfont.render(catname, True, libthemeconf.btntext)
		bg.blit(menulabel, ((48+40-(menulabel.get_width() // 2)), 5))
		tilex=10
		tiley=60
		tilejumpx=100
		tilejumpy=95
		
		#tile render
		for tile in tilelist:
			tile.render(tilex, tiley)
			if tilex+tilejumpx+90<screenx:
				tilex += tilejumpx
			else:
				tilex=10
				tiley += tilejumpy
	#display drawing
	if scupdate==1:
		scupdate=0
		screensurf.blit(bg, (0, 0))
		
		#minitool render
		activewids.sort(key=lambda x: x.wo, reverse=True)
		for wid in activewids:
			try:
				wid.render()
				uptlist.extend([wid.framerect])
			except Exception as err:
				errorreport(wid.title, "Render", err)
				activewids.remove(wid)
		pygame.display.update()
	else:
		#passive minitool renderer to keep minitools updated.
		uptlist=list()
		activewids.sort(key=lambda x: x.wo, reverse=True)
		for wid in activewids:
			try:
				#render should return either none or a list of updated areas.
				widrectret=wid.render()
				if widrectret==None:
					uptlist.extend([wid.framerect])
				else:
					uptlist=uptlist + widrectret
			except Exception as err:
				errorreport(wid.title, "Render", err)
				activewids.remove(wid)
		pygame.display.update(uptlist)
	#window movement
	if movewid==1:
		prevpos=movepos
		movepos=pygame.mouse.get_pos()
		xoff =(prevpos[0] - movepos[0])
		yoff =(prevpos[1] - movepos[1])
		try:
			widtomove.movet(xoff, yoff)
		except Exception as err:
			errorreport(wid.title, "Window Move", err)
			activewids.remove(widtomove)
			movewid=0
		scupdate=1
		time.sleep(0.04)
	elif movewid==2:
		prevpos=movepos
		movepos=pygame.mouse.get_pos()
		xoff =(prevpos[0] - movepos[0])
		yoff =(prevpos[1] - movepos[1])
		try:
			widtomove.resizet(xoff, yoff)
		except AttributeError:
			pass
		except Exception as err:
			errorreport(wid.title, "Window Move", err)
			activewids.remove(widtomove)
			movewid=0
		scupdate=1
		time.sleep(0.04)
	else:
		time.sleep(0.04)
	#ShellSystem processor
	shsysret=ShellSystem.QSTART()
	if shsysret=="taskman":
		try:
			widx=launchutils.taskman(screensurf, 0, 40, 80, argument=activewids)
			widx.taskid=taskidcnt
			taskidcnt +=1
			#ctivewids=activewids + [widx]
			for wid in activewids:
				wid.wo += 1
			activewids.extend([widx])
			taskmanlist.extend([widx.taskid])
		except Exception as err:
			errorreport("Taskman", "Init (TASKMAN)", err)
	if shsysret=="console":
		try:
			widx=launchutils.launchconsole(screensurf, 0, 40, 80)
			widx.taskid=taskidcnt
			taskidcnt +=1
			for wid in activewids:
				wid.wo += 1
			activewids.extend([widx])
		except Exception as err:
				errorreport("Console", "Init (Console)", err)
	#minitool sig processor	
	for wid in activewids:
		noerror=1
		try:
			widret=wid.sig()
		except Exception as err:
			errorreport(wid.title, "Signal Query", err)
			activewids.remove(wid)
			noerror=0
		if noerror==1:
			if widret!=None:
				if widret[0]==0:
					widadd=widret[1]
					for widd in activewids:
						widd.wo += 1
					widadd.movet(-40, -80)
					widadd.wo=0
					widadd.taskid=taskidcnt
					taskidcnt +=1
					activewids.extend([widadd])
				elif widret[0]==1:
					if widret[1]==0:
						wid.close()
					activewids.remove(wid)
					scupdate=1
				elif widret[0]=="TASKSWITCH" and wid.taskid==hudtaskswid:
					wid.sigret=None
					if widret[1]==0:
						for widq in activewids:
							widq.wo += 1
						for widd in activewids:
							if widd.taskid==widret[2]:
								#launchutils.consolewrite("Taskswitcher: bring task: \"" + widd.title + "\" Of TaskID: \"" + str(widd.taskid) + "\" To Front")
								widd.wo=0
								scupdate=1	
				elif widret[0]=="TASKMAN" and wid.taskid in taskmanlist:
					#reset taskman's return variable.
					wid.sigret=None
					if widret[1]==0:
						for widd in activewids:
							if widd.taskid==widret[2]:
								if widret[2] not in hiddenwids:
									activewids.remove(widd)
									widd.close()
									scupdate=1
									launchutils.consolewrite("Taskman: Close task: \"" + widd.title + "\" Of TaskID: \"" + str(widd.taskid) + "\"")
								else:
									launchutils.consolewrite("Taskman: ERROR: CANNOT Close task: \"" + widd.title + "\"")
									launchutils.consolewrite("Of TaskID: \"" + str(widd.taskid) + "\"")
									launchutils.consolewrite("It is a protected task used by the system!")
					if widret[1]==1:
						if widret[2] not in hiddenwids:
							for widq in activewids:
								widq.wo += 1
							for widd in activewids:
								if widd.taskid==widret[2]:
									launchutils.consolewrite("Taskman: bring task: \"" + widd.title + "\" Of TaskID: \"" + str(widd.taskid) + "\" To Front")
									widd.wo=0
									widd.x=40
									widd.y=80
									widd.movet(0, 0)
									scupdate=1
						else:
							for widd in activewids:
								if widd.taskid==widret[2]:
									launchutils.consolewrite("Taskman: ERROR: CANNOT bring task: \"" + widd.title + "\"")
									launchutils.consolewrite("Of TaskID: \"" + str(widret[2]) + "\" To Front")
									launchutils.consolewrite("It is a protected task used by the system!")
									break

				elif widret[0]=="TASKMAN":
					launchutils.consolewrite(">>WARNING: Unauthorized use of TASKMAN signals was blocked.")
					launchutils.consolewrite(">>Task name: \"" + wid.title + "\" TaskID: \"" + str(wid.taskid) + "\"")
		
	#event handler
	for event in pygame.event.get():
		if event.type == QUIT:
			qflg=1
			for wid in activewids:
				try:
					wid.hostquit()
				except Exception as err:
					errorreport(wid.title, "Host Quit", err)
			break
		#free up these keys for applications...
		#if event.type == KEYDOWN and event.key == K_F1:
		#	subprocess.Popen(["python", "helpview.py", "launcher.xml"])
		#elif event.type == KEYDOWN and event.key == K_F8:
		#	pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-launcher.png')))
		#	break
		#minitool keyboard event processors.
		elif event.type == KEYDOWN:
			for wid in activewids:
				if wid.wo==0:
					try:
						wid.keydown(event)
					except Exception as err:
						errorreport(wid.title, "Keydown", err)
						activewids.remove(wid)
					break
		if event.type == KEYUP:
			for wid in activewids:
				if wid.wo==0:
					try:
						wid.keyup(event)
					except Exception as err:
						errorreport(wid.title, "Keyup", err)
						activewids.remove(wid)
					break
		#screen resize code activation
		if event.type==VIDEORESIZE:
			resizeflg=1
			resw=event.w
			resh=event.h
			time.sleep(0.1)
			break
		#mousebuttonup code 
		if event.type==MOUSEBUTTONUP:
			if movewid==1:
				movewid=0
			elif movewid==2:
				movewid=0
			else:
				for wid in activewids:
					if wid.wo==0:
						#if wid.widbox.collidepoint(event.pos)==1:
						try:
							wid.clickup(event)
						except Exception as err:
							errorreport(wid.title, "Clickup", err)
							activewids.remove(wid)
						break
		if event.type==MOUSEBUTTONDOWN:
			#minitool click processing
			notile=0
			#first=1
			activewids.sort(key=lambda x: x.wo, reverse=False)
			for wid in activewids:
				#if wid.wo==0 and first==1:
				#	print "fun"
				#first=0
				if wid.framerect.collidepoint(event.pos)==1:
					notile=1
					if not wid.widbox.collidepoint(event.pos)==1:
						if wid.closerect.collidepoint(event.pos)==1 and event.button==1:
							try:
								wid.close()
							except Exception as err:
								errorreport(wid.title, "Close", err)
							activewids.remove(wid)
							scupdate=1
							break
						elif event.pos[1]>(wid.y + wid.widbox.h):
							movewid=2
							movepos=event.pos
							widtomove=wid
							if wid.wo!=0:
								wid.wo=0
								activewids.remove(wid)
								for widd in activewids:
									widd.wo += 1
								activewids.extend([wid])
							break
						else:
							movewid=1
							movepos=event.pos
							widtomove=wid
							if wid.wo!=0:
								wid.wo=0
								activewids.remove(wid)
								for widd in activewids:
									widd.wo += 1
								activewids.extend([wid])
							break
							#activewids.insert(0, wid)
							#activewids.sort(key=lambda x: x.wo, reverse=True)
					else:
						try:
							wid.click(event)
						except Exception as err:
							errorreport(wid.title, "Click", err)
							activewids.remove(wid)
							break
							
						if wid.wo!=0:
							wid.wo=0
							scupdate=1
							activewids.remove(wid)
							for widd in activewids:
								widd.wo += 1
							activewids.extend([wid])
						break
			#tile click processing
			if notile==0:
				for tile in tilelist:
					if tile.tilebox.collidepoint(event.pos)==1 and event.button==1:
						actret=tile.act()
						if actret!=None:
							if actret=="taskman":
								#widis=launchutils.widlookup("taskman")
								try:
									widx=launchutils.taskman(screensurf, 0, 40, 80, argument=activewids)
									widx.taskid=taskidcnt
									taskidcnt +=1
									scupdate=1
									#ctivewids=activewids + [widx]
									for wid in activewids:
										wid.wo += 1
									activewids.extend([widx])
									taskmanlist.extend([widx.taskid])
								except Exception as err:
									errorreport("Taskman", "Init (TASKMAN)", err)
							elif len(actret)==3:
								widis=actret[0]
								try:
									widx=widis(screensurf, 0, 40, 80, argument=None)
									widx.taskid=taskidcnt
									taskidcnt +=1
									scupdate=1
									#ctivewids=activewids + [widx]
									for wid in activewids:
										wid.wo += 1
									activewids.extend([widx])
								except Exception as err:
									errorreport("<INIT ERROR, SEE TRACEBACK>", "Init (plugin)", err)
								
							else:
								widis=launchutils.widlookup(actret[0])
								try:
									widx=widis(screensurf, 0, 40, 80, argument=actret[1])
									widx.taskid=taskidcnt
									taskidcnt +=1
									#ctivewids=activewids + [widx]
									for wid in activewids:
										wid.wo += 1
									scupdate=1
									activewids.extend([widx])
									#activewids.sort(key=lambda x: x.wo, reverse=True)
								except Exception as err:
									errorreport("<INIT ERROR, SEE TRACEBACK>", "Init (internal)", err)
							
							
				#file menu
				if filemx.collidepoint(event.pos)==1 and event.button==1:
					menuret=vmui.menuset(filemenu, 3, 43, reclick=0, fontsize=26)
					if menuret=="HELP":
						subprocess.Popen(["python", "helpview.py", "launcher.xml"])
					if menuret=="ABOUT2":
						subprocess.Popen(["python", "MK2-TOOLS.py", "textview", "README.md"])
					if menuret=="ABOUT":
						vmui.aboutdiag(diagabt, (screenx // 2), (screeny // 2))
					if menuret=="SETBG":
						vmui.settheme(3, 43)
						scupdate=1
						bg=(libthemeconf.bgmake(None)).convert()
						bg=pygame.transform.scale(bg, (screenx, screeny))
						bg.blit(bgoverlay, ((screenx - 250), (screeny - 250)))
						redrawhud=1
					if menuret=="QUIT":
						qflg=1
						for wid in activewids:
							try:
								wid.hostquit()
							except Exception as err:
								errorreport(wid.title, "Host Quit", err)
								
						break
				#system menu
				if sysmx.collidepoint(event.pos)==1 and event.button==1:
					menuret=vmui.menuset(systemmenu, 133, 43, reclick=0, fontsize=26)
					if menuret=="TASKMAN":
						try:
							#widis=launchutils.widlookup("taskman")
							widx=launchutils.taskman(screensurf, 0, 40, 80, argument=activewids)
							widx.taskid=taskidcnt
							taskidcnt +=1
							scupdate=1
							for wid in activewids:
								wid.wo += 1
							activewids.extend([widx])
							taskmanlist.extend([widx.taskid])
						except Exception as err:
								errorreport("Taskman", "Init (TASKMAN)", err)
					if menuret=="CON":
						try:
							widx=launchutils.launchconsole(screensurf, 0, 40, 80)
							widx.taskid=taskidcnt
							taskidcnt +=1
							scupdate=1
							for wid in activewids:
								wid.wo += 1
							activewids.extend([widx])
						except Exception as err:
								errorreport("Console", "Init (Console)", err)
					if menuret=="SYSSHELL":
						try:
							widx=launchutils.shell(screensurf, 0, 40, 80, argument=ShellSystem)
							widx.taskid=taskidcnt
							taskidcnt +=1
							scupdate=1
							for wid in activewids:
								wid.wo += 1
							activewids.extend([widx])
						except Exception as err:
								errorreport("Console", "Init (Shell)", err)
					if menuret=="FILEMAN":
						try:
							widx=launchutils.fileman(screensurf, 0, 40, 80)
							widx.taskid=taskidcnt
							taskidcnt +=1
							scupdate=1
							for wid in activewids:
								wid.wo += 1
							activewids.extend([widx])
						except Exception as err:
								errorreport("Console", "Init (Fileman)", err)
					if menuret=="SCSHOT":
						pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-launcher.png')))
				#category menu
				if catmx.collidepoint(event.pos)==1 and event.button==1:
					menuret=vmui.menuset(catmenu, 48, 43, reclick=0, fontsize=26)
					if menuret=="MAIN":
						tilelist=maincat
						catid=0
						catname="Main"
						scupdate=1
						uptcat=1
						fullredraw=1
					if menuret=="GAMES":
						tilelist=gamescat
						catid=1
						catname="Games"
						scupdate=1
						uptcat=1
						fullredraw=1
					if menuret=="WELCOME":
						tilelist=welcomecat
						catid=2
						catname="Welcome"
						scupdate=1
						uptcat=1
						fullredraw=1
					if menuret=="DEMOS":
						tilelist=democat
						catid=3
						catname="Demos"
						scupdate=1
						uptcat=1
						fullredraw=1
					if menuret=="LTOOL":
						tilelist=ltoolcat
						catid=4
						catname="Mini Tools"
						scupdate=1
						uptcat=1
						fullredraw=1
					if menuret=="PLUG":
						tilelist=plugincat
						catid=5
						catname="Plugins"
						scupdate=1
						uptcat=1
						fullredraw=1
	