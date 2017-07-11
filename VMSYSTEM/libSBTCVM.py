#!/usr/bin/env python
import libbaltcalc
import pygame
import array
import math
import time
import os

#SBTCVM common function library.

#SBTCVM Mark 2
#Simple Balanced Ternary Computer Virtual Machine
#
#v2.0.1
#
#(c)2016-2017 Thomas Leathers and Contributors
#
#  SBTCVM Mark 2 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  SBTCVM Mark 2 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with SBTCVM Mark 2. If not, see <http://www.gnu.org/licenses/>

valfchars=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "_"] 

#used to create things like log names.
#such as asssembler tracelogs and VM execlogs
def namecrunch(fnameraw, apendtoend):
	namx=fnameraw.lower()
	namx=namx.replace("/", "-")
	namx=namx.replace("\\", "-")
	namx=namx.replace("~", "")
	#namx=namx.split(".")
	namq=namx
	namn=namq
	for RENX in namq:
		if RENX not in valfchars:
			namn=namn.replace(RENX, "_")
	return (namn + apendtoend)

def trunkto4(code):
	codecnt=0
	for fel in code:
		codecnt +=1
	if codecnt<4:
		if codecnt==3:
			return("0" + code)
		if codecnt==2:
			return("00" + code)
		if codecnt==1:
			return("000" + code)
	#code=libbaltcalc.BTINVERT(code)
	return(code)

def trunkto5(code):
	codecnt=0
	for fel in code:
		codecnt +=1
	if codecnt<5:
		if codecnt==4:
			return("0" + code)
		if codecnt==3:
			return("00" + code)
		if codecnt==2:
			return("000" + code)
		if codecnt==1:
			return("0000" + code)
	#code=libbaltcalc.BTINVERT(code)
	return(code)

#used to get linear adress point number in decimal (for example for fiding an adress in the rom)
def numstruct(code):
	strut1=(libbaltcalc.BTTODEC(code))
	strut2=(strut1 + 9842)
	#print strut2
	return strut2

#used by the buzzer (do not use for 9 trit numtructs. use normal numstruct for that!)
def buzznumstruct5(code):
	strut1=(libbaltcalc.BTTODEC(code))
	strut2=(strut1 + 122)
	#print strut2
	return strut2
	
def drawnumstruct3(code):
	strut1=(libbaltcalc.BTTODEC(code))
	strut2=(strut1 + 13)
	#print strut2
	return strut2

def drawnumstruct2(code):
	strut1=(libbaltcalc.BTTODEC(code))
	strut2=(strut1 + 4)
	#print strut2
	return strut2
#raster draw support

VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")
def stregload(filenameg):
	if os.path.isfile(filenameg):
		return(filenameg)
	elif os.path.isfile(os.path.join("ROMS", filenameg)):
		return(os.path.join("ROMS", filenameg))
	elif os.path.isfile(os.path.join("VMUSER", filenameg)):
		return(os.path.join("VMUSER", filenameg))
	elif os.path.isfile(os.path.join("VMSYSTEM", filenameg)):
		return(os.path.join("VMSYSTEM", filenameg))
	elif os.path.isfile(os.path.join(VMSYSROMS, filenameg)):
		return(os.path.join(VMSYSROMS, filenameg))
	else:
		#print ("FATAL ERROR: libtrom: NONEXISTENT TROM! (" + filenameg + ")")
		sys.exit("FATAL ERROR: libtrom: NONEXISTENT STREG! (" + filenameg + ")")

#used by color channels of color raster, and by monochrome raster shades.
def dollytell(lookupcode):
	if lookupcode=="--":
		return("0")
	if lookupcode=="-0":
		return("32")
	if lookupcode=="-+":
		return("64")
	if lookupcode=="0-":
		return("96")
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

#converts a 6-trit RGB color code into a color pygame can use.
def colorfind(CODE):
	REDBT = (CODE[0] + CODE[1])
	GRNBT = (CODE[2] + CODE[3])
	BLUBT = (CODE[4] + CODE[5])
	REDBIN = (dollytell(REDBT))
	GRNBIN = (dollytell(GRNBT))
	BLUBIN = (dollytell(BLUBT))
	#NAME = datalist
	return((int(REDBIN), int(GRNBIN), int(BLUBIN)))

#returns pygame rectangle from 2 points used to draw vector filled rectangles
def makerectbipoint(Jx1, Jy1, Jx2, Jy2):
	if Jx1>Jx2:
		sizeX=(Jx1-Jx2)
		xval=Jx2
	else:
		sizeX=(Jx2-Jx1)
		xval=Jx1
	if Jy1>Jy2:
		yval=Jy2
		sizeY=(Jy1-Jy2)
	else:
		sizeY=(Jy2-Jy1)
		yval=Jy1
	sizeY += 1
	sizeX += 1
	return(pygame.Rect((xval, yval), (sizeX, sizeY)))

#more intelegent truncation function (used in the math functions for example)
def trunkto6(code):
	codecnt=0
	for fel in code:
		codecnt +=1
	if codecnt<9:
		if codecnt==8:
			return("0" + code)
		if codecnt==7:
			return("00" + code)
		if codecnt==6:
			return("000" + code)
		if codecnt==5:
			return("0000" + code)
		if codecnt==4:
			return("00000" + code)
		if codecnt==3:
			return("000000" + code)
		if codecnt==2:
			return("0000000" + code)
		if codecnt==1:
			return("00000000" + code)
	#print code
	#code=libbaltcalc.BTINVERT(code)
	return((code[0]) + (code[1]) + (code[2]) + (code[3]) + (code[4]) + (code[5]) + (code[6]) + (code[7]) + (code[8]))






def trunkto6math(code):
	codecnt=0
	for fel in code:
		codecnt +=1
	if codecnt<9:
		if codecnt==8:
			return("0" + code)
		if codecnt==7:
			return("00" + code)
		if codecnt==6:
			return("000" + code)
		if codecnt==5:
			return("0000" + code)
		if codecnt==4:
			return("00000" + code)
		if codecnt==3:
			return("000000" + code)
		if codecnt==2:
			return("0000000" + code)
		if codecnt==1:
			return("00000000" + code)
	#print code
	#code=libbaltcalc.BTINVERT(code)

	#print code
	#code=libbaltcalc.BTINVERT(code)
	if codecnt>9:
		#print "integer overflow"
		if code[0]=="+":
			code="---------"
		elif code[0]=="-":
			code="+++++++++"
		else:
			code="---------"
	return((code[0]) + (code[1]) + (code[2]) + (code[3]) + (code[4]) + (code[5]) + (code[6]) + (code[7]) + (code[8]))

#print(trunkto6("---0+++"))
#print(trunkto6("--0+++"))
#print(trunkto6("-0+++"))
#print(trunkto6("0+++"))
#print(trunkto6("+++"))
#print(trunkto6("++"))
#print(trunkto6("+"))

def abtslackline(receveabt, linetext):
	interx=[(receveabt[1]), (receveabt[2]),(receveabt[3]), (receveabt[4]), (receveabt[5]), (receveabt[6]), (receveabt[7]), (receveabt[8]), (receveabt[9]), (receveabt[10]), (receveabt[11]), (receveabt[12]), (receveabt[13]), (receveabt[14]), (receveabt[15]), (receveabt[16]), (receveabt[17]), (receveabt[18]), (receveabt[19]), (receveabt[20]), (receveabt[21]), (receveabt[22]), (receveabt[23]), (receveabt[24]), (receveabt[25]),(receveabt[26]), (linetext)]
	return interx

def abtcharblit(receveabtb, charblit):
	if charblit=="\n":
		receveabtb=abtslackline(receveabtb, "")
	else:
		charnum=0
		curr=receveabtb[26]
		for f in curr:
			if charnum==36:
				receveabtb=abtslackline(receveabtb, "")
			charnum += 1
		receveabtb[26]=((receveabtb[26]) + charblit)
	return(receveabtb)

#sound functions
	
def mk1buzz(code):
	timechar=code[0]
	#print timechar
	if timechar=="+":
		timemag=60
	elif timechar=="-":
		timemag=20
	else:
		timemag=40
	freqcode=((code[1]) + (code[2]) + (code[3]) + (code[4]) +(code[5]))
	#print freqcode
	baserep=160
	repjump=2
	magn=buzznumstruct5(libbaltcalc.BTINVERT(freqcode))
	magn=(243 - magn + 20)
	
	repadd=(repjump * magn)
	#samplmag=sqblksnd((baserep + repadd), (20))
	#sampltnk=samplmag[:6480]
	if timechar=="+":
		#sampltnk=(sampltnk + sampltnk + sampltnk + sampltnk + sampltnk)
		sampltnk=autosquare(repadd, 0.3)
	elif timechar=="-":
		sampltnk=autosquare(repadd, 0.1)
		#sampltnk=(sampltnk)
		
	else:
		#sampltnk=(sampltnk + sampltnk + sampltnk)
		sampltnk=autosquare(repadd, 0.2)
	#print sampltnk
	return sampltnk

def foobsin(num):
	#return math.sin(math.sin(math.sin(num)))
	#return math.sin(math.sin(num))
	return (math.floor(math.sin(num)) * 4500)


def autosquare(freq, lenth):
	temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

#SBTC Graphics operations (currently just TUI routines, future plans include actual graphics modes.

pygame.font.init()
simplefont = pygame.font.SysFont(None, 16)


fondir=os.path.join("VMSYSTEM", "FONT0")
fondir2=os.path.join("VMSYSTEM", "FONT1")


def abtslackline(receveabt, linetext):
	interx=[(receveabt[1]), (receveabt[2]),(receveabt[3]), (receveabt[4]), (receveabt[5]), (receveabt[6]), (receveabt[7]), (receveabt[8]), (receveabt[9]), (receveabt[10]), (receveabt[11]), (receveabt[12]), (receveabt[13]), (receveabt[14]), (receveabt[15]), (receveabt[16]), (receveabt[17]), (receveabt[18]), (receveabt[19]), (receveabt[20]), (receveabt[21]), (receveabt[22]), (receveabt[23]), (receveabt[24]), (receveabt[25]), (receveabt[26]), (receveabt[27]), (receveabt[28]), (receveabt[29]), (receveabt[30]), (receveabt[31]), (receveabt[32]), (receveabt[33]), (receveabt[34]), (receveabt[35]), (receveabt[36]), (receveabt[37]), (receveabt[38]), (receveabt[39]), (receveabt[40]), (receveabt[41]), (receveabt[42]), (receveabt[43]), (receveabt[44]), (receveabt[45]), (receveabt[46]), (receveabt[47]), (receveabt[48]), (receveabt[49]), (receveabt[50]), (receveabt[51]), (receveabt[52]), (receveabt[53]), (linetext)]
	if linetext=="":
		print ("TTY|" + receveabt[53])
	else:
		#print ("TTYL|" + linetext)
		print ("TTY|" + receveabt[53])
	return interx
newl=1
def abtcharblit(receveabtb, charblit):
	global newl
	newl=0
	if charblit=="\n":
		newl=1
		receveabtb=abtslackline(receveabtb, "")
	else:
		charnum=0
		curr=receveabtb[53]
		for f in curr:
			if charnum==71:
				receveabtb=abtslackline(receveabtb, "")
				newl=1
			charnum += 1
		receveabtb[53]=((receveabtb[53]) + charblit)
	return(receveabtb)

def getnewlstate():
	global newl
	if newl==1:
		return(1)
		newl=0
	else:
		return(0)

def charblit(chsurface, colx, liney, charcode):
	colx=(colx*9)
	liney=(liney*9)
	glifcode=charcodedict.get(charcode)
	#print glifcode
	gliffile=(chargliph.get(glifcode))
	#print gliffile
	#glif=pygame.image.load(os.path.join(fondir, (chargliph.get(glifcode))))
	glif=chargliphfileopt[glifcode]
	xg=chsurface.blit(glif, (colx, liney))
	return (chsurface, xg)

def charblit2(chsurface, colx, liney, charcode):
	colx=(colx*9)
	liney=(liney*18)
	glifcode=charcodedict.get(charcode)
	#print glifcode
	gliffile=(chargliph.get(glifcode))
	#print gliffile
	#glif=pygame.image.load(os.path.join(fondir, (chargliph.get(glifcode))))
	glif=chargliphfileopt2[glifcode]
	xg=chsurface.blit(glif, (colx, liney))
	return (chsurface, xg)
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
	return"00"


#Text encoding tables

charcodedict = {"------": "a", "-----0": "b", "-----+": "c", "----0-": "d", "----00": "e", "----0+": "f", "----+-": "g", "----+0": "h", "----++": "i", "---0--": "j", "---0-0": "k", "---0-+": "l", "---00-": "m", "---000": "n", "---00+": "o", "---0+-": "p", "---0+0": "q", "---0++": "r", "---+--": "s", "---+-0": "t", "---+-+": "u", "---+0-": "v", "---+00": "w", "---+0+": "x", "---++-": "y", "---++0": "z", "---+++": "A", "--0---": "B", "--0--0": "C", "--0--+": "D", "--0-0-": "E", "--0-00": "F", "--0-0+": "G", "--0-+-": "H", "--0-+0": "I", "--0-++": "J", "--00--": "K", "--00-0": "L", "--00-+": "M", "--000-": "N", "--0000": "O", "--000+": "P", "--00+-": "Q", "--00+0": "R", "--00++": "S", "--0+--": "T", "--0+-0": "U", "--0+-+": "V", "--0+0-": "W", "--0+00": "X", "--0+0+": "Y", "--0++-": "Z", "--0++0": "0", "--0+++": "1", "--+---": "2", "--+--0": "3", "--+--+": "4", "--+-0-": "5", "--+-00": "6", "--+-0+": "7", "--+-+-": "8", "--+-+0": "9", "--+-++": "`", "--+0--": "~", "--+0-0": "!", "--+0-+": "@", "--+00-": "#", "--+000": "$", "--+00+": "%", "--+0+-": "^", "--+0+0": "&", "--+0++": "*", "--++--": "(", "--++-0": ")", "--++-+": "-", "--++0-": "=", "--++00": "_", "--++0+": "+", "--+++-": "[", "--+++0": "]", "--++++": "\\", "-0----": "{", "-0---0": "}", "-0---+": "|", "-0--0-": ";", "-0--00": "\'", "-0--0+": ",", "-0--+-": ".", "-0--+0": "/", "-0--++": ":", "-0-0--": '\"', "-0-0-0": "<", "-0-0-+": ">", "-0-00-": "?", "-0-000": "\n", "-0-00+": " "}
#primary character lookup dictionary (returns code of a character)
charlookupdict={"a": "------", "b": "-----0", "c": "-----+", "d": "----0-", "e": "----00", "f": "----0+", "g": "----+-", "h": "----+0", "i": "----++", "j": "---0--", "k": "---0-0", "l": "---0-+", "m": "---00-", "n": "---000", "o": "---00+", "p": "---0+-", "q": "---0+0", "r": "---0++", "s": "---+--", "t": "---+-0", "u": "---+-+", "v": "---+0-", "w": "---+00", "x": "---+0+", "y": "---++-", "z": "---++0", "A": "---+++", "B": "--0---", "C": "--0--0", "D": "--0--+", "E": "--0-0-", "F": "--0-00", "G": "--0-0+", "H": "--0-+-", "I": "--0-+0", "J": "--0-++", "K": "--00--", "L": "--00-0", "M": "--00-+", "N": "--000-", "O": "--0000", "P": "--000+", "Q": "--00+-", "R": "--00+0", "S": "--00++", "T": "--0+--", "U": "--0+-0", "V": "--0+-+", "W": "--0+0-", "X": "--0+00", "Y": "--0+0+", "Z": "--0++-", "0": "--0++0", "1": "--0+++", "2": "--+---", "3": "--+--0", "4": "--+--+", "5": "--+-0-", "6": "--+-00", "7": "--+-0+", "8": "--+-+-", "9": "--+-+0", "`": "--+-++", "~": "--+0--", "!": "--+0-0", "@": "--+0-+", "#": "--+00-", "$": "--+000", "%": "--+00+", "^": "--+0+-", "&": "--+0+0", "*": "--+0++", "(": "--++--", ")": "--++-0", "-": "--++-+", "=": "--++0-", "_": "--++00", "+": "--++0+", "[": "--+++-", "]": "--+++0", "\\": "--++++", "{": "-0----", "}": "-0---0", "|": "-0---+", ";": "-0--0-", "\'": "-0--00", ",": "-0--0+", ".": "-0--+-", "/": "-0--+0", ":": "-0--++", '\"': "-0-0--", "<": "-0-0-0", ">": "-0-0-+", "?": "-0-00-", "\n": "-0-000", " ": "-0-00+"}
#character gliph table.
chargliph={"a": "chara.gif", "b": "charb.gif", "c": "charc.gif", "d": "chard.gif", "e": "chare.gif", "f": "charf.gif", "g": "charg.gif", "h": "charh.gif", "i": "chari.gif", "j": "charj.gif", "k": "chark.gif", "l": "charl.gif", "m": "charm.gif", "n": "charn.gif", "o": "charo.gif", "p": "charp.gif", "q": "charq.gif", "r": "charr.gif", "s": "chars.gif", "t": "chart.gif", "u": "charu.gif", "v": "charv.gif", "w": "charw.gif", "x": "charx.gif", "y": "chary.gif", "z": "charz.gif", "A": "charAc.gif", "B": "charBc.gif", "C": "charCc.gif", "D": "charDc.gif", "E": "charEc.gif", "F": "charFc.gif", "G": "charGc.gif", "H": "charHc.gif", "I": "charIc.gif", "J": "charJc.gif", "K": "charKc.gif", "L": "charLc.gif", "M": "charMc.gif", "N": "charNc.gif", "O": "charOc.gif", "P": "charPc.gif", "Q": "charQc.gif", "R": "charRc.gif", "S": "charSc.gif", "T": "charTc.gif", "U": "charUc.gif", "V": "charVc.gif", "W": "charWc.gif", "X": "charXc.gif", "Y": "charYc.gif", "Z": "charZc.gif", "0": "char0.gif", "1": "char1.gif", "2": "char2.gif", "3": "char3.gif", "4": "char4.gif", "5": "char5.gif", "6": "char6.gif", "7": "char7.gif", "8": "char8.gif", "9": "char9.gif", "`": "characcent.gif", "~": "chartild.gif", "!": "charexclaim.gif", "@": "charAT.gif", "#": "charhash.gif", "$": "charUSD.gif", "%": "charPERC.gif", "^": "charCARROT.gif", "&": "charAND.gif", "*": "charATRISK.gif", "(": "charLPAR.gif", ")": "charRPAR.gif", "-": "charHYPHON.gif", "=": "charEQUAL.gif", "_": "charUNDERSC.gif", "+": "charPLUS.gif", "[": "charLBRAK.gif", "]": "charRBRAK.gif", "\\": "charBKSLASH.gif", "{": "charLCURL.gif", "}": "charRCURL.gif", "|": "charVERTBAR.gif", ";": "charsemicol.gif", "\'": "charapos.gif", ",": "charcomma.gif", ".": "charpereod.gif", "/": "charFDSLASH.gif", ":": "charcol.gif", '\"': "charDUBQTE.gif", "<": "charLESSTHAN.gif", ">": "charGREATTHAN.gif", "?": "charquestion.gif", " ": "charSPACE.gif"}

#primary character list. use to check if a character has a valid code
charscrossck=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "=", "_", "+", "[", "]", "\\", "{", "}", "|", ";", "\'", ",", ".", "/", ":", '\"', "<", ">", "?", "\n", " "]

#4-trit keyscan tables:
texttoscan={"1": "----","2": "---0","3": "---+","4": "--0-","5": "--00","6": "--0+","7": "--+-","8": "--+0","9": "--++","0": "-0--","-": "-0-0","+": "-0-+","a": "-00-","b": "-000","c": "-00+","d": "-0+-","e": "-0+0","f": "-0++","g": "-+--","h": "-+-0","i": "-+-+","j": "-+0-","k": "-+00","l": "-+0+","m": "-++-","n": "-++0","o": "-+++","p": "0---","q": "0--0","r": "0--+","s": "0-0-","t": "0-00","u": "0-0+","v": "0-+-","w": "0-+0","x": "0-++","y": "00--","z": "00-0"," ": "00-+","\n": "000-"}
scantotext={}
for keyscrev in texttoscan:
	keysccode=texttoscan[keyscrev]
	scantotext[keysccode]=keyscrev
	
#print scantotext

def charcodelook(code):
	return(charcodedict[code])

def charlook(char):
	return(charlookupdict[char])

#build banks of character images
#9x9 font
chargliphfile={}
#9x18 font
chargliphfile2={}
for fxq in chargliph:
	imgdat=chargliph[fxq]
	chargliphfile[fxq]=(pygame.image.load(os.path.join(fondir, (imgdat))))
for fxq in chargliph:
	imgdat=chargliph[fxq]
	chargliphfile2[fxq]=(pygame.image.load(os.path.join(fondir2, (imgdat))))

chargliphfileopt=chargliphfile.copy()
chargliphfileopt2=chargliphfile2.copy()
def glyphoptim(surface):
	global chargliphfileopt
	global chargliphfileopt2
	for fxq in chargliphfile:
		imgpreconv=chargliphfile[fxq]
		imgpostconv=imgpreconv.convert(surface)
		chargliphfileopt[fxq]=imgpostconv
	for fxq in chargliphfile2:
		imgpreconv=chargliphfile2[fxq]
		imgpostconv=imgpreconv.convert(surface)
		chargliphfileopt2[fxq]=imgpostconv
		

USERCONFTEMP='''#This is the USER config file.
#this is autocreated by sbtcvm

#single-rom Programs should always be on "TROMA"
#also, single-rom programs can be launched with MK2-RUN.py
#multirom programs can be launched from MK2-RUN.py through the use of streg files. 
#see intro.streg for an example.

#the default streg can be overwritten here:
#DEFAULTSTREG="intro.streg"


#enable to use step-by-step execution. makes debugging easier :) 
#(when enabled press enter to advance CPU)
#usually this should be zero "0" (aka off) set to one "1" to turn on.
#notice: this has not been updated to work with the new keyscan operations, so its usefulness varies.
#stepbystep=0

#cpu wait time (in seconds)
#the default is 0.0005 seconds. shorter delay times cause faster operation provided
#your PC has the processing power.
#CPUWAIT=(0.0005)

#default setting for readout updates
#setting this to 1 may speed up SBTCVM on some computers.
#you can toggle the readout update setting in-VM using F4
#step-by-step mode always has readouts enabled regardless of the update setting.
#disablereadouts=1

#frame skipping interval (default 1) 0=off
#fskip=1

#set this to 1 to disable TTY rendering. (you would still be able to read tty
#output, as SBTCVM mirrors the TTY to standard output.
#ttystyle=0

#LOGGING RELATED SETTINGS BELOW

#MAIN VM ENGINE:

#log execution process in CAP directory:
#Note that these logs can be VERY LONG.
#vmexeclogflg=0

#Dump EXEC MEMORY at exit (This will dump the current state of the
#troms in memory, into the CAP directory as TROMA.dmp... TROMB.dmp.. Etc.)
#useful for debugging
#logromexit=0
#log IObus on exit this logs the final state of the IObus on exit.
#logIOexit=0
#also you can issue "manual" equivalents to these via F10 (filenames will differ from exit dumps)


#LIBTROM:

#log reads. default is 0. libtrom logging must be on for this to work.
#logreads=0
#log writes. default is 0. libtrom logging must be on for this to work.
#logwrites=0
#libtrom logging. if on, libtrom will log various events in log files in CAP directory.
#tromlogging=0'''