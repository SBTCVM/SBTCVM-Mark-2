#!/usr/bin/env python
#SBTCVM Mark 2 GFX toolkit
import os

import pygame
import time
from pygame.locals import *
import sys
import VMSYSTEM.libbaltcalc as libbaltcalc

VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")

def gfxargfind(arg):
	lowarg=arg.lower()
	argisfile=0
	qfilewasvalid=0
	for extq in ["", ".png", ".PNG", ".gif", ".GIF"]:
		qarg=(arg + extq)
		qlowarg=(lowarg + extq.lower())
		print("searching for: \"" + qarg + "\"...")
		if os.path.isfile(qarg):
			argisfile=1
			print("found: " + qarg)
		elif os.path.isfile(os.path.join("VMSYSTEM", qarg)):
			qarg=os.path.join("VMSYSTEM", qarg)
			print("found: " + qarg)
			argisfile=1
		elif os.path.isfile(os.path.join(VMSYSROMS, qarg)):
			qarg=os.path.join(VMSYSROMS, qarg)
			print("found: " + qarg)
			argisfile=1
		elif os.path.isfile(os.path.join("VMUSER", qarg)):
			qarg=os.path.join("VMUSER", qarg)
			print("found: " + qarg)
			argisfile=1
		elif os.path.isfile(os.path.join("ROMS", qarg)):
			qarg=os.path.join("ROMS", qarg)
			print("found: " + qarg)
			argisfile=1
		if argisfile==1:
			if os.path.isfile(qarg):
				
				qfilewasvalid=1
				return(qarg)
			
			else:
				print("not valid.")
				argisfile=0
				
	if qfilewasvalid==0:
		print("File not found.")
		sys.exit()
	

def trunkto3(code):
	codecnt=0
	for fel in code:
		codecnt +=1
	if codecnt<3:
		if codecnt==2:
			return("0" + code)
		if codecnt==1:
			return("00" + code)
	#print code
	#code=libbaltcalc.BTINVERT(code)
	return((code[0]) + (code[1]) + (code[2]))



#used to lookup 2-trit channel values to get the binRGb value for that channel
def dollytell(lookupcode):
	if lookupcode=="--":
		return("  0")
	if lookupcode=="-0":
		return(" 32")
	if lookupcode=="-+":
		return(" 64")
	if lookupcode=="0-":
		return(" 96")
	if lookupcode=="00":
		return("127")
	if lookupcode=="0+":
		return("159")
	if lookupcode=="+-":
		return("191")
	if lookupcode=="+0":
		return("223")
	if lookupcode=="++":
		return("255")

def codeshift(colch):
	colch=int(colch)
	#print colch
	if colch<16:
		return("--")
	if colch<32:
		return("-0")
	if colch<48:
		return("-0")
	if colch<64:
		return("-+")
	if colch<80:
		return("-+")
	if colch<96:
		return("0-")
	if colch<111:
		return("0-")
	if colch<127:
		return("00")
	if colch<143:
		return("00")
	if colch<159:
		return("0+")
	if colch<175:
		return("0+")
	if colch<191:
		return("+-")
	if colch<207:
		return("+-")
	if colch<223:
		return("+0")
	if colch<239:
		return("++")
	if colch<=255:
		return("++")
	return"ERROR"




#6-trit intensity dropshift rounder
def dropshift(colch):
	colch=int(colch)
	#print colch
	if colch<16:
		return(0)
	if colch<32:
		return(32)
	if colch<48:
		return(32)
	if colch<64:
		return(64)
	if colch<80:
		return(64)
	if colch<96:
		return(96)
	if colch<111:
		return(96)
	if colch<127:
		return(127)
	if colch<143:
		return(127)
	if colch<159:
		return(159)
	if colch<175:
		return(159)
	if colch<191:
		return(191)
	if colch<207:
		return(191)
	if colch<223:
		return(223)
	if colch<239:
		return(255)
	if colch<=255:
		return(255)
	return"ERROR"


class colgroup:
	def __init__(self, con, num):
		self.con=con
		self.num=num
	


try:
	cmd=sys.argv[1]
except:
	cmd=None
if cmd=="-h" or cmd=="--help" or cmd=="help":
	print('''This is SBTCVM Mark 2's GFX toolkit.
commands:
MK2-GFX.py -h (--help) (help): this text
MK2-GFX.py -v (--version)
MK2-GFX.py -a (--about): about MK2-GFX.py
MK2-GFX.py -c (--colraster) [imagefile]: convert a 27x27 pixel or smaller image to color raster instrucions (exported as a *.tasm)
MK2-GFX.py -cg (--colraster_groupcolor) [imagefile]: same as -c, but groups colors together as a compression scheme.
MK2-GFX.py -cg2 (--colraster_groupcolor2) [imagefile]: same as -cg, but tracks the most common color and uses a single fill instruction to further compress the image.
''')
elif cmd=="-v" or cmd=="--version":
	print("SBTCVM Mark 2 GFX toolkit v2.1.0")
elif cmd==None:
	print("tip: use MK2-GFX.py -h for help.")
elif cmd=="-a" or cmd=="--about":
	print('''#SBTCVM Mark 2 GFX toolkit

v2.1.0

Copyright (c) 2016-2018 Thomas Leathers and Contributors 

  SBTCVM Mark 2 GFX toolkit is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Mark 2 GFX toolkit is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Mark 2 GFX toolkit. If not, see <http://www.gnu.org/licenses/>
''')
elif cmd=="-c" or cmd=="--colraster":
	arg=sys.argv[2]
	arg=gfxargfind(arg)
	pygame.display.init()
	screensurf=pygame.display.set_mode((27, 27))
	
	IMGSOURCE=pygame.image.load(arg)
	
	IMGw=IMGSOURCE.get_width()
	IMGh=IMGSOURCE.get_height()
	
	HPIX=0
	assmflename=arg
	assmnamelst=assmflename.rsplit('.', 1)
	tasmfile=(assmnamelst[0] + (".tasm"))
	tasmout=open(tasmfile, "w")
	tasmout.write("\n#autogenerated by SBTCVM MARK 2 GFX toolkit, from: \"" + arg + "\" \n")
	tasmout.write("textstart\n")
	tasmout.write("autogenerated by SBTCVM MARK 2 GFX \n toolkit, from: \"" + arg + "\" \n")
	tasmout.write("textstop\n")
	while HPIX!=IMGh:
		WPIX=0
		while WPIX!=IMGw:
			COLLIST=IMGSOURCE.get_at((WPIX, HPIX))
			Wtern=trunkto3(libbaltcalc.DECTOBT((WPIX - 13)))
			Htern=trunkto3(libbaltcalc.DECTOBT((HPIX - 13)))
			#print "foo"
			#print COLLIST
			preR=COLLIST[0]
			preG=COLLIST[1]
			preB=COLLIST[2]
			preA=255
			#print((preR, preG, preB, preA))
			postR=dropshift(preR)
			postG=dropshift(preG)
			postB=dropshift(preB)
			terR=codeshift(preR)
			terG=codeshift(preG)
			terB=codeshift(preB)
			postA=dropshift(preA)
			#print((postR, postG, postB, postA))
			IMGSOURCE.set_at((WPIX, HPIX),(postR, postG, postB))
			tasmout.write("setcolorreg|000" + terR + terG + terB + "\n")
			tasmout.write("colorpixel|000" + Wtern + Htern + "\n")
			WPIX += 1
			time.sleep(0.0001)
		print(("line: " + str(HPIX) + " done"))
		
		screensurf.blit(IMGSOURCE, (0, 0))
		pygame.display.update()
		HPIX += 1
	tasmout.write("userwait")
	print(("image: \"" + arg + "\" converted to: \"" + tasmfile + "\" for SBTCVM Mark 2's color raster"))
	#pygame.image.save(IMGSOURCE, ("imgfilter-out.png"))
			
	#print(IMGSOURCE.get_at((639, 479)))
elif cmd=="-cg" or cmd=="--colraster_groupcolor":
	arg=sys.argv[2]
	arg=gfxargfind(arg)
	pygame.display.init()
	screensurf=pygame.display.set_mode((27, 27))
	
	IMGSOURCE=pygame.image.load(arg)
	
	IMGw=IMGSOURCE.get_width()
	IMGh=IMGSOURCE.get_height()
	print("start colortable")
	colortable=dict()
	
	
	HPIX=0
	assmflename=arg
	assmnamelst=assmflename.rsplit('.', 1)
	tasmfile=(assmnamelst[0] + (".tasm"))
	tasmout=open(tasmfile, "w")
	tasmout.write("\n#autogenerated by SBTCVM MARK 2 GFX toolkit, from: \"" + arg + "\" \n")
	tasmout.write("textstart\n")
	tasmout.write("autogenerated by SBTCVM MARK 2 GFX \n toolkit, from: \"" + arg + "\" \n")
	tasmout.write("textstop\n")
	print("begin image scan")
	while HPIX!=IMGh:
		WPIX=0
		while WPIX!=IMGw:
			COLLIST=IMGSOURCE.get_at((WPIX, HPIX))
			Wtern=trunkto3(libbaltcalc.DECTOBT((WPIX - 13)))
			Htern=trunkto3(libbaltcalc.DECTOBT((HPIX - 13)))
			#print "foo"
			#print COLLIST
			preR=COLLIST[0]
			preG=COLLIST[1]
			preB=COLLIST[2]
			preA=255
			#print((preR, preG, preB, preA))
			postR=dropshift(preR)
			postG=dropshift(preG)
			postB=dropshift(preB)
			terR=codeshift(preR)
			terG=codeshift(preG)
			terB=codeshift(preB)
			postA=dropshift(preA)
			#print((postR, postG, postB, postA))
			IMGSOURCE.set_at((WPIX, HPIX),(postR, postG, postB))
			#tasmout.write("setcolorreg|000" + terR + terG + terB + "\n")
			
			pixinstruct=("colorpixel|000" + Wtern + Htern + "\n")
			try:
				colortable[(terR + terG + terB)]=(colortable[(terR + terG + terB)] + pixinstruct)
			except KeyError:
				colortable[(terR + terG + terB)]=(pixinstruct)
				
			WPIX += 1
			time.sleep(0.0001)
		print(("line: " + str(HPIX) + " done"))
		
		screensurf.blit(IMGSOURCE, (0, 0))
		pygame.display.update()
		HPIX += 1
	print("building drawing routines...")
	for fx in colortable:
		tasmout.write("#color change \n")
		tasmout.write("setcolorreg|000" + fx + "\n")
		tasmout.write(colortable[fx])
	tasmout.write("userwait")
	print(("image: \"" + arg + "\" converted to: \"" + tasmfile + "\" for SBTCVM Mark 2's color raster"))
	#pygame.image.save(IMGSOURCE, ("imgfilter-out.png"))
			
	#print(IMGSOURCE.get_at((639, 479)))
elif cmd=="-cg2" or cmd=="--colraster_groupcolor2":
	arg=sys.argv[2]
	arg=gfxargfind(arg)
	pygame.display.init()
	screensurf=pygame.display.set_mode((27, 27))
	
	IMGSOURCE=pygame.image.load(arg)
	
	IMGw=IMGSOURCE.get_width()
	IMGh=IMGSOURCE.get_height()
	print("start colortable")
	colortable=dict()
	
	
	HPIX=0
	assmflename=arg
	assmnamelst=assmflename.rsplit('.', 1)
	tasmfile=(assmnamelst[0] + (".tasm"))
	tasmout=open(tasmfile, "w")
	tasmout.write("\n#autogenerated by SBTCVM MARK 2 GFX toolkit, from: \"" + arg + "\" \n")
	tasmout.write("textstart\n")
	tasmout.write("autogenerated by SBTCVM MARK 2 GFX \n toolkit, from: \"" + arg + "\" \n")
	tasmout.write("textstop\n")
	print("begin image scan")
	while HPIX!=IMGh:
		WPIX=0
		while WPIX!=IMGw:
			COLLIST=IMGSOURCE.get_at((WPIX, HPIX))
			Wtern=trunkto3(libbaltcalc.DECTOBT((WPIX - 13)))
			Htern=trunkto3(libbaltcalc.DECTOBT((HPIX - 13)))
			#print "foo"
			#print COLLIST
			preR=COLLIST[0]
			preG=COLLIST[1]
			preB=COLLIST[2]
			preA=255
			#print((preR, preG, preB, preA))
			postR=dropshift(preR)
			postG=dropshift(preG)
			postB=dropshift(preB)
			terR=codeshift(preR)
			terG=codeshift(preG)
			terB=codeshift(preB)
			postA=dropshift(preA)
			#print((postR, postG, postB, postA))
			IMGSOURCE.set_at((WPIX, HPIX),(postR, postG, postB))
			#tasmout.write("setcolorreg|000" + terR + terG + terB + "\n")
			
			pixinstruct=("colorpixel|000" + Wtern + Htern + "\n")
			try:
				colg=colortable[(terR + terG + terB)]
				colortable[(terR + terG + terB)]=colgroup((colg.con + pixinstruct), (colg.num + 1))
			except KeyError:
				colortable[(terR + terG + terB)]=(colgroup(pixinstruct, 1))
				
			WPIX += 1
			time.sleep(0.0001)
		print(("line: " + str(HPIX) + " done"))
		
		screensurf.blit(IMGSOURCE, (0, 0))
		pygame.display.update()
		HPIX += 1
	maxcol=0
	for fx in colortable:
		xfc=colortable[fx]
		if xfc.num>maxcol:
			maxcol=xfc.num
	for fx in colortable:
		xfc=colortable[fx]
		if xfc.num==maxcol:
			tasmout.write("colorfill|000" + fx + "\n")
			del colortable[fx]
			break
	print("building drawing routines...")
	for fx in colortable:
		tasmout.write("#color change \n")
		tasmout.write("setcolorreg|000" + fx + "\n")
		tasmout.write((colortable[fx]).con)
	tasmout.write("userwait")
	print(("image: \"" + arg + "\" converted to: \"" + tasmfile + "\" for SBTCVM Mark 2's color raster"))
	#pygame.image.save(IMGSOURCE, ("imgfilter-out.png"))
			
	#print(IMGSOURCE.get_at((639, 479)))
else:
	print("see MK2-GFX.py -h for help.")
	print(cmd)