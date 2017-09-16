#!/usr/bin/env python
import VMSYSTEM.libvmui as vmui
import VMSYSTEM.libvmconf as libvmconf
import VMSYSTEM.libthemeconf as libthemeconf
import VMSYSTEM.libbaltcalc as libbaltcalc
import pygame
import time
import copy
import sys
import os
import traceback

pygame.font.init()
simplefont = pygame.font.SysFont(None, 19)
monofont = pygame.font.SysFont("Mono", 16)
#monofont.set_bold(True)

titlebg=libthemeconf.titleactbg
titletext=libthemeconf.titleacttext
titleinactbg=libthemeconf.titleinactbg
titleinacttext=libthemeconf.titleinacttext
framebg=libthemeconf.hudbg
frametext=libthemeconf.hudtext
framebtn=libthemeconf.btnbg2
framebtntext=libthemeconf.btntext
framediv=libthemeconf.huddiv
shellbg=libthemeconf.consbg
shelltext=libthemeconf.constext
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

#que method:
#que is a system of inter-application communication.
#que codes:
#(0, arguments) = generic data
#(1, arguments) = image data
#(2, arguments) = text
#(100, arguments) = shell query (used by Shell), any responses should be in a list, 1 string per line
#(101) = shell status check (used by Shell at regular interval, no arguments sent.), any responses should be in a list, 1 string per line
#(102) = shell ready (used by Shell during shell startup, no arguments sent.), any responses should be in a list, 1 string per line
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
	if namestring=="shell":
		return shell

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
def drawframe(framerect, closerect, widbox, widsurf, screensurf, title, wo):
	if wo==0:
		pygame.draw.rect(screensurf, titlebg, framerect, 0)
		pygame.draw.rect(screensurf, framediv, framerect, 1)
		pygame.draw.rect(screensurf, framebtn, closerect, 0)
		pygame.draw.line(screensurf, framebtntext, (closerect.x+4, closerect.y+4), (closerect.x+14, closerect.y+14), 3)
		pygame.draw.line(screensurf, framebtntext, (closerect.x+14, closerect.y+4), (closerect.x+4, closerect.y+14), 3)
		pygame.draw.rect(screensurf, framediv, closerect, 1)
		pygame.draw.line(screensurf, framediv, (framerect.x, framerect.y+hudy), ((framerect.x + framerect.w - 1), framerect.y+hudy))
		screensurf.blit(widsurf, widbox)
		labtx=simplefont.render(title, True, titletext, titlebg)
		screensurf.blit(labtx, ((framerect.x + 25), (framerect.y + 1)))
	else:
		pygame.draw.rect(screensurf, titleinactbg, framerect, 0)
		pygame.draw.rect(screensurf, framediv, framerect, 1)
		pygame.draw.rect(screensurf, framebtn, closerect, 0)
		pygame.draw.line(screensurf, framebtntext, (closerect.x+4, closerect.y+4), (closerect.x+14, closerect.y+14), 3)
		pygame.draw.line(screensurf, framebtntext, (closerect.x+14, closerect.y+4), (closerect.x+4, closerect.y+14), 3)
		pygame.draw.rect(screensurf, framediv, closerect, 1)
		pygame.draw.line(screensurf, framediv, (framerect.x, framerect.y+hudy), ((framerect.x + framerect.w - 1), framerect.y+hudy))
		screensurf.blit(widsurf, widbox)
		labtx=simplefont.render(title, True, titleinacttext, titleinactbg)
		screensurf.blit(labtx, ((framerect.x + 25), (framerect.y + 1)))
	
#Plugin Loader
for plugcodefile in os.listdir(Plugpath):
	if plugcodefile.lower().endswith(".sdap.py"):
		PLUGFILE=open(os.path.join(Plugpath, plugcodefile), 'r')
		try:
			PLUGEXEC=compile(PLUGFILE.read(), os.path.join(Plugpath, plugcodefile), 'exec')
			exec(PLUGEXEC)
			pluginst=plugobj(SDAPPLUGREF, SDAPNAME, SDAPLABEL, SDAPDIR, SDAPICON, SDAPCAT)
			pluglist.extend([pluginst])
			consolewrite("Load plugin: " + SDAPNAME + " (" + plugcodefile + ")")
		except SyntaxError as err:
			consolewrite("Plugin failure: SyntaxError on " + plugcodefile)
			print(traceback.format_exc())
			for errline in vmui.listline(str(err)):
				consolewrite(errline)

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
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title, self.wo)
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
	def que(self, signal):
		return


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
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title, self.wo)
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
	def que(self, signal):
		return

class shell:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="Shell - test mode"
		#taskid is set automatically
		self.taskid=0
		self.yjump=16
		self.argument=argument
		if self.argument!=None:
			self.title="Shell - " + self.argument.title
		self.widx=((monofont.size("_")[0])*60)+20
		self.conscope=20
		self.conoffset=0
		self.curoffset=0
		self.widy=(self.conscope * self.yjump) + self.yjump + 6
		self.textin=""
		self.consbak=list()
		#x and y are required.
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy))
		self.widsurf.fill(shellbg)
		self.shtext=([""] * 100)
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
		self.curstatus=1
		self.curcnt=0
		self.curpoint=40
		self.shellstart=1
		self.inputrect=pygame.Rect(0, (self.widy-self.yjump-4), self.widx, (self.yjump+4))
		#print self.shtext[(len(self.shtext)-self.conscope+self.conoffset):(len(self.shtext)-self.conoffset)]
		#print -self.conscope+self.conoffset
		#print -self.conoffset
	def render(self):
		if self.shellstart==1:
			self.shellstart=0
			if self.argument!=None:
				self.retlist=self.argument.que([102])
				if self.retlist!=None:
					for self.line in self.retlist:
						self.shellwrite(self.line)
		if self.argument!=None:
			self.retlist=self.argument.que([101])
			if self.retlist!=None:
				for self.line in self.retlist:
					self.shellwrite(self.line)
		#scrollbar arithetic
		if self.curcnt<self.curpoint:
			self.curcnt += 1
		else:
			self.curcnt=0
			if self.curstatus==1:
				self.curstatus=0
				self.redraw=1
			else:
				self.curstatus=1
				self.redraw=1
		if self.curstatus==1:
			self.textinD=vmui.charinsert(self.textin, "|", (self.curoffset + 1))
		else:
			self.textinD=vmui.charinsert(self.textin, " ", (self.curoffset + 1))
		self.textinD=(">" + self.textinD)
		if self.scrdrg==1:
			self.redraw=1
			self.scrlb=(100 * float(self.conscope)/float(len(self.shtext)))
			self.scrloff=(100 * float(self.conoffset-len(self.shtext))/float(len(self.shtext)))
			self.scrlfull=300
			self.dy=self.sy
			self.mpos=pygame.mouse.get_pos()
			self.sy=(self.mpos[1])
			self.qy=self.dy-self.sy
			if self.qy<0:
				if not self.conscope+self.conoffset>=len(self.shtext):
					self.conoffset+=abs(self.qy//3)
					#self.conoffset+1
			if self.qy>0:
				if self.conoffset!=0:
					self.conoffset-=abs(self.qy//3)
			if self.conscope+self.conoffset>len(self.shtext):
				self.conoffset=(len(self.shtext)-self.conscope)
			if self.conoffset<0:
				self.conoffset=0
			
		self.scrlb=(100 * float(self.conscope)/float(len(self.shtext)))
		self.scrloff=(100 * float(self.conoffset)/float(len(self.shtext)))
		self.scrlfull=300
		self.fullrect=pygame.Rect((self.x+self.widx-20), self.y, 20, (self.scrlfull + 1))
		self.partrect=pygame.Rect((self.x+self.widx-19), (self.y + (3 * self.scrloff)), 18, (3 * self.scrlb))
		#rendering
		if self.consbak!=self.shtext:
			self.constbak=list(self.shtext)
			self.texty=0
			self.widsurf.fill(shellbg)
			for self.conline in self.shtext[(len(self.shtext)-(self.conscope+self.conoffset)):(len(self.shtext)-self.conoffset)]:
				self.labtx=monofont.render(self.conline, True, shelltext, shellbg)
				self.widsurf.blit(self.labtx, (0, self.texty))
				self.texty += self.yjump
			self.labtx=monofont.render(self.textinD, True, shelltext, shellbg)
			pygame.draw.rect(self.widsurf, shellbg, self.inputrect, 0)
			pygame.draw.rect(self.widsurf, shelltext, self.inputrect, 1)
			self.widsurf.blit(self.labtx, ((self.inputrect.x + 2), (self.inputrect.y + 2)))
		elif self.redraw==1:
			self.redraw=0
			self.texty=0
			self.widsurf.fill(shellbg)
			for self.conline in self.shtext[(len(self.shtext)-(self.conscope+self.conoffset)):(len(self.shtext)-self.conoffset)]:
				self.labtx=monofont.render(self.conline, True, shelltext, shellbg)
				self.widsurf.blit(self.labtx, (0, self.texty))
				self.texty += self.yjump
			self.labtx=monofont.render(self.textinD, True, shelltext, shellbg)
			pygame.draw.rect(self.widsurf, shellbg, self.inputrect, 0)
			pygame.draw.rect(self.widsurf, shelltext, self.inputrect, 1)
			self.widsurf.blit(self.labtx, ((self.inputrect.x + 2), (self.inputrect.y + 2)))
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title, self.wo)
		pygame.draw.rect(self.screensurf, frametext, self.fullrect, 0)
		pygame.draw.rect(self.screensurf, framediv, self.fullrect, 1)
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
			if not self.conscope+self.conoffset>=len(self.shtext):
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
			if not self.conscope+self.conoffset>=len(self.shtext):
				self.conoffset+=1
				self.redraw=1
		elif event.key==pygame.K_DOWN:
			if self.conoffset!=0:
				self.conoffset-=1
				self.redraw=1
		#elif event.key==pygame.BACKSPACE:
		#home/end support.
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_HOME:
			if self.curoffset!=0:
				self.curoffset=0
				self.redraw=1
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_END:
			if self.curoffset!=len(self.textin):
				self.curoffset=len(self.textin)
				self.redraw=1
		#cursor movement
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
			if self.curoffset!=0:
				self.curoffset -= 1
				self.redraw=1
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
			if self.curoffset!=len(self.textin):
				self.curoffset += 1
				self.redraw=1
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
			self.shellwrite(">" + self.textin)
			if self.argument!=None:
				self.retlist=self.argument.que([100, self.textin])
				if self.retlist!=None:
					for self.line in self.retlist:
						self.shellwrite(self.line)
			self.curoffset=0
			self.textin=""
			self.conoffset=0
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
			if len(self.textin)!=0 and self.curoffset!=0:
				self.textin=vmui.charremove(self.textin, self.curoffset)
				self.curoffset -= 1
				self.redraw=1
		elif event.type == pygame.KEYDOWN and event.key != pygame.K_TAB:
			self.curoffset += 1
			self.textin=vmui.charinsert(self.textin, str(event.unicode), self.curoffset)
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
	def que(self, signal):
		return
	def shellwrite(self, string):
		self.shtext.pop(0)
		self.shtext.append(string[0:60])
		if len(string)>60:
			consolewrite("Shell: Warning: line of text too long... clipping...")


		
		


