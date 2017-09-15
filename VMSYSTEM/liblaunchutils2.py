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
	if namestring=="TEST":
		return testwid
	if namestring=="scribble":
		return scribble
	if namestring=="credits":
		return qcred
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

class testwid:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="TEST"
		#taskid is set automatically
		self.taskid=0
		
		self.widx=140
		self.widy=140
		#x and y are required.
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy))
		self.widsurf.fill(framebg)
		consolewrite("TEST: Test Tool running")
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
		self.newinstance=0
		self.selfquit=0
		self.testsigprotect1=0
	def render(self):
		self.labtx=simplefont.render("window order: " + str(self.wo), True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 0))
		self.labtx=simplefont.render("taskid: " + str(self.taskid), True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 20))
		self.labtx=simplefont.render("space = new instance", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 40))
		self.labtx=simplefont.render("q = close this window", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 60))
		self.labtx=simplefont.render("e = test sig protect 1", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 80))
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title)
	def movet(self, xoff, yoff):
		self.x -= xoff
		self.y -= yoff
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		self.closerect=self.frametoup[2]
		self.widbox=self.frametoup[0]
		self.framerect=self.frametoup[1]
	#click is given pygame MOUSEBUTTONDOWN events that fall within widbox
	def click(self, event):
		consolewrite("TEST: click")
	#similar to click, except it receves MOUSEBUTTONUP events that fall within widbox.
	def clickup(self, event):
		consolewrite("TEST: clickup")
	#keydown and keyup are given pygame KEYDOWN and KEYUP events.
	def keydown(self, event):
		consolewrite("TEST: Keydown")
		#print event.unicode
		if event.key==pygame.K_SPACE:
			self.newinstance=1
		if event.key==pygame.K_q:
			self.selfquit=1
		if event.key==pygame.K_e:
			self.testsigprotect1=1
	def keyup(self, event):
		consolewrite("TEST: Keyup")
	#close is called when the window is to be closed.
	def close(self):
		consolewrite("TEST: Window Close")
	#hostquit is called when the host program is going to quit.
	def hostquit(self):
		consolewrite("TEST: Host Program Quit")
	def sig(self):
		if self.newinstance==1:
			self.newinstance=0
			consolewrite("TEST: Sending mini tool launch signal")
			return (0, testwid(self.screensurf, 0))
		if self.testsigprotect1==1:
			self.testsigprotect1=0
			consolewrite("TEST: Testing Signal Protection on task closing.")
			return ("TASKMAN", 0, 0)
			
		if self.selfquit==1:
			self.selfquit=0
			consolewrite("TEST: Sending selfquit signal")
			return (1, 0)
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


class scribble:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="Scribble"
		#taskid is set automatically
		self.taskid=0
		
		self.widx=324
		self.widy=283
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy)).convert(self.screensurf)
		self.widsurf.fill(framebg)
		self.labtx=simplefont.render("click left box or use a,s,d to cycle color [27 colors]", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 0))
		self.labtx=simplefont.render("click the right box or use c to change pen size", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 20))
		self.labtx=simplefont.render("click inside this window to begin.", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 40))
		self.labtx=simplefont.render("z is undo, x is fill", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 60))
		self.paintsurf=pygame.Surface((self.widx, self.widy-40)).convert(self.widsurf)
		self.paintsurf.fill((255, 255, 255))
		self.paintsurfbak=self.paintsurf.copy()
		self.paintrect=self.paintsurf.get_rect()
		self.paintrect.x = (self.x)
		self.paintrect.y = (self.y)
		self.pensize=1
		self.color1rect=pygame.Rect(self.x, (self.y + self.widy - 38), 30, 30)
		#self.sizesmall=pygame.Rect(self.x + 30, (self.y + self.widy - 40), self.pensize, self.pensize)
		self.sizerect=pygame.Rect(self.x + 32, (self.y + self.widy - 38), 30, 30)
		self.penlist=[1, 2, 3, 4, 5, 7, 9, 10, 15, 20, 30]
		self.penindex=0
		self.colorr=0
		self.colorb=0
		self.colorg=0
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		self.scrib=0
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
		self.firstclick=1
		self.redraw=0
	def render(self):
		self.scribblecolor=(self.colorr, self.colorg, self.colorb)
		if self.firstclick==2:
			self.firstclick=0
			self.widsurf.blit(self.paintsurf, (0, 0))
		if self.redraw==1:
			self.redraw=0
			self.widsurf.blit(self.paintsurf, (0, 0))
		if self.scrib==1:
			self.dx=self.sx
			self.dy=self.sy
			self.mpos=pygame.mouse.get_pos()
			self.sx=(self.mpos[0] - self.x)
			self.sy=(self.mpos[1] - self.y)
			pygame.draw.line(self.paintsurf, self.scribblecolor, (self.dx, self.dy), (self.sx, self.sy), self.penlist[self.penindex])
			self.widsurf.blit(self.paintsurf, (0, 0))
		
		#self.labtx=simplefont.render("window order: " + str(self.wo), True, frametext, framebg)
		#self.widsurf.blit(self.labtx, (0, 0))
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title)
		pygame.draw.rect(self.screensurf, self.scribblecolor, self.color1rect, 0)
		pygame.draw.rect(self.screensurf, framediv, self.color1rect, 1)
		pygame.draw.rect(self.screensurf, frametext, self.sizerect, 0)
		self.labtx=simplefont.render(str(self.penlist[self.penindex]), True, framebg, frametext)
		self.screensurf.blit(self.labtx, (self.x + 32, (self.y + self.widy - 38)))
	def movet(self, xoff, yoff):
		self.x -= xoff
		self.y -= yoff
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		self.closerect=self.frametoup[2]
		self.widbox=self.frametoup[0]
		self.framerect=self.frametoup[1]
		self.paintrect.x = (self.x)
		self.paintrect.y = (self.y)
		self.color1rect=pygame.Rect(self.x, (self.y + self.widy - 38), 30, 30)
		self.sizerect=pygame.Rect(self.x + 32, (self.y + self.widy - 38), 30, 30)
	def click(self, event):
		if self.firstclick==1:
			self.firstclick=2
			
		elif self.sizerect.collidepoint(event.pos) == 1:
			if self.penindex==(len(self.penlist) - 1):
				self.penindex=0
			else:
				self.penindex += 1
		elif self.color1rect.collidepoint(event.pos) == 1:
			if self.colorr==0:
				self.colorr=127
			elif self.colorr==127:
				self.colorr=255
			elif self.colorr==255:
				self.colorr=0
				if self.colorg==0:
					self.colorg=127
				elif self.colorg==127:
					self.colorg=255
				elif self.colorg==255:
					self.colorg=0
					if self.colorb==0:
						self.colorb=127
					elif self.colorb==127:
						self.colorb=255
					elif self.colorb==255:
						self.colorb=0
		elif self.paintrect.collidepoint(event.pos) == 1:
			self.paintsurfbak=self.paintsurf.copy()
			self.sx=(event.pos[0] - self.x)
			self.sy=(event.pos[1] - self.y)
			self.scrib=1
	def clickup(self, event):
		self.scrib=0
	def keydown(self, event):
		
		if event.key==pygame.K_a:
			if self.colorr==0:
				self.colorr=127
			elif self.colorr==127:
				self.colorr=255
			elif self.colorr==255:
				self.colorr=0
		if event.key==pygame.K_s:
			if self.colorg==0:
				self.colorg=127
			elif self.colorg==127:
				self.colorg=255
			elif self.colorg==255:
				self.colorg=0
		if event.key==pygame.K_d:
			if self.colorb==0:
				self.colorb=127
			elif self.colorb==127:
				self.colorb=255
			elif self.colorb==255:
				self.colorb=0
		if event.key==pygame.K_z and self.firstclick==0:
			self.paintsurfq=self.paintsurfbak
			self.paintsurfbak=self.paintsurf
			self.paintsurf=self.paintsurfq
			self.redraw=1
		if event.key==pygame.K_x and self.firstclick==0:
			self.paintsurfbak=self.paintsurf.copy()
			self.scribblecolor=(self.colorr, self.colorg, self.colorb)
			self.paintsurf.fill(self.scribblecolor)
			self.redraw=1
		if event.key==pygame.K_c:
			if self.penindex==(len(self.penlist) - 1):
				self.penindex=0
			else:
				self.penindex += 1
	def keyup(self, event):
		return
	def close(self):
		return
	def hostquit(self):
		return
	def sig(self):
		return


class qcred:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="Credits"
		#taskid is set automatically
		self.taskid=0
		self.pixjmp=14
		self.widx=600
		self.widy=370
		#x and y are required.
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy))
		self.widsurf.fill(libthemeconf.creditbg)
		self.texttable=texttable=["","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
		self.abt = open(os.path.join("VMSYSTEM", "L_CREDIT.TXT"))
		self.scrollsurf=pygame.Surface((600, 410))
		self.scrollmask=pygame.Surface((600, 370))
		self.scrollsurfyaw=-20
		self.scrollmaskyaw=0
		self.scrollsurfwid=0
		self.slide=0
		self.GFXLOGOCRED=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'GFXLOGO-CAT.png')).convert()
		self.sbtccat=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'SBTCCAT34.png')).convert()
		self.slidecnt=0
		self.hbar=pygame.Surface((190, 4))
		self.hbar.fill(libthemeconf.credittext)
	def render(self):
		if self.slide==0:
			self.flid=self.abt.readline()
			self.flid=self.flid.replace('\n', '')
			if self.flid=="-<END>-":
				self.abt.seek(0)
				self.flid=self.abt.readline()
				self.flid=self.flid.replace('\n', '')
			self.texttable.pop(0)
			self.texttable.append(self.flid)
			
			#self.slidecnt=0
			self.pixcnt1=0
			
			self.scrollmaskyaw=0
			self.scrollsurfyaw=-20
			self.scrollsurf.fill(libthemeconf.creditbg)
			#screensurf.fill((255, 255, 255))
			for self.qlid in self.texttable:
				if self.qlid=="-<GFXLOGO>-":
					self.abttextbox=self.GFXLOGOCRED.get_rect()
					self.abttextbox.centerx=self.scrollsurf.get_rect().centerx
					self.abttextbox.y=self.pixcnt1
					self.scrollsurf.blit(self.GFXLOGOCRED, self.abttextbox)
				elif self.qlid=="-<HBAR>-":
					self.abttextbox=self.hbar.get_rect()
					self.abttextbox.centerx=self.scrollsurf.get_rect().centerx
					self.abttextbox.y=self.pixcnt1
					self.scrollsurf.blit(self.hbar, self.abttextbox)
				elif self.qlid=="-<SBTCCAT>-":
					self.abttextbox=self.sbtccat.get_rect()
					self.abttextbox.centerx=self.scrollsurf.get_rect().centerx
					self.abttextbox.y=self.pixcnt1
					self.scrollsurf.blit(self.sbtccat, self.abttextbox)
				elif self.qlid!="":
					self.abttext=simplefont.render(self.qlid, True, libthemeconf.credittext, libthemeconf.creditbg)
					self.abttextbox=self.abttext.get_rect()
					self.abttextbox.centerx=self.scrollsurf.get_rect().centerx
					self.abttextbox.y=self.pixcnt1
					self.scrollsurf.blit(self.abttext, self.abttextbox)
				self.pixcnt1 += self.pixjmp
				self.slide=1
		if self.slide==1:
			if self.slidecnt==14:
				self.slidecnt=0
				self.slide=0
				self.pixcnt1=0
			else:
				
				self.widsurf.blit(self.scrollsurf, (0, self.scrollsurfyaw))
				#self.widsurf.blit(self.scrollmask, (self.scrollsurfwid, self.scrollmaskyaw))
				self.scrollsurfyaw -= 1
				self.slidecnt += 1
			#time.sleep(.05)
			#pygame.display.update()
		#scrollmask.blit(scrollsurf, (0, scrollsurfyaw))
		#widsurf.blit(scrollmask, (scrollsurfwid, scrollmaskyaw))
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title)
	def movet(self, xoff, yoff):
		self.x -= xoff
		self.y -= yoff
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		self.closerect=self.frametoup[2]
		self.widbox=self.frametoup[0]
		self.framerect=self.frametoup[1]
	#click is given pygame MOUSEBUTTONDOWN events that fall within widbox
	def click(self, event):
		return
		
	#similar to click, except it receves MOUSEBUTTONUP events that fall within widbox.
	def clickup(self, event):
		return
	#keydown and keyup are given pygame KEYDOWN and KEYUP events.
	def keydown(self, event):
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
		
		


