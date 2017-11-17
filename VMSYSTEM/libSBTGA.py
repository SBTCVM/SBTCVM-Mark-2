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
dispsurf1=pygame.Surface((54, 38))

cubedisprect0=pygame.Rect(0, 0, 570, 405)
cubedisprect1=pygame.Rect(0, 0, 648, 456)
cubeblock0=pygame.Rect(0, 0, 5, 5)
cubeblock1=pygame.Rect(0, 0, 12, 12)
cubeblocksurf0=pygame.Surface((5, 5))
cubeblocksurf1=pygame.Surface((12, 12))
#SBTGA v1
class buffdisplay:
	def __init__(self, screensurf, membus, offset, mode="G0"):
		self.screensurf=screensurf
		self.membus=membus
		self.offset=offset
		self.mode=mode
		
	def render(self, x=0, y=0):
		if self.mode=="G0":
			dispsurf0.lock()
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
			dispsurf0.unlock()
			return self.screensurf.blit(pygame.transform.scale(dispsurf0, (648, 460)), (x, y))
		if self.mode=="G2":
			dispsurf0.lock()
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
						self.part=((self.chunk[6]))
					elif self.chunkcnt==1:
						self.chunkcnt=2
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[7]))
					elif self.chunkcnt==2:
						self.chunkcnt=3
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[8]))
					elif self.chunkcnt==3:
						self.chunkcnt=4
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[9]))
					elif self.chunkcnt==4:
						self.chunkcnt=5
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[10]))
					elif self.chunkcnt==5:
						self.chunkcnt=6
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[11]))
					elif self.chunkcnt==6:
						self.chunkcnt=7
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[12]))
					elif self.chunkcnt==7:
						self.chunkcnt=8
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[13]))
					elif self.chunkcnt==8:
						self.chunkcnt=0
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[14]))
						self.addr=libSBTCVM.trunkto6(libbaltcalc.btadd(self.addr, "+"))
					self.GREY=shadlook0(self.part)
					dispsurf0.set_at((self.pixx, self.pixy),(self.GREY, self.GREY, self.GREY))
					#print self.chunkcnt
					#print self.pixx
					#print self.pixy
					self.pixx += 1
				self.pixy += 1
			dispsurf0.unlock()
			return self.screensurf.blit(pygame.transform.scale(dispsurf0, (648, 460)), (x, y))
		if self.mode=="G3":
			dispsurf1.lock()
			self.pixy=0
			self.pixx=0
			self.chunkcnt=0
			self.addr=self.offset
			while self.pixy!=38:
				self.pixx=0
				while self.pixx!=54:
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
					dispsurf1.set_at((self.pixx, self.pixy),(self.R1, self.G1, self.B1))
					self.pixx += 1
				self.pixy += 1
			dispsurf1.unlock()
			return self.screensurf.blit(pygame.transform.scale(dispsurf1, (648, 460)), (x, y))
		if self.mode=="G4":
			dispsurf1.lock()
			self.pixy=0
			self.pixx=0
			self.chunkcnt=0
			self.addr=self.offset
			while self.pixy!=38:
				self.pixx=0
				while self.pixx!=54:
					if self.chunkcnt==0:
						self.chunkcnt=1
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[6]))
					elif self.chunkcnt==1:
						self.chunkcnt=2
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[7]))
					elif self.chunkcnt==2:
						self.chunkcnt=3
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[8]))
					elif self.chunkcnt==3:
						self.chunkcnt=4
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[9]))
					elif self.chunkcnt==4:
						self.chunkcnt=5
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[10]))
					elif self.chunkcnt==5:
						self.chunkcnt=6
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[11]))
					elif self.chunkcnt==6:
						self.chunkcnt=7
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[12]))
					elif self.chunkcnt==7:
						self.chunkcnt=8
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[13]))
					elif self.chunkcnt==8:
						self.chunkcnt=0
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[14]))
						self.addr=libSBTCVM.trunkto6(libbaltcalc.btadd(self.addr, "+"))
					self.GREY=shadlook0(self.part)
					dispsurf1.set_at((self.pixx, self.pixy),(self.GREY, self.GREY, self.GREY))
					#print self.chunkcnt
					#print self.pixx
					#print self.pixy
					self.pixx += 1
				self.pixy += 1
			dispsurf1.unlock()
			return self.screensurf.blit(pygame.transform.scale(dispsurf1, (648, 460)), (x, y))
			return self.screensurf.blit(dispsurf1, (x, y))
	def setoffset(self, offset):
		self.offset=offset
	def setmode(self, mode):
		self.mode=mode

#Cube matrix approx method
class buffdisplaycubematrix:
	def __init__(self, screensurf, membus, offset, mode="G0"):
		self.screensurf=screensurf
		self.membus=membus
		self.offset=offset
		self.mode=mode
		self.cubeblocksurf1=cubeblocksurf1.convert(self.screensurf)
		self.cubeblocksurf0=cubeblocksurf0.convert(self.screensurf)
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
					#dispsurf0.set_at((self.pixx, self.pixy),(self.R1, self.G1, self.B1))
					self.cubeblocksurf0.fill((self.R1, self.G1, self.B1))
					self.screensurf.blit(self.cubeblocksurf0, (((self.pixx * 5) + x), ((self.pixy * 5) + y)))
					self.pixx += 1
				self.pixy += 1
			cubedisprect0.x=x
			cubedisprect0.y=y
			return cubedisprect0
			#return self.screensurf.blit(pygame.transform.scale(dispsurf0, (648, 460)), (x, y))
		if self.mode=="G2":
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
						self.part=((self.chunk[6]))
					elif self.chunkcnt==1:
						self.chunkcnt=2
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[7]))
					elif self.chunkcnt==2:
						self.chunkcnt=3
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[8]))
					elif self.chunkcnt==3:
						self.chunkcnt=4
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[9]))
					elif self.chunkcnt==4:
						self.chunkcnt=5
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[10]))
					elif self.chunkcnt==5:
						self.chunkcnt=6
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[11]))
					elif self.chunkcnt==6:
						self.chunkcnt=7
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[12]))
					elif self.chunkcnt==7:
						self.chunkcnt=8
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[13]))
					elif self.chunkcnt==8:
						self.chunkcnt=0
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[14]))
						self.addr=libSBTCVM.trunkto6(libbaltcalc.btadd(self.addr, "+"))
					self.GREY=shadlook0(self.part)
					#dispsurf0.set_at((self.pixx, self.pixy),(self.GREY, self.GREY, self.GREY))
					self.cubeblocksurf0.fill((self.GREY, self.GREY, self.GREY))
					self.screensurf.blit(self.cubeblocksurf0, (((self.pixx * 5) + x), ((self.pixy * 5) + y)))
					#print self.chunkcnt
					#print self.pixx
					#print self.pixy
					self.pixx += 1
				self.pixy += 1
			#return self.screensurf.blit(pygame.transform.scale(dispsurf0, (648, 460)), (x, y))
			cubedisprect0.x=x
			cubedisprect0.y=y
			return cubedisprect0
		if self.mode=="G3":
			self.pixy=0
			self.pixx=0
			self.chunkcnt=0
			self.addr=self.offset
			while self.pixy!=38:
				self.pixx=0
				while self.pixx!=54:
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
					#dispsurf1.set_at((self.pixx, self.pixy),(self.R1, self.G1, self.B1))
					self.cubeblocksurf1.fill((self.R1, self.G1, self.B1))
					self.screensurf.blit(self.cubeblocksurf1, (((self.pixx * 12) + x), ((self.pixy * 12) + y)))
					self.pixx += 1
				self.pixy += 1
			cubedisprect1.x=x
			cubedisprect1.y=y
			return cubedisprect1
			#return self.screensurf.blit(pygame.transform.scale(dispsurf1, (648, 460)), (x, y))
		if self.mode=="G4":
			self.pixy=0
			self.pixx=0
			self.chunkcnt=0
			self.addr=self.offset
			while self.pixy!=38:
				self.pixx=0
				while self.pixx!=54:
					if self.chunkcnt==0:
						self.chunkcnt=1
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[6]))
					elif self.chunkcnt==1:
						self.chunkcnt=2
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[7]))
					elif self.chunkcnt==2:
						self.chunkcnt=3
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[8]))
					elif self.chunkcnt==3:
						self.chunkcnt=4
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[9]))
					elif self.chunkcnt==4:
						self.chunkcnt=5
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[10]))
					elif self.chunkcnt==5:
						self.chunkcnt=6
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[11]))
					elif self.chunkcnt==6:
						self.chunkcnt=7
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[12]))
					elif self.chunkcnt==7:
						self.chunkcnt=8
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[13]))
					elif self.chunkcnt==8:
						self.chunkcnt=0
						self.chunk=self.membus[libSBTCVM.numstruct(self.addr)]
						self.part=((self.chunk[14]))
						self.addr=libSBTCVM.trunkto6(libbaltcalc.btadd(self.addr, "+"))
					self.GREY=shadlook0(self.part)
					#dispsurf1.set_at((self.pixx, self.pixy),(self.GREY, self.GREY, self.GREY))
					#cubeblock1.x=((self.pixx * 12) + x)
					#cubeblock1.y=((self.pixy * 12) + y)
					#pygame.draw.rect(self.screensurf, (self.GREY, self.GREY, self.GREY), cubeblock1)
					self.cubeblocksurf1.fill((self.GREY, self.GREY, self.GREY))
					self.screensurf.blit(self.cubeblocksurf1, (((self.pixx * 12) + x), ((self.pixy * 12) + y)))
					#print self.chunkcnt
					#print self.pixx
					#print self.pixy
					self.pixx += 1
				self.pixy += 1
			cubedisprect1.x=x
			cubedisprect1.y=y
			return cubedisprect1
			#return self.screensurf.blit(pygame.transform.scale(dispsurf1, (648, 460)), (x, y))
	def setoffset(self, offset):
		self.offset=offset
	def setmode(self, mode):
		self.mode=mode

		