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
simplefont = pygame.font.SysFont(None, 16)

framebg=libthemeconf.hudbg
frametext=libthemeconf.hudtext
framebtn=libthemeconf.btnbg2
framediv=libthemeconf.huddiv
#frametext=libthemeconf.hudt

hudy=20
fpad=1


#tool lookup function.
def widlookup(namestring):
	if namestring=="TEST":
		return testwid
	if namestring=="scribble":
		return scribble

#standardized rect generation
def getframes(x, y, widsurf):
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
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy))
		self.widsurf.fill((255, 255, 255))
		
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
	def render(self):
		self.labtx=simplefont.render("window order: " + str(self.wo), True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 0))
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
	def keyup(self, event):
		print "keyup"
	#close is called when the window is to be closed.
	def close(self):
		print "window close"
	#hostquit is called when the host program is going to quit.
	def hostquit(self):
		print "host program quit."
		

class scribble:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="scribble"
		
		self.widx=324
		self.widy=283
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy)).convert(self.screensurf)
		self.widsurf.fill((200, 200, 200))
		self.paintsurf=pygame.Surface((self.widx, self.widy-40)).convert(self.widsurf)
		self.paintsurf.fill((255, 255, 255))
		self.paintrect=self.paintsurf.get_rect()
		self.paintrect.x = (self.x)
		self.paintrect.y = (self.y + 20)
		self.scribblecolor=(0, 0, 0)
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		self.scrib=0
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
	def render(self):
		if self.scrib==1:
			self.dx=self.sx
			self.dy=self.sy
			self.mpos=pygame.mouse.get_pos()
			self.sx=(self.mpos[0] - self.x)
			self.sy=(self.mpos[1] - self.y - hudy)
			pygame.draw.line(self.paintsurf, self.scribblecolor, (self.dx, self.dy), (self.sx, self.sy))
			self.widsurf.blit(self.paintsurf, (0, 0))
		#self.labtx=simplefont.render("window order: " + str(self.wo), True, frametext, framebg)
		#self.widsurf.blit(self.labtx, (0, 0))
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title)
	def movet(self, xoff, yoff):
		self.x -= xoff
		self.y -= yoff
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		self.closerect=self.frametoup[2]
		self.widbox=self.frametoup[0]
		self.framerect=self.frametoup[1]
		self.paintrect.x = (self.x)
		self.paintrect.y = (self.y)
	#click is given pygame MOUSEBUTTONDOWN events that fall within widbox
	def click(self, event):
		if self.paintrect.collidepoint(event.pos) == 1:
			self.sx=(event.pos[0] - self.x)
			self.sy=(event.pos[1] - self.y - hudy)
			self.scrib=1
	#similar to click, except it receves MOUSEBUTTONUP events that fall within widbox.
	def clickup(self, event):
		self.scrib=0
	#keydown and keyup are given pygame KEYDOWN and KEYUP events.
	def keydown(self, event):
		return
		#print event.unicode
	def keyup(self, event):
		return
	#close is called when the window is to be closed.
	def close(self):
		return
	#hostquit is called when the host program is going to quit.
	def hostquit(self):
		return
		



		