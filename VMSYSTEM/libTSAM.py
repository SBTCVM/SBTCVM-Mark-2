#!/usr/bin/env python
import time
import os
import sys
import pygame
from pygame.locals import *
import libSBTCVM
import libbaltcalc
import array
#import libtrom
import libvmconf
synthfreq=int(libvmconf.getconf("audio", "mixrate"))
print synthfreq
pygame.font.init()

#SBTCVM Digital Sample Playback/translation library. 

def PCMcrunch(datastr, freq):
	ret=[]
	for x in datastr:
		if x=="+":
		#dividing the mixer rate (synthfreq), by a static value, creates a consistent speed & pitch across mixer rates.
		#higher divison values=higher pitch make sure each of these has the same value!
		#divison value==Hz of PCM playback.
		#3000.0 and -2000.0 are CORRECT. for some odd reason having the + value
		#be 2000 leaves the left channel silent, but having that and
		#the - value be -3000 causes clipping...  oh well. making note of this.
			ret.extend([3000.0]*(synthfreq//freq))
		if x=="-":
			ret.extend([-2000.0]*(synthfreq//freq))
		if x=="0":
			ret.extend([0.0]*(synthfreq//freq))
	return ret

def sampleconv(offset, length, bank, freq):
	samplebuff=""
	
	dlen=abs(libbaltcalc.BTTODEC(length)+9841)
	for x in xrange(1, dlen):
		samplebuff=samplebuff+(bank[libSBTCVM.numstruct(offset)])[6:]
		offset=libbaltcalc.btadd(offset, "+")
	return PCMcrunch(samplebuff, freq)


class SampleChannnel:
	def __init__(self, channum, bank):
		self.channum=channum
		self.sample=pygame.mixer.Sound(array.array('f', PCMcrunch("000000000", 2000)))
		self.frequency=2000
		self.offset=libbaltcalc.DECTOBT(libbaltcalc.mni(9))
		self.lengthx="00000000+"
		self.regen=0
		self.slidechan=pygame.mixer.Channel(channum)
		#correct for slight left channel bias. have left 0.2 less than right.
		self.slidechan.set_volume(0.5, 0.7)
		self.bank=bank
	def setoffset(self, offset, bank):
		self.regen=1
		self.offset=offset
		self.bank=bank
	def setfreq(self, freq):
		#add freq checks here to add frequencies. also add them to MK2-TWAV.py.
		if freq=="---------":
			self.frequency=2000
		elif freq=="--------0":
			self.frequency=4000
		self.regen=1
	#length set
	def setlen(self, lengthx):
		self.regen=1
		self.lengthx=lengthx
		print(lengthx)
	#play routine
	def play(self):
		self.slidechan.stop()
		#if params have changed, regenerate sample.
		if self.regen==1:
			self.regen=0
			notearray=array.array('f', sampleconv(self.offset, self.lengthx, self.bank, self.frequency))
			self.sample=pygame.mixer.Sound(notearray)
		self.slidechan.play(self.sample)
		print(self.channum)
	def stop(self):
		self.slidechan.stop()
		
