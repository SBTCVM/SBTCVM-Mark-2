#!/usr/bin/env python
import time
import os
import sys
import pygame
from pygame.locals import *
import libSBTCVM
import libbaltcalc
#import libtrom
#import libvmconf
#mixrate=int(libvmconf.getconf("audio", "mixrate"))
pygame.font.init()

def getcolor0(string):
	redch=string[0]
	greench=string[1]
	bluech=string[2]
	if redch=="-":
		redre=0
	if redch=="0":
		redre=127
	if redch=="+":
		redre=255
	if greench=="-":
		greenre=0
	if greench=="0":
		greenre=127
	if greench=="+":
		greenre=255
	if bluech=="-":
		bluere=0
	if bluech=="0":
		bluere=127
	if bluech=="+":
		bluere=255
	return (redre, greenre, bluere)

#1-trit mono channel conversion. (used with 3-trit RGB)
def shadlook0(string):
	if string=="-":
		return 0
	if string=="0":
		return 127
	if string=="+":
		return 255

dispsurf0=pygame.Surface((114, 81))

#SBTGA v1
class buffdisplay:
	def __init__(self, screensurf, membus, offset, mode="G0"):
		self.screensurf=screensurf
		self.membus=membus
		self.offset=offset
		self.mode=mode
	def render(self, x=0, y=0):
		if self.mode=="G0":
			self.pixy=0
			self.pixx=0
			self.chunkcnt=0
			self.addr=self.offset
			while self.pixy!=81:
				self.pixx=0
				while self.pixx!=114:
					if self.chunkcnt==0:
						self.chunkcnt=1
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[6]) + (self.chunk[7]) + (self.chunk[8]))
					elif self.chunkcnt==1:
						self.chunkcnt=2
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[9]) + (self.chunk[10]) + (self.chunk[11]))
					elif self.chunkcnt==2:
						self.chunkcnt=0
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[12]) + (self.chunk[13]) + (self.chunk[14]))
						self.addr=libSBTCVM.trunkto6(libbaltcalc.btadd(self.addr, "+"))
					self.R1=shadlook0(self.part[0])
					self.G1=shadlook0(self.part[1])
					self.B1=shadlook0(self.part[2])
					#print (self.R1, self.G1, self.B1)
					dispsurf0.set_at((self.pixx, self.pixy),(self.R1, self.G1, self.B1))
					self.pixx += 1
				self.pixy += 1
			return self.screensurf.blit(pygame.transform.scale(dispsurf0, (648, 486)), (x, y))
	def setoffset(self, offset):
		self.offset=offset
	def setmode(self, mode):
		self.mode=mode
		