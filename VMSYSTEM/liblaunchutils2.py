#!/usr/bin/env python
import VMSYSTEM.libvmui as vmui
import VMSYSTEM.libvmconf as libvmconf
import VMSYSTEM.libthemeconf as libthemeconf
import pygame
import time
import copy
import sys
import os
import traceback
pygame.font.init()
simplefont = pygame.font.SysFont(None, 19)

framebg=libthemeconf.hudbg
frametext=libthemeconf.hudtext
framebtn=libthemeconf.btnbg2
framediv=libthemeconf.huddiv
#frametext=libthemeconf.hudt

hudy=20
fpad=1

Plugpath="plugins"

constext=([""] * 100)
#consfull=[]
#print constext

def consolewrite(string):
	global constext
	#global consfull
	constext.pop(0)
	constext.append(string)
	#consfull.append(string)
	print ("Con: " + string)

#sig method:
#sig must be a list of arguments or be None
#list of sig return codes:
#(0, widinstance)=activate the pre-initalized wid widinstance
#(1, x)=close self. x=0: call self's close method. 1=don't call close method.
#None=do nothing
#
#
##special sigs:
#("TASKMAN", code, taskid)=used ONLY by taskman. (the host program keeps track of the taskid's authorized to use this)
#code=0 close taskid, code=1 bring taskid to top and reset its x & y values.
PLUGINDUMMY=pygame.image.load(os.path.join("VMSYSTEM", "GFX", "launch", 'dummy.png'))

pluglist=list()

class plugobj:
	def __init__(self, classref, execname, label, direc=None, icon=None, catid=None):
		self.classref=classref
		self.icnpath=icon
		self.execname=execname
		self.label=label
		self.direc=direc
		self.catid=catid
		if self.direc!=None:
			if self.icnpath!=None:
				self.icon=pygame.image.load(os.path.join(Plugpath, self.direc, self.icnpath))
			else:
				self.icon=PLUGINDUMMY
		else:
			self.icon=PLUGINDUMMY

#tool lookup function.
def widlookup(namestring):
	#if namestring=="TEST":
	#	return testwid
	#if namestring=="scribble": -moved to plugin
	#	return scribble
	#if namestring=="credits": -moved to plugin
	#	return qcred
	#if namestring=="taskman":
	#	return taskman
	if namestring=="LaunchConsole":
		return launchconsole

#standardized rect generation
def getframes(x, y, widsurf):
	y -= 21
	x -= 1
	widbox=widsurf.get_rect()
	widbox.x=x+fpad
	widbox.y=y+hudy+fpad
	framebox=pygame.Rect(x, y, (widbox.w + fpad + fpad), (widbox.h + fpad + hudy + fpad))
	closebtnrect=pygame.Rect(x, y, hudy, hudy)
	return (widbox, framebox, closebtnrect)
	
#standardized frame drawing
def drawframe(framerect, closerect, widbox, widsurf, screensurf, title):
	pygame.draw.rect(screensurf, framebg, framerect, 0)
	pygame.draw.rect(screensurf, framediv, framerect, 1)
	pygame.draw.rect(screensurf, framebtn, closerect, 0)
	pygame.draw.rect(screensurf, framediv, closerect, 1)
	pygame.draw.line(screensurf, framediv, (framerect.x, framerect.y+hudy), ((framerect.x + framerect.w - 1), framerect.y+hudy))
	screensurf.blit(widsurf, widbox)
	labtx=simplefont.render(title, True, frametext, framebg)
	screensurf.blit(labtx, ((framerect.x + 25), (framerect.y + 1)))
	

#taskman is a special case. due to the nature of it.
class taskman:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		consolewrite("Taskman: running")
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="Taskman"
		#taskid is set automatically
		self.taskid=0
		self.argument=argument
		self.widx=300
		self.widy=500
		#x and y are required.
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy))
		self.widsurf.fill(framebg)
		
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
		self.closetasktx=simplefont.render("Close Task", True, framebg, frametext)
		self.bringtoptx=simplefont.render("Bring to top", True, framebg, frametext)
		self.seltask=None
		self.sigret=None
	def render(self):
		self.texty=20
		self.textx=0
		self.taskdict=dict()
		self.widsurf.fill(framebg)
		#copy and sort raw tasklist given to taskman by host program
		self.argumentcopy=list(self.argument)
		self.argumentcopy.sort(key=lambda x: x.taskid, reverse=False)
		#tasklist parser
		for self.task in self.argumentcopy:
			if self.seltask==self.task.taskid:
				self.labtx=simplefont.render(("Name: " + self.task.title + " | Order: " + str(self.task.wo) + " | taskid: " + str(self.task.taskid)), True, framebg, frametext)
			else:
				self.labtx=simplefont.render(("Name: " + self.task.title + " | Order: " + str(self.task.wo) + " | taskid: " + str(self.task.taskid)), True, frametext, framebg)
			self.clickbx=self.widsurf.blit(self.labtx, (self.textx, self.texty))
			self.clickbx.x += self.x
			self.clickbx.y += self.y
			self.taskdict[self.task.taskid]=self.clickbx
			self.texty += 18
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title)
		#task commands
		self.clx=self.screensurf.blit(self.closetasktx, (self.x, self.y))
		self.topx=self.screensurf.blit(self.bringtoptx, (self.x+5+self.closetasktx.get_width(), self.y))
	def movet(self, xoff, yoff):
		self.x -= xoff
		self.y -= yoff
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		self.closerect=self.frametoup[2]
		self.widbox=self.frametoup[0]
		self.framerect=self.frametoup[1]
	def click(self, event):
		if self.seltask not in self.taskdict:
			self.seltask=None
		#task commands logic
		if self.seltask!=None:
			if self.clx.collidepoint(event.pos)==1:
				self.sigret=("TASKMAN", 0, self.seltask)
			elif self.topx.collidepoint(event.pos)==1:
				self.sigret=("TASKMAN", 1, self.seltask)
			else:
				self.sigret=None
		else:
			self.sigret=None
		#task selector
		for self.taskc in self.taskdict:
			if self.taskdict[self.taskc].collidepoint(event.pos)==1:
				self.seltask=self.taskc
				#print self.seltask
				return
	def clickup(self, event):
		return
	def keydown(self, event):
		return
	def keyup(self, event):
		return
	def close(self):
		return
	def hostquit(self):
		return
	def sig(self):
		return self.sigret


class launchconsole:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="Console"
		#taskid is set automatically
		self.taskid=0
		self.yjump=16
		self.widx=500
		self.conscope=20
		self.conoffset=0
		self.widy=(self.conscope * self.yjump)
		
		self.consbak=list()
		#x and y are required.
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy))
		self.widsurf.fill(framebg)
		
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
		self.redraw=0
		self.scrdrg=0
		#print constext[(len(constext)-self.conscope+self.conoffset):(len(constext)-self.conoffset)]
		#print -self.conscope+self.conoffset
		#print -self.conoffset
		consolewrite("Console: Use mouse wheel or UP/DOWN to scroll")
	def render(self):
		#scrollbar arithetic
		if self.scrdrg==1:
			self.redraw=1
			self.scrlb=(100 * float(self.conscope)/float(len(constext)))
			self.scrloff=(100 * float(self.conoffset-len(constext))/float(len(constext)))
			self.scrlfull=300
			self.dy=self.sy
			self.mpos=pygame.mouse.get_pos()
			self.sy=(self.mpos[1])
			self.qy=self.dy-self.sy
			if self.qy<0:
				if not self.conscope+self.conoffset>=len(constext):
					self.conoffset+=abs(self.qy//3)
					#self.conoffset+1
			if self.qy>0:
				if self.conoffset!=0:
					self.conoffset-=abs(self.qy//3)
			if self.conscope+self.conoffset>len(constext):
				self.conoffset=(len(constext)-self.conscope)
			if self.conoffset<0:
				self.conoffset=0
			
		self.scrlb=(100 * float(self.conscope)/float(len(constext)))
		self.scrloff=(100 * float(self.conoffset)/float(len(constext)))
		self.scrlfull=300
		self.fullrect=pygame.Rect((self.x+self.widx-20), self.y, 20, (self.scrlfull + 1))
		self.partrect=pygame.Rect((self.x+self.widx-19), (self.y + (3 * self.scrloff)), 18, (3 * self.scrlb))
		#rendering
		if self.consbak!=constext:
			self.constbak=list(constext)
			self.texty=0
			self.widsurf.fill(framebg)
			for self.conline in constext[(len(constext)-(self.conscope+self.conoffset)):(len(constext)-self.conoffset)]:
				self.labtx=simplefont.render(self.conline, True, frametext, framebg)
				self.widsurf.blit(self.labtx, (0, self.texty))
				self.texty += self.yjump
		elif self.redraw==1:
			self.redraw=0
			self.texty=0
			self.widsurf.fill(framebg)
			for self.conline in constext[(len(constext)-(self.conscope+self.conoffset)):(len(constext)-self.conoffset)]:
				self.labtx=simplefont.render(self.conline, True, frametext, framebg)
				self.widsurf.blit(self.labtx, (0, self.texty))
				self.texty += self.yjump
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title)
		pygame.draw.rect(self.screensurf, frametext, self.fullrect, 0)
		pygame.draw.rect(self.screensurf, framebg, self.partrect, 0)
	def movet(self, xoff, yoff):
		self.x -= xoff
		self.y -= yoff
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		self.closerect=self.frametoup[2]
		self.widbox=self.frametoup[0]
		self.framerect=self.frametoup[1]
	#click is given pygame MOUSEBUTTONDOWN events that fall within widbox
	def click(self, event):
		if self.partrect.collidepoint(event.pos) and event.button==1:
			self.scrdrg=1
			self.sy=(event.pos[1])
			self.redraw=1
		if event.button==4:
			if not self.conscope+self.conoffset>=len(constext):
				self.conoffset+=1
				self.redraw=1
		if event.button==5:
			if self.conoffset!=0:
				self.conoffset-=1
				self.redraw=1
	#similar to click, except it receves MOUSEBUTTONUP events that fall within widbox.
	def clickup(self, event):
		if self.scrdrg==1:
			self.scrdrg=0
		return
	#keydown and keyup are given pygame KEYDOWN and KEYUP events.
	def keydown(self, event):
		if event.key==pygame.K_UP:
			if not self.conscope+self.conoffset>=len(constext):
				self.conoffset+=1
				self.redraw=1
		elif event.key==pygame.K_DOWN:
			if self.conoffset!=0:
				self.conoffset-=1
				self.redraw=1
		return
	def keyup(self, event):
		return
	#close is called when the window is to be closed.
	def close(self):
		return
	#hostquit is called when the host program is going to quit.
	def hostquit(self):
		return 
	def sig(self):
		return


for plugcodefile in os.listdir(Plugpath):
	if plugcodefile.lower().endswith(".sdap.py"):
		PLUGFILE=open(os.path.join(Plugpath, plugcodefile), 'r')
		try:
			PLUGEXEC=compile(PLUGFILE.read(), os.path.join(Plugpath, plugcodefile), 'exec')
			exec(PLUGEXEC)
			pluginst=plugobj(SDAPPLUGREF, SDAPNAME, SDAPLABEL, SDAPDIR, SDAPICON, SDAPCAT)
			pluglist.extend([pluginst])
			consolewrite("Load plugin: " + SDAPNAME)
		except SyntaxError as err:
			consolewrite("Plugin failure: SyntaxError on " + plugcodefile)
			print(traceback.format_exc())
			for errline in vmui.listline(str(err)):
				consolewrite(errline)
		
		


