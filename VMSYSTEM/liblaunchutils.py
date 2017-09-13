#!/usr/bin/env python
import VMSYSTEM.libvmui as vmui
import VMSYSTEM.libvmconf as libvmconf
import VMSYSTEM.libthemeconf as libthemeconf
import pygame
import time
import copy
import sys
import os
pygame.font.init()
simplefont = pygame.font.SysFont(None, 19)

framebg=libthemeconf.hudbg
frametext=libthemeconf.hudtext
framebtn=libthemeconf.btnbg2
framediv=libthemeconf.huddiv
#frametext=libthemeconf.hudt

hudy=20
fpad=1

#sig method:
#sig must be a list of arguments or be None
#list of sig return codes:
#(0, widinstance)=activate the pre-initalized wid widinstance
#(1, x)=close self. x=0: call self's close method. 1=don't call close method.
#None=do nothing
#
#
#

#tool lookup function.
def widlookup(namestring):
	if namestring=="TEST":
		return testwid
	if namestring=="scribble":
		return scribble

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
	

class testwid:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="TEST"
		
		self.widx=140
		self.widy=140
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
		self.newinstance=0
		self.selfquit=0
	def render(self):
		self.labtx=simplefont.render("window order: " + str(self.wo), True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 0))
		self.labtx=simplefont.render("space = new instance", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 20))
		self.labtx=simplefont.render("q = close this window", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 40))
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
		print "click"
		
	#similar to click, except it receves MOUSEBUTTONUP events that fall within widbox.
	def clickup(self, event):
		print "clickup"
	#keydown and keyup are given pygame KEYDOWN and KEYUP events.
	def keydown(self, event):
		print "keydown"
		#print event.unicode
		if event.key==pygame.K_SPACE:
			self.newinstance=1
		if event.key==pygame.K_q:
			self.selfquit=1
	def keyup(self, event):
		print "keyup"
	#close is called when the window is to be closed.
	def close(self):
		print "window close"
	#hostquit is called when the host program is going to quit.
	def hostquit(self):
		print "host program quit."
	def sig(self):
		if self.newinstance==1:
			self.newinstance=0
			return (0, testwid(self.screensurf, 0))
		if self.selfquit==1:
			self.selfquit=0
			return (1, 0)
		return

class scribble:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="Scribble"
		
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



		