#!/usr/bin/env python
#SBTCVM Mark 2 Graphics Adapter Toolkit
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
		print "searching for: \"" + qarg + "\"..."
		if os.path.isfile(qarg):
			argisfile=1
			print "found: " + qarg
		elif os.path.isfile(os.path.join("VMSYSTEM", qarg)):
			qarg=os.path.join("VMSYSTEM", qarg)
			print "found: " + qarg
			argisfile=1
		elif os.path.isfile(os.path.join(VMSYSROMS, qarg)):
			qarg=os.path.join(VMSYSROMS, qarg)
			print "found: " + qarg
			argisfile=1
		elif os.path.isfile(os.path.join("VMUSER", qarg)):
			qarg=os.path.join("VMUSER", qarg)
			print "found: " + qarg
			argisfile=1
		elif os.path.isfile(os.path.join("ROMS", qarg)):
			qarg=os.path.join("ROMS", qarg)
			print "found: " + qarg
			argisfile=1
		if argisfile==1:
			if os.path.isfile(qarg):
				
				qfilewasvalid=1
				return(qarg)
			
			else:
				print "not valid."
				argisfile=0
				
	if qfilewasvalid==0:
		print "File not found."
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



def dollytell(lookupcode):
	if lookupcode=="-":
		return("0")
	if lookupcode=="0":
		return("127")
	if lookupcode=="+":
		return("255")

def codeshift(colch):
	colch=int(colch)
	if colch<63:
		return "-"
	if colch<190:
		return "0"
	else:
		return "+"
		
def dropshift(colch):
	colch=int(colch)
	if colch<63:
		return 0
	if colch<190:
		return 127
	else:
		return 255



class colgroup:
	def __init__(self, con, num):
		self.con=con
		self.num=num
	


try:
	cmd=sys.argv[1]
except:
	cmd=None
if cmd=="-h" or cmd=="--help" or cmd=="help":
	print '''This is SBTCVM Mark 2's GAT toolkit.
commands:
MK2-GAT.py -h (--help) (help): this text
MK2-GAT.py -v (--version)
MK2-GAT.py -a (--about): about MK2-GAT.py
MK2-GAT.py -g0 (--modegfx0) [imagefile]: convert an (exactly) 114x81 pixel
 image to a full framebuffer area (exported as a *.tasm) for the G0, 114x81,
 3-trit RGB screen mode.
MK2-GAT.py -g2 (--modegfx2) [imagefile]: full framebuffer: G2 (114x81 1-trit monochrome)
MK2-GAT.py -g3 (--modegfx3) [imagefile]: full framebuffer: G3 (54x38 3-trit RGB)
MK2-GAT.py -g4 (--modegfx4) [imagefile]: full framebuffer: G4 (54x38 1-trit monochrome)'''
elif cmd=="-v" or cmd=="--version":
	print "SBTCVM Mark 2 GAT toolkit v1.0.0"
elif cmd==None:
	print "tip: use MK2-GAT.py -h for help."
elif cmd=="-a" or cmd=="--about":
	print '''#SBTCVM Mark 2 GAT toolkit

v1.0.0

Copyright (c) 2016-2018 Thomas Leathers and Contributors 

  SBTCVM Mark 2 GAT toolkit is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Mark 2 GAT toolkit is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Mark 2 GAT toolkit. If not, see <http://www.gnu.org/licenses/>
'''
elif cmd=="-g0" or cmd=="--modegfx0":
	arg=sys.argv[2]
	arg=gfxargfind(arg)
	pygame.display.init()
	screensurf=pygame.display.set_mode((114, 81))
	
	IMGSOURCE=pygame.image.load(arg)
	
	IMGw=IMGSOURCE.get_width()
	IMGh=IMGSOURCE.get_height()
	if IMGw!=114 or IMGh!=81:
		sys.exit("ERROR: Image not proper size! image MUST match mode G0 screen size! (114x81)")
		
	
	HPIX=0
	assmflename=arg
	assmnamelst=assmflename.rsplit('.', 1)
	tasmfile=(assmnamelst[0] + (".tasm"))
	tasmout=open(tasmfile, "w")
	tasmout.write("\n#autogenerated by SBTCVM MARK 2 GAT toolkit, from: \"" + arg + "\" \n")
	tasmout.write("""setreg1|---------
IOwrite1|>dispmode
setreg1|>dispoff
IOwrite1|>dispoffset
setreg1|000000000
IOwrite1|>dispupdate
userwait
""")
	chunkcnt=0
	first=1
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
			#tasmout.write("colorpixel|000" + Wtern + Htern + "\n")
			if chunkcnt==0:
				chunkcnt+=1
				tasmout.write("null|" + terR + terG + terB)
			elif chunkcnt==1:
				chunkcnt+=1
				tasmout.write(terR + terG + terB)
			else:
				chunkcnt=0
				if first==1:
					first=0
					tasmout.write(terR + terG + terB + "|dispoff\n")
				else:
					tasmout.write(terR + terG + terB + "\n")
			WPIX += 1
			time.sleep(0.0001)
		print ("line: " + str(HPIX) + " done")
		
		screensurf.blit(IMGSOURCE, (0, 0))
		pygame.display.update()
		HPIX += 1
	#tasmout.write("userwait")
	print ("image: \"" + arg + "\" converted to: \"" + tasmfile + "\" for SBTCVM SBTGA mode G0 (full)")
	#pygame.image.save(IMGSOURCE, ("imgfilter-out.png"))
			
	#print(IMGSOURCE.get_at((639, 479)))
elif cmd=="-g2" or cmd=="--modegfx2":
	arg=sys.argv[2]
	arg=gfxargfind(arg)
	pygame.display.init()
	screensurf=pygame.display.set_mode((114, 81))
	
	IMGSOURCE=pygame.image.load(arg)
	
	IMGw=IMGSOURCE.get_width()
	IMGh=IMGSOURCE.get_height()
	if IMGw!=114 or IMGh!=81:
		sys.exit("ERROR: Image not proper size! image MUST match mode G2 screen size! (114x81)")
		
	
	HPIX=0
	assmflename=arg
	assmnamelst=assmflename.rsplit('.', 1)
	tasmfile=(assmnamelst[0] + (".tasm"))
	tasmout=open(tasmfile, "w")
	tasmout.write("\n#autogenerated by SBTCVM MARK 2 GAT toolkit, from: \"" + arg + "\" \n")
	tasmout.write("""setreg1|--------+
IOwrite1|>dispmode
setreg1|>dispoff
IOwrite1|>dispoffset
setreg1|000000000
IOwrite1|>dispupdate
userwait
""")
	chunkcnt=0
	first=1
	while HPIX!=IMGh:
		WPIX=0
		while WPIX!=IMGw:
			COLLIST=IMGSOURCE.get_at((WPIX, HPIX))
			Wtern=trunkto3(libbaltcalc.DECTOBT((WPIX - 13)))
			Htern=trunkto3(libbaltcalc.DECTOBT((HPIX - 13)))
			#print "foo"
			#print COLLIST
			pre=COLLIST[1]
			#print((preR, preG, preB, preA))
			post=dropshift(pre)
			ter=codeshift(pre)
			#print((postR, postG, postB, postA))
			IMGSOURCE.set_at((WPIX, HPIX),(post, post, post))
			#tasmout.write("setcolorreg|000" + terR + terG + terB + "\n")
			#tasmout.write("colorpixel|000" + Wtern + Htern + "\n")
			if chunkcnt==0:
				chunkcnt+=1
				tasmout.write("null|" + ter)
			elif chunkcnt<8:
				chunkcnt+=1
				tasmout.write(ter)
			else:
				chunkcnt=0
				if first==1:
					first=0
					tasmout.write(ter + "|dispoff\n")
				else:
					tasmout.write(ter + "\n")
			WPIX += 1
			time.sleep(0.0001)
		print ("line: " + str(HPIX) + " done")
		
		screensurf.blit(IMGSOURCE, (0, 0))
		pygame.display.update()
		HPIX += 1
	#tasmout.write("userwait")
	print ("image: \"" + arg + "\" converted to: \"" + tasmfile + "\" for SBTCVM SBTGA mode G2 (full)")
	#pygame.image.save(IMGSOURCE, ("imgfilter-out.png"))
			
	#print(IMGSOURCE.get_at((639, 479)))
###
elif cmd=="-g3" or cmd=="--modegfx3":
	arg=sys.argv[2]
	arg=gfxargfind(arg)
	pygame.display.init()
	screensurf=pygame.display.set_mode((114, 81))
	
	IMGSOURCE=pygame.image.load(arg)
	
	IMGw=IMGSOURCE.get_width()
	IMGh=IMGSOURCE.get_height()
	if IMGw!=54 or IMGh!=38:
		sys.exit("ERROR: Image not proper size! image MUST match mode G3 screen size! (54x38)")
		
	
	HPIX=0
	assmflename=arg
	assmnamelst=assmflename.rsplit('.', 1)
	tasmfile=(assmnamelst[0] + (".tasm"))
	tasmout=open(tasmfile, "w")
	tasmout.write("\n#autogenerated by SBTCVM MARK 2 GAT toolkit, from: \"" + arg + "\" \n")
	tasmout.write("""setreg1|-------0-
IOwrite1|>dispmode
setreg1|>dispoff
IOwrite1|>dispoffset
setreg1|000000000
IOwrite1|>dispupdate
userwait
""")
	chunkcnt=0
	first=1
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
			#tasmout.write("colorpixel|000" + Wtern + Htern + "\n")
			if chunkcnt==0:
				chunkcnt+=1
				tasmout.write("null|" + terR + terG + terB)
			elif chunkcnt==1:
				chunkcnt+=1
				tasmout.write(terR + terG + terB)
			else:
				chunkcnt=0
				if first==1:
					first=0
					tasmout.write(terR + terG + terB + "|dispoff\n")
				else:
					tasmout.write(terR + terG + terB + "\n")
			WPIX += 1
			time.sleep(0.0001)
		print ("line: " + str(HPIX) + " done")
		
		screensurf.blit(IMGSOURCE, (0, 0))
		pygame.display.update()
		HPIX += 1
	#tasmout.write("userwait")
	print ("image: \"" + arg + "\" converted to: \"" + tasmfile + "\" for SBTCVM SBTGA mode G3 (full)")
	#pygame.image.save(IMGSOURCE, ("imgfilter-out.png"))
			
	#print(IMGSOURCE.get_at((639, 479)))
elif cmd=="-g4" or cmd=="--modegfx4":
	arg=sys.argv[2]
	arg=gfxargfind(arg)
	pygame.display.init()
	screensurf=pygame.display.set_mode((114, 81))
	
	IMGSOURCE=pygame.image.load(arg)
	
	IMGw=IMGSOURCE.get_width()
	IMGh=IMGSOURCE.get_height()
	if IMGw!=54 or IMGh!=38:
		sys.exit("ERROR: Image not proper size! image MUST match mode G4 screen size! (54x38)")
		
	
	HPIX=0
	assmflename=arg
	assmnamelst=assmflename.rsplit('.', 1)
	tasmfile=(assmnamelst[0] + (".tasm"))
	tasmout=open(tasmfile, "w")
	tasmout.write("\n#autogenerated by SBTCVM MARK 2 GAT toolkit, from: \"" + arg + "\" \n")
	tasmout.write("""setreg1|-------00
IOwrite1|>dispmode
setreg1|>dispoff
IOwrite1|>dispoffset
setreg1|000000000
IOwrite1|>dispupdate
userwait
""")
	chunkcnt=0
	first=1
	while HPIX!=IMGh:
		WPIX=0
		while WPIX!=IMGw:
			COLLIST=IMGSOURCE.get_at((WPIX, HPIX))
			Wtern=trunkto3(libbaltcalc.DECTOBT((WPIX - 13)))
			Htern=trunkto3(libbaltcalc.DECTOBT((HPIX - 13)))
			#print "foo"
			#print COLLIST
			pre=COLLIST[1]
			#print((preR, preG, preB, preA))
			post=dropshift(pre)
			ter=codeshift(pre)
			#print((postR, postG, postB, postA))
			IMGSOURCE.set_at((WPIX, HPIX),(post, post, post))
			#tasmout.write("setcolorreg|000" + terR + terG + terB + "\n")
			#tasmout.write("colorpixel|000" + Wtern + Htern + "\n")
			if chunkcnt==0:
				chunkcnt+=1
				tasmout.write("null|" + ter)
			elif chunkcnt<8:
				chunkcnt+=1
				tasmout.write(ter)
			else:
				chunkcnt=0
				if first==1:
					first=0
					tasmout.write(ter + "|dispoff\n")
				else:
					tasmout.write(ter + "\n")
			WPIX += 1
			time.sleep(0.0001)
		print ("line: " + str(HPIX) + " done")
		
		screensurf.blit(IMGSOURCE, (0, 0))
		pygame.display.update()
		HPIX += 1
	#tasmout.write("userwait")
	print ("image: \"" + arg + "\" converted to: \"" + tasmfile + "\" for SBTCVM SBTGA mode G4 (full)")
	#pygame.image.save(IMGSOURCE, ("imgfilter-out.png"))
			
	#print(IMGSOURCE.get_at((639, 479)))
else:
	print "see MK2-GAT.py -h for help."
	print cmd