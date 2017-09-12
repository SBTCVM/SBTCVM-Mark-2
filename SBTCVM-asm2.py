#!/usr/bin/env python
import VMSYSTEM.libSBTCVM as libSBTCVM
import VMSYSTEM.libbaltcalc as libbaltcalc
import sys
import os


assmoverrun=19683
instcnt=0
txtblk=0
VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")
critcomperr=0

compvers="v2.3.0"

outfile="assmout.trom"
#define IOmaps
IOmapread={"random": "--0------"}
IOmapwrite={}
#populate IOmaps with memory pointers
scratchmap={}
scratchstart="---------"
shortsccnt=1
scratchstop="---++++++"
IOgen=scratchstart
while IOgen!=scratchstop:
	#scratchmap[("mem" + str(shortsccnt))] = IOgen
	IOmapread[("mem" + str(shortsccnt))] = IOgen
	IOmapwrite[("mem" + str(shortsccnt))] = IOgen
	IOgen=libSBTCVM.trunkto6(libbaltcalc.btadd(IOgen, "+"))
	shortsccnt += 1
#scratchmap[("mem" + str(shortsccnt))] = scratchstop
IOmapread[("mem" + str(shortsccnt))] = scratchstop
IOmapwrite[("mem" + str(shortsccnt))] = scratchstop

def getlinetern(line):
	line=(line-9841)
	tline=libSBTCVM.trunkto6(libbaltcalc.DECTOBT(line))
	return tline

tracecomp=0
#used to write to the compiler log if the compiler is in tracelog mode
def complog(textis):
	if tracecomp==1:
		compilerlog.write(textis)
#class used by the goto refrence system
class gotoref:
	def __init__(self, line, gtname):
		self.line=line
		self.tline=getlinetern(line)
		self.gtname=gtname
#begin by reading command line arguments
try:
	cmd=sys.argv[1]
except:
	cmd=None

if "GLOBASMFLG" in globals():
	cmd=GLOBASMFLG
if cmd=="-h" or cmd=="--help" or cmd=="help":
	print '''This is SBTCVM-asm2.py, SBTCVM Mark 2's assembler.
commands:
SBTCVM-asm2.py -h (--help) (help): this text
SBTCVM-asm2.py -v (--version)
SBTCVM-asm2.py -a (--about): about SBTCVM-asm2.py
SBTCVM-asm2.py -c (--compile) [sourcefile]: build a tasm source into a trom
SBTCVM-asm2.py -t (--tracecompile) [sourcefile]: same as -c but logs the compiling process in detail in the CAP directory.
SBTCVM-asm2.py [sourcefile]: build a tasm source into a trom
'''
elif cmd=="-v" or cmd=="--version":
	print ("SBTCVM Assember" + compvers)
elif cmd=="-a" or cmd=="--about":
	print '''SBTCVM Assembler 2


''' + compvers + '''

Copyright (c) 2016-2017 Thomas Leathers and Contributors

  SBTCVM Assembler 2 is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Assembler 2 is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Assembler 2. If not, see <http://www.gnu.org/licenses/>
'''
elif cmd==None:
	print "tip: use SBTCVM-asm2.py -h for help."
elif cmd=="-c" or cmd=="--compile" or cmd[0]!="-" or cmd=="-t" or cmd=="--tracecompile":
	print("SBTCVM-asm " + compvers + " starting")
	if "GLOBASMFLG" in globals():
		arg=GLOBASMFLG
	else:
		if cmd[0]!="-":
			arg=sys.argv[1]
		else:
			arg=sys.argv[2]
	print arg
	lowarg=arg.lower()
	argisfile=0
	argistasm=0
	#file search operation
	for extq in ["", ".tasm", ".TASM"]:
		qarg=(arg + extq)
		qlowarg=(lowarg + extq.lower())
		print "searching for: \"" + qarg + "\"..."
		argisfile
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
			if qlowarg.endswith(".tasm") and os.path.isfile(qarg):
				print "tasm source found."
				arg=qarg
				argistasm=1
				break
			
			else:
				print "Not valid."
				argisfile=0
	if argisfile==0 or argistasm==0:
		#print "ERROR: file not found, or is not a tasm file STOP"
		sys.exit("ERROR: SBTCVM assembler was unable to load the specified filename. STOP")
	#generate a name for logs in case its needed
	#logsub=arg.replace("/", "-")
	#logsub=logsub.replace("~", "")
	#logsub=logsub.split(".")
	logsub=libSBTCVM.namecrunch(arg, "-tasm-comp.log")
	#detect if command line options specify tracelog compile mode:
	if cmd=="-t" or cmd=="--tracecompile":
		tracecomp=1
		compilerlog=open(os.path.join('CAP', logsub), "w")
	else:
		tracecomp=0
	#arg=arg.replace("./", "")
	#print arg
	complog("starting up compiler...\n")
	complog("TASM VERSION: SBTCVM-asm " + compvers + "\n")
	complog("source: " + arg + "\n")
	complog("---------\n\n")
	#open 2 instances of source. one per pass.
	sourcefile=open(arg, 'r')
	sourcefileB=open(arg, 'r')
	#open(arg, 'r') as sourcefile
	gotoreflist=list()
	#first pass (detects goto refrence labels and preps them to be used by second pass)
	print "preforming prescan & prep pass"
	complog("preforming prescan & prep pass\n")
	srcline=0
	for linen in sourcefile:
		srcline += 1
		lined=linen
		#removes newlines from line
		linen=linen.replace("\n", "")
		#removes tabs from line
		linen=linen.replace("	", "")
		#stores an unsplit line for text blocks.
		linenraw=linen
		#causes comments to be ignored
		linen=(linen.split("#"))[0]
		#makes semicolon a stand-in for vertical bars. (offered as an easier to type option)
		linen=linen.replace(";", "|")
		linelist=linen.split("|")
		#set this to one by default, set it otherwise on multi-instruction macros.
		instlenflg=1
		
		if (len(linelist))==2:
			instword=(linelist[0])
			instdat=(linelist[1])
		else:
			instword=(linelist[0])
			instdat="000000000"
		if instword=="textstop":
			txtblk=0
			complog("TEXTBLOCK END\n")
		gtflag=1
		if txtblk==1:
			for f in lined:
				instcnt += 1
		elif instword=="textstart":
			txtblk=1
			complog("TEXTBLOCK START\n")
		#raw class
		elif instword=="romread1":
			instcnt += 1
		elif instword=="romread2":
			instcnt += 1
		elif instword=="IOread1":
			instcnt += 1
		elif instword=="IOread2":
			instcnt += 1
		elif instword=="IOwrite1":
			instcnt += 1
		elif instword=="IOwrite2":
			instcnt += 1
		elif instword=="regswap":
			instcnt += 1
		elif instword=="copy1to2":
			instcnt += 1
		elif instword=="copy2to1":
			instcnt += 1
		elif instword=="invert1":
			instcnt += 1
		elif instword=="invert2":
			instcnt += 1
		elif instword=="add":
			instcnt += 1
		elif instword=="subtract":
			instcnt += 1
		elif instword=="multiply":
			instcnt += 1
		elif instword=="divide":
			instcnt += 1
		elif instword=="setreg1":
			instcnt += 1
		elif instword=="setreg2":
			instcnt += 1
		elif instword=="setinst":
			instcnt += 1
		elif instword=="setdata":
			instcnt += 1
		#----jump in used opcodes----
		#color drawing
		elif instword=="continue":
			instcnt += 1
		elif instword=="colorpixel":
			instcnt += 1
		elif instword=="setcolorreg":
			instcnt += 1
		elif instword=="colorfill":
			instcnt += 1
		elif instword=="setcolorvect":
			instcnt += 1
		elif instword=="colorline":
			instcnt += 1
		elif instword=="colorrect":
			instcnt += 1
		#mono drawing
		elif instword=="monopixel":
			instcnt += 1
		elif instword=="monofill":
			instcnt += 1
		elif instword=="setmonovect":
			instcnt += 1
		elif instword=="monoline":
			instcnt += 1
		elif instword=="monorect":
			instcnt += 1
		#----opcode --00-+ unused----
		elif instword=="stop":
			instcnt += 1
		elif instword=="null":
			instcnt += 1
		elif instword=="gotodata":
			instcnt += 1
		elif instword=="gotoreg1":
			instcnt += 1
		elif instword=="gotodataif":
			instcnt += 1
		elif instword=="wait":
			instcnt += 1
		elif instword=="YNgoto":
			instcnt += 1
		elif instword=="userwait":
			instcnt += 1
		elif instword=="TTYclear":
			instcnt += 1
		#----gap in used opcodes----
		elif instword=="gotoA":
			instcnt += 1
			autostpflg=1
		elif instword=="gotoAif":
			instcnt += 1
		elif instword=="gotoB":
			instcnt += 1
			autostpflg=1
		elif instword=="gotoBif":
			instcnt += 1
		elif instword=="gotoC":
			instcnt += 1
		elif instword=="gotoCif":
			instcnt += 1
		elif instword=="gotoD":
			instcnt += 1
		elif instword=="gotoDif":
			instcnt += 1
		elif instword=="gotoE":
			instcnt += 1
		elif instword=="gotoEif":
			instcnt += 1
		elif instword=="gotoF":
			instcnt += 1
		elif instword=="gotoFif":
			instcnt += 1
		#----gap in used opcodes----
		elif instword=="dumpreg1":
			instcnt += 1
		elif instword=="dumpreg2":
			instcnt += 1
		elif instword=="TTYwrite":
			instcnt += 1
		elif instword=="buzzer":
			instcnt += 1
		elif instword=="setregset":
			instcnt += 1
		elif instword=="regset":
			instcnt += 1
		elif instword=="setkeyint":
			instcnt += 1
		elif instword=="keyint":
			instcnt += 1
		elif instword=="offsetlen":
			instcnt += 1
		elif instword=="clearkeyint":
			instcnt += 1
		elif instword=="gotoifgreater":
			instcnt += 1
		elif instword=="TTYbg":
			instcnt += 2
			#this flag MUST be set to 2 on dual-instruction keywords like the regset macros here.
			#this is only for the prescan pass as its needed to properly calculate gotorefrence labels.
			instlenflg=2
		elif instword=="TTYlinedraw":
			instcnt += 2
			instlenflg=2
		elif instword=="TTYmode":
			instcnt += 2
			instlenflg=2
		elif instword=="threadref":
			instcnt += 1
		elif instword=="threadstart":
			instcnt += 1
		elif instword=="threadstop":
			instcnt += 1
		elif instword=="threadkill":
			instcnt += 1
		elif instword=="ptread":
			instcnt += 1
		elif instword=="ptwri":
			instcnt += 1
		elif instword=="ptwridat":
			instcnt += 1
		elif instword=="ptinc":
			instcnt += 1
		elif instword=="ptdec":
			instcnt += 1
		elif instword=="ptset":
			instcnt += 1
		elif instword=="ptadd":
			instcnt += 1
		elif instword=="ptget":
			instcnt += 1
		else:
			gtflag=0
		if gtflag==1 and (txtblk==0 or linenraw=="textstart"):
			complog("pass 1: srcline:" + str(srcline) + " instcnt:" + str(instcnt) + " inst:" + instword + " instdat:" +  instdat + "\n")
		elif gtflag==1 and txtblk==1:
			complog("TEXTBLOCK: pass 1 : srcline:" + str(srcline) + " instcnt:" + str(instcnt) + " textline: \"" + linenraw + "\"\n")
		#gotoref label processing. (populates gotoreflist (used by gotoref pointers in second pass))
		if (len(linelist))==3 and gtflag==1 and txtblk==0 and instword[0]!="#":
			if instword=="textstart":
				instcnt += 1
			gtox=gotoref((instcnt - instlenflg), linelist[2])
			gotoreflist.extend([gtox])
			
			
			print ("found gotoref: \"" + linelist[2] + "\", at instruction:\"" + str((instcnt - 1)) + "\", Source line:\"" + str(srcline) + "\"")
			complog("found gotoref: \"" + linelist[2] + "\", at instruction:\"" + str((instcnt - 1)) + "\", Source line:\"" + str(srcline) + "\"\n")
			if instword=="textstart":
				instcnt -= 1
	#Second Pass (Primary pass)
	#print gotoreflist
	instcnt=0
	firstloop=1
	srcline=0
	for linen in sourcefileB:
		srcline += 1
		if firstloop==1:
			print "preforming compileloop startup..."
			complog("\n\npreforming compileloop startup...\n")
			assmflename=arg
			complog("source file: \"" + assmflename + "\"\n")
			assmnamelst=assmflename.rsplit('.', 1)
			outfile=(assmnamelst[0] + (".trom"))
			complog("output file: \"" + outfile + "\"\n")
			outn = open(outfile, 'w')
			firstloop=0
			print "done. begin compile."
			complog("done. begin compile.\n")
		lined=linen
		
		linen=linen.replace("\n", "")
		linen=linen.replace("	", "")
		linenraw=linen
		linen=(linen.split("#"))[0]
		linen=linen.replace(";", "|")
		linelist=linen.split("|")
		autostpflg=0
		gtflag=1
		if (len(linelist))==2 or (len(linelist))==3:
			instword=(linelist[0])
			instdat=(linelist[1])
		else:
			instword=(linelist[0])
			instdat="000000000"
		if instdat=="":
			instdat="000000000"
			print "NOTICE: data portion at source line:\"" + str(srcline) + "\" blank, defaulting to ground..."
			complog("NOTICE: data portion at source line:\"" + str(srcline) + "\" blank, defaulting to ground...\n")
		#if len(instdat)==6 and instdat[0]!=">" and instdat[0]!=":":
		#	print "Mark 1.x legacy NOTICE: instruction \"" + instword + "\" at \"" + str(srcline) + "\"  did not have 9 trits data. it has been padded far from radix. please pad any legacy instructions manually."
		#	complog("Mark 1.x legacy NOTICE: instruction \"" + instword + "\" at \"" + str(srcline) + "\"  did not have 9 trits data. it has been padded far from radix. please pad any legacy instructions manually.\n")
		#	instdat=("000" + instdat)
		if instword=="textstop":
			txtblk=0
			complog("TEXTBLOCK END\n")
		if txtblk==1:
			for f in lined:
				texchout=libSBTCVM.charlook(f)
				texchout=("000" + texchout)
				outn.write("--+++0" + (texchout) + "\n")
				instcnt += 1
		elif instword=="textstart":
			txtblk=1
			complog("TEXTBLOCK START\n")
		#raw class
		elif instword=="romread1":
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("------" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("------" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
			
		elif instword=="romread2":
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("-----0" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("-----0" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
		elif instword=="IOread1":
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("-----+" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				try:
					IOpnk=IOmapread[instgpe[1]]
					outn.write("-----+" + IOpnk + "\n")
				except KeyError:
					#print "ERROR: IO read shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: IO read shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: IO read shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
				instcnt += 1
			#outn.write("-----+" + instdat + "\n")
			#instcnt += 1
		elif instword=="IOread2":
			#outn.write("----0-" + instdat + "\n")
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("----0-" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				try:
					IOpnk=IOmapread[instgpe[1]]
					outn.write("----0-" + IOpnk + "\n")
				except KeyError:
					#print "ERROR: IO read shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: IO read shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: IO read shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
				instcnt += 1
			#instcnt += 1
		elif instword=="IOwrite1":
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("----00" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				try:
					IOpnk=IOmapwrite[instgpe[1]]
					outn.write("----00" + IOpnk + "\n")
				except KeyError:
					#print "ERROR: IO write shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: IO write shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: IO write shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
				instcnt += 1
			#instcnt += 1
		elif instword=="IOwrite2":
			#outn.write("----0+" + instdat + "\n")
			#instcnt += 1
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("----0+" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				try:
					IOpnk=IOmapwrite[instgpe[1]]
					outn.write("----0+" + IOpnk + "\n")
				except KeyError:
					#print "ERROR: IO write shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: IO write shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: IO write shortcut: \"" + instgpe[1] + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
				instcnt += 1
		elif instword=="regswap":
			outn.write("----+-" + instdat + "\n")
			instcnt += 1
		elif instword=="copy1to2":
			outn.write("----+0" + instdat + "\n")
			instcnt += 1
		elif instword=="copy2to1":
			outn.write("----++" + instdat + "\n")
			instcnt += 1
		elif instword=="invert1":
			outn.write("---0--" + instdat + "\n")
			instcnt += 1
		elif instword=="invert2":
			outn.write("---0-0" + instdat + "\n")
			instcnt += 1
		elif instword=="add":
			outn.write("---0-+" + instdat + "\n")
			instcnt += 1
		elif instword=="subtract":
			outn.write("---00-" + instdat + "\n")
			instcnt += 1
		elif instword=="multiply":
			outn.write("---000" + instdat + "\n")
			instcnt += 1
		elif instword=="divide":
			outn.write("---00+" + instdat + "\n")
			instcnt += 1
		elif instword=="setreg1":
			#outn.write("---0+-" + instdat + "\n")
			#instcnt += 1
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("---0+-" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("---0+-" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")

		elif instword=="setreg2":
		#	outn.write("---0+0" + instdat + "\n")
			#instcnt += 1
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("---0+0" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("---0+0" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")

		elif instword=="setinst":
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("---0++" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("---0++" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
		elif instword=="setdata":
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("---+--" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("---+--" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
		#----jump in used opcodes----
		elif instword=="continue":
			outn.write("---+++" + instdat + "\n")
			instcnt += 1
		#color drawing
		elif instword=="colorpixel":
			outn.write("--0---" + instdat + "\n")
			instcnt += 1
		elif instword=="setcolorreg":
			instclst=instdat.split(',')
			if len(instclst)==3:
				vxR=libSBTCVM.codeshift(instclst[0])
				vxB=libSBTCVM.codeshift(instclst[1])
				vxG=libSBTCVM.codeshift(instclst[2])
				outn.write("--0--0" + ("000" + vxR + vxB + vxG) + "\n")
			else:
				outn.write("--0--0" + instdat + "\n")
			instcnt += 1
		elif instword=="colorfill":
			instclst=instdat.split(',')
			if len(instclst)==3:
				vxR=libSBTCVM.codeshift(instclst[0])
				vxB=libSBTCVM.codeshift(instclst[1])
				vxG=libSBTCVM.codeshift(instclst[2])
				
				outn.write("--0--+" + ("000" + vxR + vxB + vxG) + "\n")
			else:
				outn.write("--0--+" + instdat + "\n")
			instcnt += 1
		elif instword=="setcolorvect":
			outn.write("--0-0-" + instdat + "\n")
			instcnt += 1
		elif instword=="colorline":
			outn.write("--0-00" + instdat + "\n")
			instcnt += 1
		elif instword=="colorrect":
			outn.write("--0-0+" + instdat + "\n")
			instcnt += 1
		#mono drawing
		elif instword=="monopixel":
			outn.write("--0-+-" + instdat + "\n")
			instcnt += 1
		elif instword=="monofill":
			outn.write("--0-+0" + instdat + "\n")
			instcnt += 1
		elif instword=="setmonovect":
			outn.write("--0-++" + instdat + "\n")
			instcnt += 1
		elif instword=="monoline":
			outn.write("--00--" + instdat + "\n")
			instcnt += 1
		elif instword=="monorect":
			outn.write("--00-0" + instdat + "\n")
			instcnt += 1
		#----opcode --00-+ unused----
		elif instword=="stop":
			outn.write("--000-" + instdat + "\n")
			instcnt += 1
			autostpflg=1
		elif instword=="null":
			outn.write("000000" + instdat + "\n")
			instcnt += 1
		elif instword=="gotodata":
			instgpe=instdat.split(">")
			autostpflg=1
			if (len(instgpe))==1:
				outn.write("--000+" + instdat + "\n")#
				instcnt += 1
				
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("--000+" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
				
		elif instword=="gotoreg1":
			outn.write("--00+-" + instdat + "\n")
			instcnt += 1
			autostpflg=1
		elif instword=="gotodataif":
			instgpe=instdat.split(">")
			autostpflg=1
			if (len(instgpe))==1:
				outn.write("--00+0" + instdat + "\n")#
				instcnt += 1
				
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("--00+0" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
					
		elif instword=="gotoifgreater":
			instgpe=instdat.split(">")
			autostpflg=1
			if (len(instgpe))==1:
				outn.write("--0+0-" + instdat + "\n")#
				instcnt += 1
				
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("--0+0-" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
			#instcnt += 1
		elif instword=="wait":
			outn.write("--00++" + instdat + "\n")
			instcnt += 1
		elif instword=="YNgoto":
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("--0+--" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("--0+--" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
		elif instword=="userwait":
			outn.write("--0+-0" + instdat + "\n")
			instcnt += 1
		elif instword=="TTYclear":
			outn.write("--0+-+" + instdat + "\n")
			instcnt += 1
		#----gap in used opcodes----
		elif instword=="gotoA":
			outn.write("--+---" + instdat + "\n")
			instcnt += 1
			autostpflg=1
		elif instword=="gotoAif":
			outn.write("--+--0" + instdat + "\n")
			instcnt += 1
		elif instword=="gotoB":
			outn.write("--+--+" + instdat + "\n")
			instcnt += 1
			autostpflg=1
		elif instword=="gotoBif":
			outn.write("--+-0-" + instdat + "\n")
			instcnt += 1
		elif instword=="gotoC":
			outn.write("--+-00" + instdat + "\n")
			instcnt += 1
			autostpflg=1
		elif instword=="gotoCif":
			outn.write("--+-0+" + instdat + "\n")
			instcnt += 1
		elif instword=="gotoD":
			outn.write("--+-+-" + instdat + "\n")
			instcnt += 1
			autostpflg=1
		elif instword=="gotoDif":
			outn.write("--+-+0" + instdat + "\n")
			instcnt += 1
		elif instword=="gotoE":
			outn.write("--+-++" + instdat + "\n")
			instcnt += 1
			autostpflg=1
		elif instword=="gotoEif":
			outn.write("--+0--" + instdat + "\n")
			instcnt += 1
		elif instword=="gotoF":
			outn.write("--+0-0" + instdat + "\n")
			instcnt += 1
			autostpflg=1
		elif instword=="gotoFif":
			outn.write("--+0-+" + instdat + "\n")
			instcnt += 1
		#----gap in used opcodes----
		elif instword=="dumpreg1":
			outn.write("--++0+" + instdat + "\n")
			instcnt += 1
		elif instword=="dumpreg2":
			outn.write("--+++-" + instdat + "\n")
			instcnt += 1
		elif instword=="TTYwrite":
			#outn.write("--+++0" + instdat + "\n")
			#instcnt += 1
			instgpe=instdat.split(":")
			if (len(instgpe))==1:
				outn.write("--+++0" + instdat + "\n")
				instcnt += 1
			else:
				if instgpe[1]=="enter":
					ksc="\n"
				elif instgpe[1]=="space":
					ksc=" "
				else:
					ksc=(instgpe[1])[0]
				outn.write("--+++0" + "000" + (libSBTCVM.charlook(ksc)) + "\n")
				instcnt += 1
		elif instword=="buzzer":
			outn.write("--++++" + instdat + "\n")
			instcnt += 1
		elif instword=="setregset":
			outn.write("-0-000" + instdat + "\n")
			instcnt += 1
		elif instword=="regset":
			outn.write("-0-00+" + instdat + "\n")
			instcnt += 1
		
		elif instword=="setkeyint":
			instgpe=instdat.split(":")
			if (len(instgpe))==1:
				outn.write("-0-+++" + instdat + "\n")
				instcnt += 1
			else:
				if instgpe[1]=="space":
					ksc=" "
				elif instgpe[1]=="enter":
					ksc="\n"
				else:
					ksc=(instgpe[1])[0]
				outn.write("-0-+++" + "00000" + (libSBTCVM.texttoscan[ksc]) + "\n")
				instcnt += 1
		elif instword=="keyint":
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("-00---" + instdat + "\n")#
				instcnt += 1
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("-00---" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
		elif instword=="clearkeyint":
			outn.write("-00--0" + instdat + "\n")
			instcnt += 1
		elif instword=="offsetlen":
			instclst=instdat.split(",")
			if len(instclst)==3:
				tritgnd=instclst[0]
				tritoffset=int(instclst[1])
				tritlen=int(instclst[2])
				if tritgnd=="on":
					tritgndpar="+"
				else:
					tritgndpar="0"
				if tritoffset==0:
					tritoffsetpar="--"
				elif tritoffset==1:
					tritoffsetpar="-0"
				elif tritoffset==2:
					tritoffsetpar="-+"
				elif tritoffset==3:
					tritoffsetpar="0-"
				elif tritoffset==4:
					tritoffsetpar="00"
				elif tritoffset==5:
					tritoffsetpar="0+"
				elif tritoffset==6:
					tritoffsetpar="+-"
				elif tritoffset==7:
					tritoffsetpar="+0"
				elif tritoffset==8:
					tritoffsetpar="++"
				else:
					tritoffsetpar="--"
				if tritlen==1:
					tritlenpar="--"
				elif tritlen==2:
					tritlenpar="-0"
				elif tritlen==3:
					tritlenpar="-+"
				elif tritlen==4:
					tritlenpar="0-"
				elif tritlen==5:
					tritlenpar="00"
				elif tritlen==6:
					tritlenpar="0+"
				elif tritlen==7:
					tritlenpar="+-"
				elif tritlen==8:
					tritlenpar="+0"
				elif tritlen==9:
					tritlenpar="++"
				else:
					tritlenpar="++"
				outn.write("-0-++0" + "0000" + tritgndpar + tritoffsetpar + tritlenpar + "\n")
			else:
				outn.write("-0-++0" + instdat + "\n")
			instcnt += 1
		#special regset shortcut commands
		elif instword=="TTYbg":
			instclst=instdat.split(",")
			if len(instclst)==3:
				vxR=libSBTCVM.codeshift(instclst[0])
				vxB=libSBTCVM.codeshift(instclst[1])
				vxG=libSBTCVM.codeshift(instclst[2])
				outn.write("-0-000" + "---------" + "\n")
				outn.write("-0-00+" + ("000" + vxR + vxB + vxG) + "\n")
			else:
				outn.write("-0-000" + "---------" + "\n")
				outn.write("-0-00+" + instdat + "\n")
			instcnt += 2
		elif instword=="TTYlinedraw":
			if instdat=="on":
				outn.write("-0-000" + "--------0" + "\n")
				outn.write("-0-00+" + "00000000+" + "\n")
			elif instdat=="off":
				outn.write("-0-000" + "--------0" + "\n")
				outn.write("-0-00+" + "000000000" + "\n")
			else:
				outn.write("-0-000" + "--------0" + "\n")
				outn.write("-0-00+" + "00000000+" + "\n")
				
			instcnt += 2
		elif instword=="TTYmode":
			if instdat=="27":
				outn.write("-0-000" + "--------+" + "\n")
				outn.write("-0-00+" + "00000000+" + "\n")
			elif instdat=="54":
				outn.write("-0-000" + "--------+" + "\n")
				outn.write("-0-00+" + "000000000" + "\n")
			else:
				outn.write("-0-000" + "--------+" + "\n")
				outn.write("-0-00+" + "000000000" + "\n")
				
			instcnt += 2
		elif instword=="threadref":
			instcnt += 1
			if len(instdat)==2:
				outn.write("--+00-" + "0000000" + instdat + "\n")
			else:
				outn.write("--+00-" + instdat + "\n")
		elif instword=="threadstart":
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("--+000" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("--+000" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
		elif instword=="threadstop":
			instcnt += 1
			outn.write("--+00+" + instdat + "\n")
		elif instword=="threadkill":
			instcnt += 1		
			outn.write("--+0+-" + instdat + "\n")
		#thread pointer
		elif instword=="ptread":
			instcnt += 1
			outn.write("-0-0+0" + instdat + "\n")
		elif instword=="ptwri":
			instcnt += 1
			outn.write("-0-0++" + instdat + "\n")
		elif instword=="ptwridat":
			#instcnt += 1
			instgpe=instdat.split(">")
			if (len(instgpe))==1:
				outn.write("-0-+--" + instdat + "\n")#
				instcnt += 1
				autostpflg=1
			else:
				gtpoint=instgpe[1]
				gtmatch=0
				instcnt += 1
				for fx in gotoreflist:
					if fx.gtname==gtpoint:
						outn.write("-0-+--" + fx.tline + "\n")
						gtmatch=1
				if gtmatch==0:
					#print "ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP"
					complog("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP \n")
					sys.exit("ERROR: pointer: \"" + gtpoint + "\" Pointed at by: \"" +  instword + "\" At line: \"" + str(srcline) + "\", not found. STOP")
		elif instword=="ptinc":
			instcnt += 1
			outn.write("-0-0+-" + "--0000000" + "\n")
		elif instword=="ptdec":
			instcnt += 1
			outn.write("-0-0+-" + "-00000000" + "\n")
		elif instword=="ptset":
			instcnt += 1
			outn.write("-0-0+-" + "-+0000000" + "\n")
		elif instword=="ptadd":
			instcnt += 1
			outn.write("-0-0+-" + "0-0000000" + "\n")
		elif instword=="ptget":
			instcnt += 1
			outn.write("-0-0+-" + "000000000" + "\n")
		else:
			gtflag=0
		
		if gtflag==1 and (txtblk==0 or linenraw=="textstart"):
			complog("pass 2: srcline:" + str(srcline) + " instcnt:" + str(instcnt) + " inst:" + instword + " instdat:" +  instdat + "\n")
		elif gtflag==1 and txtblk==1:
			complog("TEXTBLOCK: pass 2 : srcline:" + str(srcline) + " instcnt:" + str(instcnt) + " textline: \"" + linenraw + "\"\n")
		if instcnt>assmoverrun:
			#print("ERROR!: assembler has exceded rom size limit of 19683!")
			complog("ERROR!: assembler has exceded rom size limit of 19683! \n")
			sys.exit("ERROR!: assembler has exceded rom size limit of 19683!")
	
	if txtblk==1:
		print "WARNING: unclosed Text block!"
		complog("WARNING: unclosed Text block!\n")
	
	if instcnt==0:
		#print "ERROR: No instructions found. nothing to compile."
		complog("ERROR: No instructions found. nothing to compile. /n")
		sys.exit("ERROR: No instructions found. nothing to compile.")
	if autostpflg==0 and instcnt<19683:
		print "NOTICE: no explicit goto or stop instruction at end of program.  SBTCVM-asm will add a stop automatically."
		complog("NOTICE: no explicit goto or stop instruction at end of program.  SBTCVM-asm will add a stop automatically.\n")
		outn.write("--000-" + "000000000" + "\n")
		instcnt += 1
	
	instpad=instcnt
	while instpad!=19683 and instcnt<19684:
		outn.write("000000" + "000000000" + "\n")
		instpad += 1
	outn.close()
	
	instextra=(instpad - instcnt)
	print ("SBTCVM Mk 2 assembly file \"" + assmflename + "\" has been compiled into: \"" + outfile + "\"")
	complog("SBTCVM Mk 2 assembly file \"" + assmflename + "\" has been compiled into: \"" + outfile + "\"\n")
	if tracecomp==1:
		print "tracelog enabled. log file: \"" + (os.path.join('CAP', logsub)) + "\""
	print ("total instructions: " + str(instcnt))
	complog("total instructions: " + str(instcnt) + "\n")
	print ("extra space: " + str(instextra))
	complog ("extra space: " + str(instextra) + "\n")
else:
	print "tip: use SBTCVM-asm2.py -h for help."
