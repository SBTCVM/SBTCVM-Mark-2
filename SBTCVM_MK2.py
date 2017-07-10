#!/usr/bin/env python
import VMSYSTEM.libtrom as libtrom
import pygame
from pygame.locals import *
import time
import os
import VMSYSTEM.libSBTCVM as libSBTCVM
import VMSYSTEM.libbaltcalc as libbaltcalc
import VMSYSTEM.libvmui as vmui
import sys
from random import randint
pygame.display.init()

print "SBTCVM Mark 2 Starting up..."

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


#thread data storage class
#used to store thread-specific data in BTSTACK dictionary when thread is inactive.
class BTTHREAD:
	def __init__(self, qxtactg, EXECADDRg, REG1g, REG2g, contaddrg, EXECADDRrawg, regsetpointg, TTYBGCOLREGg, TTYBGCOLg, colvectorregg, monovectorregg, colorregg, tritloadleng, tritoffsetg, tritdestgndg, threadrefg, ROMFILEg, ROMLAMPFLGg, mempoint):
		self.qxtact=qxtactg
		self.EXECADDR=EXECADDRg
		self.REG1=REG1g
		self.REG2=REG2g
		self.contaddr=contaddrg
		self.EXECADDRraw=EXECADDRrawg
		self.regsetpoint=regsetpointg
		self.TTYBGCOLREG=TTYBGCOLREGg
		self.TTYBGCOL=TTYBGCOLg
		self.colvectorreg=colvectorregg
		self.monovectorreg=monovectorregg
		self.colorreg=colorregg
		self.tritloadlen=tritloadleng
		self.tritoffset=tritoffsetg
		self.tritdestgnd=tritdestgndg
		self.threadref=threadrefg
		self.ROMFILE=ROMFILEg
		self.ROMLAMPFLG=ROMLAMPFLGg
		self.mempoint=mempoint
#ROMFILE=TROMA
#ROMLAMPFLG="A"


windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'icon64.png'))
pygame.display.set_icon(windowicon)

screensurf=pygame.display.set_mode((800, 600))
#


vmbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VMBG.png')).convert()
screensurf.blit(vmbg, (0, 0))
#init in non-kiosk mode for now, SBTCVM will re-init once it knows the kioskmode state.
vmui.initui(screensurf, 0)
vmui.dummyreadouts()
pygame.display.update()
libSBTCVM.glyphoptim(screensurf)
pygame.display.set_caption("SBTCVM Mark 2", "SBTCVM Mark 2")
pygame.font.init()

simplefont = pygame.font.SysFont(None, 16)
#used for smaller data displays (inst. data etc.)
#smldispfont = pygame.font.SysFont(None, 16)
smldispfont = pygame.font.Font(os.path.join("VMSYSTEM", "SBTCVMreadout.ttf"), 16)
#used in larger data displays (register displays, etc.)
#lgdispfont = pygame.font.SysFont(None, 20)
lgdispfont = pygame.font.Font(os.path.join("VMSYSTEM", "SBTCVMreadout.ttf"), 16)
pixcnt1=40
pixjmp=14
USRYN=0
USRWAIT=0

keyintreg="0000"

#ttyfont = pygame.font.SysFont("Mono", 10)
#ttyfontB =pygame.font.SysFont("Mono", 18)
#graphics:
#background pixmap

#indicator lamps
#GREEN
LEDGREENON=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-GREEN.png')).convert()
LEDGREENOFF=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-GREEN-OFF.png')).convert()
#CPU
CPULEDACT=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-BLUE.png')).convert()
CPULEDSTANDBY=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-ORANGE.png')).convert()

COLORDISP=pygame.Surface((27, 27)).convert()
MONODISP=pygame.Surface((9, 9)).convert()
COLORDISP.fill((127, 127, 127))
MONODISP.fill((127, 127, 127))

#this list is what is displayed on the TTY on VM boot.
#the header text is so far in this list so it appears correct in 27 line mode
abt=["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "SBTCVM", "Mark 2", "v2.0.1", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "ready", ""]
abtpref=["This is different", "Mark 2", "v2.0.0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "ready"]
abtclear=["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
#abt54clear=["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
#ttysize:
#0=72x54 (9x9 chars)
#1=72x27 (9x18 chars)

TTYMODE=0
TTYSIZE=1
pygame.mixer.init()

extradraw=0

wavsp=libSBTCVM.mk1buzz("0-----")
snf=pygame.mixer.Sound(wavsp)
snf.play()

#config defaults
TROMA="intro.trom"
#these are dud roms full of soft stops
TROMB=("DEFAULT.TROM")
TROMC=("DEFAULT.TROM")
TROMD=("DEFAULT.TROM")
TROME=("DEFAULT.TROM")
TROMF=("DEFAULT.TROM")
CPUWAIT=(0.0005)
stepbystep=0
scconf=open(os.path.join("VMSYSTEM", 'BOOTUP.CFG'), 'r')
exconf=compile(scconf.read(), os.path.join("VMSYSTEM", 'BOOTUP.CFG'), 'exec')

if os.path.isfile(os.path.join("VMUSER", "USERBOOT.CFG")):
	userscconf=open(os.path.join("VMUSER", "USERBOOT.CFG"), "r")
	userexconf=compile(userscconf.read(), os.path.join("VMUSER", 'USERBOOT.CFG'), 'exec')
	runuserconf=1
	print "user config found."
else:
	print "user config not found... creating user config in VMUSER..."
	userscconfcreate=open(os.path.join("VMUSER", "USERBOOT.CFG"), "w")
	userscconfcreate.write(libSBTCVM.USERCONFTEMP)
	userscconfcreate.close()
	runuserconf=0
DEFAULTSTREG="intro.streg"
tuibig=1
logromexit=0
logIOexit=0
vmexeclogflg=0
ttystyle=0

fskip=1
#set this to 1 as SBTCVM now runs too fast with default setting for these to be useful in normal execution.
#user can overide this in USERBOOT.CFG and toggle it using F4 key.
disablereadouts=1
exec(exconf)

scconf.close()
if runuserconf==1:
	#print "arg"
	exec(userexconf)
	userscconf.close()

fskipcnt=fskip

def vmexeclog(texttolog):
	if vmexeclogflg==1:
		vmexlogf.write(texttolog + "\n")
#vmexeclog("SYSTEM STARTUP. EXECUTION LOG ENABLED.")
key1=0
key2=0
key3=0
key4=0
key5=0
key6=0
key7=0
key8=0
key9=0
key0=0
keypos=0
keyhyp=0
keyq=0
keyw=0
keye=0
keyr=0
keyt=0
keyy=0
keyu=0
keyi=0
keyo=0
keyp=0
keya=0
keysx=0
keyd=0
keyf=0
keyg=0
keyh=0
keyj=0
keyk=0
keyl=0
keyz=0
keyx=0
keyc=0
keyv=0
keyb=0
keyn=0
keym=0
keyspace=0
keyret=0



btstopthread=0

TTYrenderflg="0"

if 'GLOBKIOSK' in globals():
	print "RUNNING IN KIOSK MODE."
	KIOSKMODE=GLOBKIOSK
else:
	KIOSKMODE=0

stepcont=0
	
#initalize VMUI system
vmui.initui(screensurf, KIOSKMODE)

if 'GLOBRUNFLG' in globals():
	
	TROMA=GLOBRUNFLG
	libtrom.redefA(TROMA)
	runtype=0
	LOGBASE=TROMA
	print ("GLOBRUNFLG found... \n running trom: \"" + TROMA + "\" as TROMA")



elif 'GLOBSTREG' in globals():
	streg_subtitle="Unnamed"
	#scstreg=open(GLOBSTREG, 'r')
	ncstreg=libSBTCVM.stregload(GLOBSTREG)
	scstreg=open(ncstreg, 'r')
	exstreg=compile(scstreg.read(), ncstreg, 'exec')
	exec(exstreg)
	scstreg.close()
	print ("streg program title:" + streg_subtitle)
	libtrom.redefA(TROMA)
	libtrom.redefB(TROMA)
	libtrom.redefC(TROMA)
	libtrom.redefD(TROMA)
	libtrom.redefE(TROMA)
	libtrom.redefF(TROMA)
	runtype=1
	LOGBASE=GLOBSTREG
	pygame.display.set_caption("SBTCVM Mark 2 | " + streg_subtitle, "SBTCVM Mark 2 | " + streg_subtitle)
	print ("GLOBSTREG found... \n Starting SBTCVM with setup in streg file: \"" + GLOBSTREG + "\"")
else:
	streg_subtitle="Unnamed"
	#scstreg=open(DEFAULTSTREG, 'r')
	ncstreg=libSBTCVM.stregload(DEFAULTSTREG)
	scstreg=open(ncstreg, 'r')
	exstreg=compile(scstreg.read(), ncstreg, 'exec')
	exec(exstreg)
	print ("streg program title:" + streg_subtitle)
	libtrom.redefA(TROMA)
	libtrom.redefB(TROMA)
	libtrom.redefC(TROMA)
	libtrom.redefD(TROMA)
	libtrom.redefE(TROMA)
	libtrom.redefF(TROMA)
	runtype=1
	LOGBASE=DEFAULTSTREG
	pygame.display.set_caption("SBTCVM Mark 2 | " + streg_subtitle, "SBTCVM Mark 2 | " + streg_subtitle)
	print ("nither GLOBSTREG or GLOBRUNFLG have been found... \nStarting SBTCVM with setup in default streg file: \"" + DEFAULTSTREG + "\"")
if vmexeclogflg==1:
	vmexlogf=open(os.path.join("CAP", libSBTCVM.namecrunch(LOGBASE, "-vmexeclog.log")), "w")

if 'GLOBLOGEXEC' in globals():
	if GLOBLOGEXEC==1:
		vmexeclogflg=1
		vmexlogf=open(os.path.join("CAP", libSBTCVM.namecrunch(LOGBASE, "-vmexeclog.log")), "w")

if 'GLOBOPSEC' in globals():
	if GLOBOPSEC==1:
		trackopsec=1
	else:
		trackopsec=0
else:
	trackopsec=0
		

#tritlength defaults
tritloadlen=9
tritoffset=0
tritdestgnd=0

def tritlen(srcdata, destdata):
	#just return srcdata if tritloadlen=9 and tritoffset=0
	if tritdestgnd==1:
		destdata="000000000"
	if tritloadlen==9 and tritoffset==0:
		#print srcdata
		return (srcdata)
	destdict={}
	destcnt=0
	tritstart=(8 - tritoffset)
	tritstop=(tritstart - tritloadlen)
	#print tritstop
	tritstack=1
	iterlist=[0, 1, 2, 3, 4, 5, 6, 7, 8]
	#parse destination data into a dict
	for f in destdata:
		destdict[destcnt]=f
		destcnt += 1
	#modify destination dict 
	for f in iterlist:
		#print tritstart
		destdict[tritstart]=srcdata[tritstart]
		tritstart -= 1
		tritstack += 1
		if tritstart==tritstop or tritstart==-1:
			break
	#print destdict
	destdataout=""
	#parse destination dict back into string and return result.
	for f in iterlist:
		destdataout=(destdataout + destdict[f])
	#print destdataout
	return destdataout
		
#def stactdebug1():
	

TTYBGCOL=libSBTCVM.colorfind("------")
TTYBGCOLREG="------"


colvectorreg="000000"
monovectorreg="000000"

if stepbystep==1:
	STEPLED=LEDGREENON
else:
	STEPLED=LEDGREENOFF

#keep unused events out of queue
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

libSBTCVMsurf=pygame.Surface((648, 486)).convert()
libSBTCVMsurf.fill(TTYBGCOL)
libSBTCVM.glyphoptim(libSBTCVMsurf)
#RAMBANK startup begin
RAMbank = {}

#calmlst = open("ORDEREDLIST6.txt")
#screensurf.fill((0,127,255))



#build IObus dictionary.
IOgen="---------"
RAMbank["---------"] = "000000000"
while IOgen!="+++++++++":
	IOgen=libSBTCVM.trunkto6(libbaltcalc.btadd(IOgen, "+"))
	RAMbank[IOgen] = "000000000"
RAMbank["+++++++++"] = "000000000"
#set Random integer port with an inital random integer
RAMbank["--0------"]=libSBTCVM.trunkto6(libbaltcalc.DECTOBT(randint(-9841,9841)))

ttyredraw=1

#IO read only list. IO addresses in this list are treated as read only. for example:
#the random integer port is read only.
IOreadonly=["--0------"]

MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
#RAMBANK startup end
colorreg="++++++"
ROMFILE=TROMA
ROMLAMPFLG="A"
stopflag=0
EXECCHANGE=0
#ROMFILE=open(BOOTUPFILE)
mempoint="---------"
EXECADDR="---------"
contaddr="---------"
EXECADDRfall=0
EXECADDRraw=EXECADDR
REG1="000000000"
REG2="000000000"
#status display optimization.
prevREG1="diff"
prevREG2="diff"
prevEXECADDR="diff"
prevROM="diff"
prevINST="diff"
prevDATA="diff"
regsetpoint="000000000"
updtcdisp=1
updtmdisp=1
updtblits=list()
updtttyprev=list()
updtrandport=1
upt=screensurf.blit(CPULEDACT, (749, 505))
updtblits.extend([upt])
upt=screensurf.blit(STEPLED, (750, 512))
updtblits.extend([upt])
print "Prep threading system..."
threadref="00"
#vmexeclog("Preping threading system...")


BTSTACK={"--": BTTHREAD(1, EXECADDR, REG1, REG2, contaddr, EXECADDRraw, regsetpoint, TTYBGCOLREG, TTYBGCOL, colvectorreg, monovectorreg, colorreg, tritloadlen, tritoffset, tritdestgnd, threadref, ROMFILE, ROMLAMPFLG, mempoint)}
for cur_id in ["-0","-+","0-","00","0+","+-","+0","++"]:
    BTSTACK[cur_id] = BTTHREAD(0, EXECADDR, REG1, REG2, contaddr, EXECADDRraw, regsetpoint, TTYBGCOLREG, TTYBGCOL, colvectorreg, monovectorreg, colorreg, tritloadlen, tritoffset, tritdestgnd, threadref, ROMFILE, ROMLAMPFLG, mempoint)

btthreadcnt=1
btcurthread="--"

curthrtex=lgdispfont.render(btcurthread, True, (127, 0, 255), (0, 0, 0)).convert()
upt=screensurf.blit(curthrtex, (170, 522))
updtblits.extend([upt])

exlogclockticnum=0

#for f in BTSTACK:
#	print str(BTSTACK[f].qxtact) + " " + f
#for f in BTSTACK:
#	print str(BTSTACK[f].qxtact) + " " + f	
print "SBTCVM Mark 2 Ready. the VM will now begin."
#vmexeclog("SBTCVM Mark 2 Ready. the VM will now begin.")
initaltime=time.time()

while stopflag==0:
	#curinst=(libtrom.tromreadinst(EXECADDR,ROMFILE))
	#curdata=(libtrom.tromreaddata(EXECADDR,ROMFILE))
	EXECADDRNUM=libSBTCVM.numstruct(EXECADDR)
	#fdelta=libtrom.ROMDICT[ROMFILE][EXECADDRNUM]
	if ROMFILE==TROMA:
		fdelta=libtrom.AROM[EXECADDRNUM]
	elif ROMFILE==TROMB:
		fdelta=libtrom.BROM[EXECADDRNUM]
	elif ROMFILE==TROMC:
		fdelta=libtrom.CROM[EXECADDRNUM]
	elif ROMFILE==TROMD:
		fdelta=libtrom.DROM[EXECADDRNUM]
	elif ROMFILE==TROME:
		fdelta=libtrom.EROM[EXECADDRNUM]
	elif ROMFILE==TROMF:
		fdelta=libtrom.FROM[EXECADDRNUM]
	curinst=((fdelta[0]) + (fdelta[1]) + (fdelta[2]) + (fdelta[3]) + (fdelta[4]) + (fdelta[5]))
	curdata=((fdelta[6]) + (fdelta[7]) + (fdelta[8]) + (fdelta[9]) + (fdelta[10]) + (fdelta[11]) + (fdelta[12]) + (fdelta[13]) + (fdelta[14]))
	#some screen display stuff & general blitting
	#screensurf.fill((0,127,255))
	#draw Background
	if trackopsec==1:
		exlogclockticnum += 1
		exlogcurtime=(time.time() - initaltime)
	elif vmexeclogflg==1:
		exlogclockticnum += 1
		exlogcurtime=(time.time() - initaltime)
		vmexeclog("data: " + curdata + " |Inst: " + curinst + " |adr: " + EXECADDR + " |thread: " + btcurthread + " |exec bank: " + ROMLAMPFLG + " |reg1: " + REG1 + " |reg2: " + REG2 + " |tic #: " + str(exlogclockticnum) + " |secs: " + format((exlogcurtime), '.11f'))
	if fskipcnt == fskip or stepbystep==1:
		if disablereadouts==0 or stepbystep==1:
			#screensurf.blit(vmbg, (0, 0))
			#these show the instruction and data in the instruction/data box :)
			if prevINST!=curinst:
				insttext=smldispfont.render(curinst, True, (0, 255, 255), (0, 0, 0)).convert()
				prevINST=curinst
				upt=screensurf.blit(insttext, (8, 522))
				updtblits.extend([upt])
			if prevDATA!=curdata:
				datatext=smldispfont.render(curdata, True, (0, 255, 127), (0, 0, 0)).convert()
				prevDATA=curdata
				upt=screensurf.blit(datatext, (8, 566))
				updtblits.extend([upt])
			
			#these draw the register displays :)
			if prevREG1!=REG1:
				reg1text=lgdispfont.render(REG1, True, (255, 0, 127), (0, 0, 0)).convert()
				prevREG1=REG1
				upt=screensurf.blit(reg1text, (219, 521))
				updtblits.extend([upt])
			if prevREG2!=REG2:
				reg2text=lgdispfont.render(REG2, True, (255, 127, 0), (0, 0, 0)).convert()
				prevREG2=REG2
				upt=screensurf.blit(reg2text, (219, 564))
				updtblits.extend([upt])
			
			
			#and here is what draws the ROM address display :)
			ROMadrtex=lgdispfont.render(EXECADDR, True, (0, 127, 255), (0, 0, 0)).convert()
			upt=screensurf.blit(ROMadrtex, (425, 564))
			updtblits.extend([upt])
			#and the current rom display :)
			CURROMTEXT=(ROMLAMPFLG)
			if prevROM!=CURROMTEXT:
				curROMtex=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0)).convert()
				prevROM=CURROMTEXT
				upt=screensurf.blit(curROMtex, (126, 522))
				updtblits.extend([upt])
		#LED LAMPS
		#CPU
		#screensurf.blit(CPULEDACT, (749, 505))
		#STEP
		
		if updtcdisp==1:
			updtcdisp=0
			COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
			upt=screensurf.blit(COLORDISPBIG, (649, 1))
			updtblits.extend([upt])
		if updtmdisp==1:
			updtmdisp=0
			MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
			upt=screensurf.blit(MONODISPBIG, (649, 150))
			updtblits.extend([upt])
		if abtpref!=abt or ttyredraw==1:
			abtpref=abt
			ttyredraw=0
			lineq=0
			linexq=0
			if ttystyle==0:
				libSBTCVMsurf.fill(TTYBGCOL)
				for fnx in abt:
					fnx=fnx.replace('\n', '')
					colq=0
					if TTYSIZE==0 or linexq>26:
						for qlin in fnx:
							#print qlin
							charq=libSBTCVM.charlookupdict.get(qlin)
							#print charq
							if TTYSIZE==1:
								libSBTCVM.charblit2(libSBTCVMsurf, colq, lineq, charq)
							else:
								libSBTCVM.charblit(libSBTCVMsurf, colq, lineq, charq)
							colq +=1
						lineq +=1
					linexq +=1		
				upt=screensurf.blit(libSBTCVMsurf, (0, 0))
				updtblits.extend([upt])
			lineq=0
			linexq=0
			#if ttystyle==1:
				#print "-----newpage---"
				#for fnx in abt:
					#if TTYSIZE==0 or linexq>26:
						#fnx=fnx.replace('\n', '')
						#colq=0
						#print ("TTY|" + fnx)
						#lineq +=1
					#linexq +=1
			lineq=0
			linexq=0
			#disabled as its far too buggy
			#if ttystyle==2:
				#for fnx in abt:
					#fnx=fnx.replace('\n', '')
					#colq=0
					#if TTYSIZE==0 or linexq>26:
						#if TTYSIZE==1:
							#ttyfn=ttyfontB.render(fnx, True, (255, 255, 255), (0, 0, 0)).convert()
							#upt=screensurf.blit(ttyfn, (0, (lineq*18)))
							##updtblits.extend([upt])
						#else:
							#ttyfn=ttyfont.render(fnx, True, (255, 255, 255), (0, 0, 0)).convert()
							#upt=screensurf.blit(ttyfn, (0, (lineq*9)))
							##updtblits.extend([upt])
						#lineq +=1
					#linexq +=1
			
				
			#print ("ttystyle" + str(ttystyle))
			#screensurf.blit(libSBTCVMsurf, (45, 40))
			#biglibSBTCVM=pygame.transform.scale(libSBTCVMsurf, (648, 486))
		if updtblits!=list():
			pygame.display.update(updtblits)
			updtblits=list()
		fskipcnt=0
		#print "sc update"
	else:
		fskipcnt+=1
		#print "sc skip"
	#ROM READ (first register)
	if curinst=="------":
		REG1=(tritlen(libtrom.tromreaddata(curdata,ROMFILE), REG1))
		#print("----")
	#ROM READ (second register)
	elif curinst=="-----0":
		REG2=(tritlen(libtrom.tromreaddata(curdata,ROMFILE), REG2))
		#print("---0")
	#IO READ REG1
	elif curinst=="-----+":
		REG1=tritlen(RAMbank[curdata], REG1)
		if curdata=="--0------":
			updtrandport=1
		#print("---+")
	#IO READ REG2
	elif curinst=="----0-":
		REG2=tritlen(RAMbank[curdata], REG2)
		if curdata=="--0------":
			updtrandport=1
		#print("--0-")
	#IO WRITE REG1
	elif curinst=="----00":
		if curdata not in IOreadonly:
			rambnkcur=RAMbank[curdata]
			RAMbank[curdata] = tritlen(REG1, rambnkcur)
		else:
			print "address \"" + curdata + "\" is read-only."
	#IO WRITE REG2
	elif curinst=="----0+":
		if curdata not in IOreadonly:
			rambnkcur=RAMbank[curdata]
			RAMbank[curdata] = tritlen(REG2, rambnkcur)
		else:
			print "address \"" + curdata + "\" is read-only."
	#swap primary Registers
	elif curinst=="----+-":
		REGTEMP = REG1
		REG1 = REG2
		REG2 = REGTEMP 
	#copy Register 1 to register 2
	elif curinst=="----+0":
		REG2 = REG1
	#copy Register 2 to register 1
	elif curinst=="----++":
		REG1 = REG2
	#invert register 1
	elif curinst=="---0--":
		REG1 = (libbaltcalc.BTINVERT(REG1))
	#invert register 2
	elif curinst=="---0-0":
		REG2 = (libbaltcalc.BTINVERT(REG2))
	#add both registers, load awnser into REG1
	elif curinst=="---0-+":
		#print REG1
		#print REG2
		#print "bla"
		REG1 = (libSBTCVM.trunkto6math(libbaltcalc.btadd(REG1, REG2)))
	#sub both registers, load awnser into REG1
	elif curinst=="---00-":
		REG1 = (libSBTCVM.trunkto6math(libbaltcalc.btsub(REG1, REG2)))
	#mul both registers, load awnser into REG1
	elif curinst=="---000":
		REG1 = (libSBTCVM.trunkto6math(libbaltcalc.btmul(REG1, REG2)))
	#div both registers, load awnser into REG1
	elif curinst=="---00+":
		ZDIVCHECKTMP=libbaltcalc.btdivcpu(REG1, REG2)
		if ZDIVCHECKTMP=="ZDIV":
			stopflag=1
			abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
			abt=libSBTCVM.abtslackline(abt, "DIVIDE BY ZERO")
			vmexeclog("VMSYSHALT: DIVIDE BY ZERO")
			REG1=="000000000"
		else:
			REG1 = (libSBTCVM.trunkto6math(ZDIVCHECKTMP))
		
	#set REG1
	elif curinst=="---0+-":
		REG1 = curdata
	#set REG2
	elif curinst=="---0+0":
		REG2 = curdata
	#set inst
	elif curinst=="---0++":
		instsetto=(REG1[0] + REG1[1] + REG1[2] + REG1[3] + REG1[4] + REG1[5])
		libtrom.tromsetinst(curdata, instsetto, ROMFILE)
	#set data
	elif curinst=="---+--":
		libtrom.tromsetdata(curdata, tritlen(REG1, libtrom.tromreaddata(curdata, ROMFILE)), ROMFILE)
	#continue
	elif curinst=="---+++":
		EXECADDRNEXT=contaddr
		EXECCHANGE=1
	#color draw
	elif curinst=="--0---":
		updtcdisp=1
		jx=libSBTCVM.drawnumstruct3((curdata[3] + curdata[4] + curdata[5]))
		jy=libSBTCVM.drawnumstruct3((curdata[6] + curdata[7] + curdata[8]))
		RGBcol=libSBTCVM.colorfind(colorreg)
		#print monocol
		pygame.draw.line(COLORDISP, RGBcol, [jx, jy], [jx, jy], 1)
		#COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
	#set PPU color Register
		
	elif curinst=="--0--0":
		updtcdisp=1
		colorreg=(curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8])
	elif curinst=="--0--+":
		updtcdisp=1
		RGBcol=libSBTCVM.colorfind((curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8]))
		#print monocol
		COLORDISP.fill(RGBcol)
		#COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
	#set PPU color vector Register
		
	elif curinst=="--0-0-":
		updtcdisp=1
		colvectorreg=(curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8])
	elif curinst=="--0-00":
		updtcdisp=1
		#print curdata
		jx=libSBTCVM.drawnumstruct3((curdata[3] + curdata[4] + curdata[5]))
		jy=libSBTCVM.drawnumstruct3((curdata[6] + curdata[7] + curdata[8]))
		kx=libSBTCVM.drawnumstruct3((colvectorreg[0] + colvectorreg[1] + colvectorreg[2]))
		ky=libSBTCVM.drawnumstruct3((colvectorreg[3] + colvectorreg[4] + colvectorreg[5]))
		RGBcol=libSBTCVM.colorfind(colorreg)
		#print monocol
		pygame.draw.line(COLORDISP, RGBcol, [jx, jy], [kx, ky], 1)
		#COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
	#color draw rect
	elif curinst=="--0-0+":
		updtcdisp=1
		#print curdata
		jx=libSBTCVM.drawnumstruct3((curdata[3] + curdata[4] + curdata[5]))
		jy=libSBTCVM.drawnumstruct3((curdata[6] + curdata[7] + curdata[8]))
		kx=libSBTCVM.drawnumstruct3((colvectorreg[0] + colvectorreg[1] + colvectorreg[2]))
		ky=libSBTCVM.drawnumstruct3((colvectorreg[3] + colvectorreg[4] + colvectorreg[5]))
		RGBcol=libSBTCVM.colorfind(colorreg)
		#print monocol
		#pygame.draw.line(COLORDISP, RGBcol, [jx, jy], [kx, ky], 1)
		COLORDISP.fill(RGBcol, (libSBTCVM.makerectbipoint(jx, jy, kx, ky)))
		#COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
	
	#mono draw
	#mono draw pixel
	elif curinst=="--0-+-":
		updtmdisp=1
		jx=libSBTCVM.drawnumstruct2((curdata[3] + curdata[4]))
		jy=libSBTCVM.drawnumstruct2((curdata[5] + curdata[6]))
		monocol=(int(libSBTCVM.dollytell((curdata[7] + curdata[8]))))
		#print monocol
		pygame.draw.line(MONODISP, (monocol, monocol, monocol), [jx, jy], [jx, jy], 1)
		#MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
	#mono fill
	elif curinst=="--0-+0":
		updtmdisp=1
		monocol=(int(libSBTCVM.dollytell((curdata[7] + curdata[8]))))
		#print monocol
		MONODISP.fill((monocol, monocol, monocol))
		#MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
	#set PPU mono vector Register
	elif curinst=="--0-++":
		updtmdisp=1
		monovectorreg=(curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8])
	#draw mono line
	elif curinst=="--00--":
		updtmdisp=1
		jx=libSBTCVM.drawnumstruct2((curdata[3] + curdata[4]))
		jy=libSBTCVM.drawnumstruct2((curdata[5] + curdata[6]))
		kx=libSBTCVM.drawnumstruct2((monovectorreg[0] + monovectorreg[1]))
		ky=libSBTCVM.drawnumstruct2((monovectorreg[2] + monovectorreg[3]))
		monocol=(int(libSBTCVM.dollytell((curdata[7] + curdata[8]))))
		#print monocol
		pygame.draw.line(MONODISP, (monocol, monocol, monocol), [jx, jy], [kx, ky], 1)
		#MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
	#mono draw rect
	elif curinst=="--00-0":
		updtmdisp=1
		jx=libSBTCVM.drawnumstruct2((curdata[3] + curdata[4]))
		jy=libSBTCVM.drawnumstruct2((curdata[5] + curdata[6]))
		kx=libSBTCVM.drawnumstruct2((monovectorreg[0] + monovectorreg[1]))
		ky=libSBTCVM.drawnumstruct2((monovectorreg[2] + monovectorreg[3]))
		monocol=(int(libSBTCVM.dollytell((curdata[7] + curdata[8]))))
		#print monocol
		#pygame.draw.line(MONODISP, (monocol, monocol, monocol), [jx, jy], [kx, ky], 1)
		MONODISP.fill((monocol, monocol, monocol), (libSBTCVM.makerectbipoint(jx, jy, kx, ky)))
		#MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
	#SHUTDOWN VM
	elif curinst=="--000-":
		stopflag=1
		abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
		abt=libSBTCVM.abtslackline(abt, "soft stop.")
		vmexeclog("VMSYSHALT: SOFT STOP")
		ttyredraw=1
	#NULL INSTRUCTION (DOES NOTHING) USE WHEN YOU WISH TO DO NOTHING :p
	#elif curinst=="--0000":
		#commented out due to doing nothing.
		#print("")
	#goto rom adress specified by CURRENT DATA
	elif curinst=="--000+":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
	#goto rom adress specified by Register 1
	elif curinst=="--00+-":
		EXECADDRNEXT=REG1
		EXECCHANGE=1
	
	elif curinst=="--00+0":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
	elif curinst=="--00++":
		waitchop=curdata[5]
		if waitchop=="+":
			waitmagn=0.3
		elif waitchop=="-":
			waitmagn=0.1
		else:
			waitmagn=0.2
		time.sleep(( waitmagn))
	#asks user if goto to adress is desired
	elif curinst=="--0+--":
		abt=libSBTCVM.abtslackline(abt, ("GOTO: (" + curdata + ") Y or N?"))
		ttyredraw=1
		USRYN=1
		extradraw=1	
	#user wait
	elif curinst=="--0+-0":
		abt=libSBTCVM.abtslackline(abt, ("Press enter to continue."))
		ttyredraw=1
		USRWAIT=1
		extradraw=1	
	#TTY clear
	elif curinst=="--0+-+":
		abt=["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
	#Goto data if Reg 1 greater
	elif curinst=="--0+0-":
		if libbaltcalc.BTTODEC(REG1)>libbaltcalc.BTTODEC(REG2):
			EXECADDRNEXT=curdata
			EXECCHANGE=1
	
	
	#note these swap TROMS
	#TROMA: goto rom adress on TROMA specified by CURRENT DATA
	elif curinst=="--+---":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMA
		ROMLAMPFLG="A"
	#conditional GOTO
	elif curinst=="--+--0":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMA
			ROMLAMPFLG="A"
	#TROMB: goto rom adress on TROMB specified by CURRENT DATA
	elif curinst=="--+--+":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMB
		ROMLAMPFLG="B"
	elif curinst=="--+-0-":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMB
			ROMLAMPFLG="B"
	#TROMC: goto rom adress on TROMC specified by CURRENT DATA
	elif curinst=="--+-00":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMC
		ROMLAMPFLG="C"
	#conditional GOTO
	elif curinst=="--+-0+":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMC
			ROMLAMPFLG="C"
	#TROMD: goto rom adress on TROMD specified by CURRENT DATA
	elif curinst=="--+-+-":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMD
		ROMLAMPFLG="D"
	#conditional GOTO
	elif curinst=="--+-+0":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMD
			ROMLAMPFLG="D"
	#TROME: goto rom adress on TROME specified by CURRENT DATA
	elif curinst=="--+-++":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROME
		ROMLAMPFLG="E"
	#conditional GOTO
	elif curinst=="--+0--":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROME
			ROMLAMPFLG="E"
	#TROMF: goto rom adress on TROMF specified by CURRENT DATA
	elif curinst=="--+0-0":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMF
		ROMLAMPFLG="F"
	#conditional GOTO
	elif curinst=="--+0-+":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMF
			ROMLAMPFLG="F"
	
	
	#dump register 1 to TTY
	elif curinst=="--++0+":
		#print ("REG1 DUMP:" + REG1 + " " + str(libbaltcalc.BTTODEC(REG1)))
		ttyredraw=1
		abt=libSBTCVM.abtslackline(abt, ("REG1 DUMP:" + REG1 + " " + str(libbaltcalc.BTTODEC(REG1))))
	#dump Register 2 to TTY
	elif curinst=="--+++-":
		#print ("REG2 DUMP:" + REG2 + " " + str(libbaltcalc.BTTODEC(REG2)))
		ttyredraw=1
		abt=libSBTCVM.abtslackline(abt, ("REG2 DUMP:" + REG2 + " " + str(libbaltcalc.BTTODEC(REG2))))
	#tty write port (direct)
	elif curinst=="--+++0":
		abt=libSBTCVM.abtcharblit(abt, (libSBTCVM.charcodelook((curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8]))))
		if TTYrenderflg=="0":
			ttyredraw=1
		else:
			if libSBTCVM.getnewlstate()==1:
				ttyredraw=1
			
	#Buzzer (direct)
	elif curinst=="--++++":
		snf.stop()
		#print "derp"
		wavsp=libSBTCVM.mk1buzz((curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8]))
		snf=pygame.mixer.Sound(wavsp)
		snf.play()
		timechop=curdata[0]
		if timechop=="+":
			time.sleep(0.3)
		elif timechop=="-":
			time.sleep(0.1)
		else:
			time.sleep(0.2)
	#set regset pointer
	elif curinst=="-0-000":
		regsetpoint=curdata
		#print "testtest"
		#print regsetpoint
	#regset
	elif curinst=="-0-00+":
		#print "Test0"
		if regsetpoint=='---------':
			TTYBGCOLREG=(curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8])
			TTYBGCOL=libSBTCVM.colorfind(TTYBGCOLREG)
			ttyredraw=1
			#print "test2"
		elif regsetpoint=='--------0':
			TTYrenderflg=curdata[8]
			if TTYrenderflg=="-":
				TTYrenderflg="0"
		elif regsetpoint=='--------+':
			TTYSIZEFLG=curdata[8]
			ttyredraw=1
			#print "test1"
			if TTYSIZEFLG=="+":
				TTYSIZE=1
			else:
				TTYSIZE=0
	#mempointer control
	elif curinst=="-0-0+-":
		#print mempoint
		mode=(curdata[0] + curdata[1])
		if mode=="--":
			mempoint=libbaltcalc.btadd(mempoint, "+")
		elif mode=="-0":
			mempoint=libbaltcalc.btadd(mempoint, "-")
		elif mode=="-+":
			mempoint=REG1
		elif mode=="00":
			REG1=mempoint
		else:
			mempoint=libbaltcalc.btadd(mempoint, REG1)
		if len(mempoint) > 9:
			stopflag=1
			abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
			abt=libSBTCVM.abtslackline(abt, "MEMORY POINTER OVERFLOW!")
			vmexeclog("VMSYSHALT: MEMORY POINTER OVERFLOW!")
			
		#print mempoint
		#print 'memctl'
	elif curinst=="-0-0+0":
		REG1=(tritlen(libtrom.tromreaddata(mempoint,ROMFILE), REG1))
		#print mempoint
	elif curinst=="-0-0++":	
		libtrom.tromsetdata(mempoint, tritlen(REG1, libtrom.tromreaddata(mempoint, ROMFILE)), ROMFILE)
		#print mempoint
	elif curinst=="-0-+--":	
		libtrom.tromsetdata(mempoint, tritlen(curdata, libtrom.tromreaddata(mempoint, ROMFILE)), ROMFILE)
		#print mempoint
	#offset length
	elif curinst=="-0-++0":
		offlen1=(curdata[7] + curdata[8])
		offlen2=(curdata[5] + curdata[6])
		offlen3=(curdata[4])
		if offlen3=="+":
			tritdestgnd=1
		else:
			tritdestgnd=0
		if offlen2=="--":
			tritoffset=0
		elif offlen2=="-0":
			tritoffset=1
		elif offlen2=="-+":
			tritoffset=2
		elif offlen2=="0-":
			tritoffset=3
		elif offlen2=="00":
			tritoffset=4
		elif offlen2=="0+":
			tritoffset=5
		elif offlen2=="+-":
			tritoffset=6
		elif offlen2=="+0":
			tritoffset=7
		elif offlen2=="++":
			tritoffset=8
		
		if offlen1=="--":
			tritloadlen=1
		elif offlen1=="-0":
			tritloadlen=2
		elif offlen1=="-+":
			tritloadlen=3
		elif offlen1=="0-":
			tritloadlen=4
		elif offlen1=="00":
			tritloadlen=5
		elif offlen1=="0+":
			tritloadlen=6
		elif offlen1=="+-":
			tritloadlen=7
		elif offlen1=="+0":
			tritloadlen=8
		elif offlen1=="++":
			tritloadlen=9
	
	#THREADING RELATED INSTRUCTIONS
	#thread refrence register
	elif curinst=="--+00-":
		threadref=(curdata[7] + curdata[8])
		#for threaddex in BTSTACK:
			#print (str(BTSTACK[threaddex].qxtact) + " threadrefregset " + threaddex)
	#start thread
	elif curinst=="--+000":
		#for threaddex in BTSTACK:
		#		print (str(BTSTACK[threaddex].qxtact) + " pre r " + threaddex)
		if threadref==btcurthread or BTSTACK[threadref].qxtact==1:
			stopflag=1
			abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
			abt=libSBTCVM.abtslackline(abt, "THREAD COLLISION!")
			vmexeclog("VMSYSHALT: THREAD COLLISION!")
			#for threaddex in BTSTACK:
			#	print (str(BTSTACK[threaddex].qxtact) + " rerror " + threaddex)
		elif BTSTACK[threadref].qxtact==0:
			#BTSTACK[threadref]=otherthreadinital
			qxp=BTTHREAD(0, EXECADDR, REG1, REG2, contaddr, EXECADDRraw, regsetpoint, TTYBGCOLREG, TTYBGCOL, colvectorreg, monovectorreg, colorreg, tritloadlen, tritoffset, tritdestgnd, threadref, ROMFILE, ROMLAMPFLG, "---------")
			#for threaddex in BTSTACK:
			#	print (str(BTSTACK[threaddex].qxtact) + " pre thread launch r " + threaddex)
			qxp.qxtact=1
			#for threaddex in BTSTACK:
			#	print (str(BTSTACK[threaddex].qxtact) + " post qxtact r " + threaddex)
			qxp.EXECADDR=curdata
			qxp.EXECADDRraw=curdata
			
			BTSTACK[threadref]=qxp
			btthreadcnt += 1
			#for threaddex in BTSTACK:
			#	print (str(BTSTACK[threaddex].qxtact) + " r " + threaddex)
	#stop current thread
	elif curinst=="--+00+":
		btstopthread=1
	#stop thread refrenced in threadref	
	elif curinst=="--+0+-":
		if btcurthread==threadref:
			btstopthread=1
		else:
			BTSTACK[threadref].qxtact=0
			btthreadcnt -= 1
	
	#END OF THREADING RELATED INSTRUCTIONS
	
	#set ketinterupt register
	elif curinst=="-0-+++":
		keyintreg=(curdata[5] + curdata[6] + curdata[7] + curdata[8])
	#keyinterupt activate
	elif curinst=="-00---":
		if keyintreg=="----":
			key1=1
			key1adr=curdata
		if keyintreg=="---0":
			key2=1
			key2adr=curdata
		if keyintreg=="---+":
			key3=1
			key3adr=curdata
		if keyintreg=="--0-":
			key4=1
			key4adr=curdata
		if keyintreg=="--00":
			key5=1
			key5adr=curdata
		if keyintreg=="--0+":
			key6=1
			key6adr=curdata
		if keyintreg=="--+-":
			key7=1
			key7adr=curdata
		if keyintreg=="--+0":
			key8=1
			key8adr=curdata
		if keyintreg=="--++":
			key9=1
			key9adr=curdata
		if keyintreg=="-0--":
			key0=1
			key0adr=curdata
		if keyintreg=="-0-0":
			keyhyp=1
			keyhypadr=curdata
		if keyintreg=="-0-+":
			keypos=1
			keyposadr=curdata
		if keyintreg=="-00-":
			keya=1
			keyaadr=curdata
		if keyintreg=="-000":
			keyb=1
			keybadr=curdata
		if keyintreg=="-00+":
			keyc=1
			keycadr=curdata
		if keyintreg=="-0+-":
			keyd=1
			keydadr=curdata
		if keyintreg=="-0+0":
			keye=1
			keyeadr=curdata
		if keyintreg=="-0++":
			keyf=1
			keyfadr=curdata
		if keyintreg=="-+--":
			keyg=1
			keygadr=curdata
		if keyintreg=="-+-0":
			keyh=1
			keyhadr=curdata
		if keyintreg=="-+-+":
			keyi=1
			keyiadr=curdata
		if keyintreg=="-+0-":
			keyj=1
			keyjadr=curdata
		if keyintreg=="-+00":
			keyk=1
			keykadr=curdata
		if keyintreg=="-+0+":
			keyl=1
			keyladr=curdata
		if keyintreg=="-++-":
			keym=1
			keymadr=curdata
		if keyintreg=="-++0":
			keyn=1
			keynadr=curdata
		if keyintreg=="-+++":
			keyo=1
			keyoadr=curdata
		if keyintreg=="0---":
			keyp=1
			keypadr=curdata
		if keyintreg=="0--0":
			keyq=1
			keyqadr=curdata
		if keyintreg=="0--+":
			keyr=1
			keyradr=curdata
		if keyintreg=="0-0-":
			keysx=1
			keysadr=curdata
		if keyintreg=="0-00":
			keyt=1
			keytadr=curdata
		if keyintreg=="0-0+":
			keyu=1
			keyuadr=curdata
		if keyintreg=="0-+-":
			keyv=1
			keyvadr=curdata
		if keyintreg=="0-+0":
			keyw=1
			keywadr=curdata
		if keyintreg=="0-++":
			keyx=1
			keyxadr=curdata
		if keyintreg=="00--":
			keyy=1
			keyyadr=curdata
		if keyintreg=="00-0":
			keyz=1
			keyzadr=curdata
		if keyintreg=="00-+":
			keyspace=1
			keyspaceadr=curdata
		if keyintreg=="000-":
			keyret=1
			keyretadr=curdata
		
		
		
		
	#clear keyinterupt
	elif curinst=="-00--0":
		if curdata[8]=="+":
			key1=0
			key2=0
			key3=0
			key4=0
			key5=0
			key6=0
			key7=0
			key8=0
			key9=0
			key0=0
			keypos=0
			keyhyp=0
			keyq=0
			keyw=0
			keye=0
			keyr=0
			keyt=0
			keyy=0
			keyu=0
			keyi=0
			keyo=0
			keyp=0
			keya=0
			keysx=0
			keyd=0
			keyf=0
			keyg=0
			keyh=0
			keyj=0
			keyk=0
			keyl=0
			keyz=0
			keyx=0
			keyc=0
			keyv=0
			keyb=0
			keyn=0
			keym=0
			keyspace=0
			keyret=0
		else:
			if keyintreg=="----":
				key1=0
			if keyintreg=="---0":
				key2=0
			if keyintreg=="---+":
				key3=0
			if keyintreg=="--0-":
				key4=0
			if keyintreg=="--00":
				key5=0
			if keyintreg=="--0+":
				key6=0
			if keyintreg=="--+-":
				key7=0
			if keyintreg=="--+0":
				key8=0
			if keyintreg=="--++":
				key9=0
			if keyintreg=="-0--":
				key0=0
			if keyintreg=="-0-0":
				keyhyp=0
			if keyintreg=="-0-+":
				keypos=0
			if keyintreg=="-00-":
				keya=0
			if keyintreg=="-000":
				keyb=0
			if keyintreg=="-00+":
				keyc=0
			if keyintreg=="-0+-":
				keyd=0
			if keyintreg=="-0+0":
				keye=0
			if keyintreg=="-0++":
				keyf=0
			if keyintreg=="-+--":
				keyg=0
			if keyintreg=="-+-0":
				keyh=0
			if keyintreg=="-+-+":
				keyi=0
			if keyintreg=="-+0-":
				keyj=0
			if keyintreg=="-+00":
				keyk=0
			if keyintreg=="-+0+":
				keyl=0
			if keyintreg=="-++-":
				keym=0
			if keyintreg=="-++0":
				keyn=0
			if keyintreg=="-+++":
				keyo=0
			if keyintreg=="0---":
				keyp=0
			if keyintreg=="0--0":
				keyq=0
			if keyintreg=="0--+":
				keyr=0
			if keyintreg=="0-0-":
				keysx=0
			if keyintreg=="0-00":
				keyt=0
			if keyintreg=="0-0+":
				keyu=0
			if keyintreg=="0-+-":
				keyv=0
			if keyintreg=="0-+0":
				keyw=0
			if keyintreg=="0-++":
				keyx=0
			if keyintreg=="00--":
				keyy=0
			if keyintreg=="00-0":
				keyz=0
			if keyintreg=="00-+":
				keyspace=0
			if keyintreg=="000-":
				keyret=0
		
		
	#NULL INSTRUCTION (new variant) (compilers should use this in place of the legacy code.)
	#elif curinst=="000000":
	#	
	#	print("")
	if updtrandport==1:
		updtrandport=0
		RAMbank["--0------"]=libSBTCVM.trunkto6(libbaltcalc.DECTOBT(randint(-9841,9841)))
	
	
	
	#needed by user quering opcodes such as 0+--	
	if extradraw==1:
		#screensurf.blit(vmbg, (0, 0))
		#these show the instruction and data in the instruction/data box :)
		insttext=smldispfont.render(curinst, True, (0, 255, 255), (0, 0, 0))
		datatext=smldispfont.render(curdata, True, (0, 255, 127), (0, 0, 0))
		screensurf.blit(insttext, (8, 522))
		screensurf.blit(datatext, (8, 566))
		#these draw the register displays :)
		reg1text=lgdispfont.render(REG1, True, (255, 0, 127), (0, 0, 0))
		reg2text=lgdispfont.render(REG2, True, (255, 127, 0), (0, 0, 0))
		screensurf.blit(reg1text, (219, 521))
		screensurf.blit(reg2text, (219, 564))
		#and here is what draws the ROM address display :)
		ROMadrtex=lgdispfont.render(EXECADDR, True, (0, 127, 255), (0, 0, 0))
		screensurf.blit(ROMadrtex, (425, 564))
		#and the current rom display :)
		CURROMTEXT=(ROMLAMPFLG)
		curROMtex=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0))
		screensurf.blit(curROMtex, (126, 522))
		#LED LAMPS
		#CPU
		screensurf.blit(CPULEDACT, (749, 505))
		#STEP
		screensurf.blit(STEPLED, (750, 512))
		screensurf.blit(COLORDISPBIG, (649, 1))
		screensurf.blit(MONODISPBIG, (649, 150))
		#TTY drawer :)
		#abtpref=abt
		#ttyredraw=0
		lineq=0
		linexq=0
		if ttystyle==0:
			libSBTCVMsurf.fill(TTYBGCOL)
			for fnx in abt:
				fnx=fnx.replace('\n', '')
				colq=0
				if TTYSIZE==0 or linexq>26:
					for qlin in fnx:
						#print qlin
						charq=libSBTCVM.charlookupdict.get(qlin)
						#print charq
						if TTYSIZE==1:
							libSBTCVM.charblit2(libSBTCVMsurf, colq, lineq, charq)
						else:
							libSBTCVM.charblit(libSBTCVMsurf, colq, lineq, charq)
						colq +=1
					lineq +=1
				linexq +=1
			upt=screensurf.blit(libSBTCVMsurf, (0, 0))
			updtblits.extend([upt])
		lineq=0
		linexq=0
		#if ttystyle==1:
			#print (chr(27) + "[2J" + chr(27) + "[H")
			#for fnx in abt:
				#fnx=fnx.replace('\n', '')
				#colq=0
				#print ("TTY|" + fnx)
				#lineq +=1
				#linexq +=1
		#lineq=0
		#linexq=0
		#disabled as its too buggy
		#if ttystyle==2:
			#for fnx in abt:
				#fnx=fnx.replace('\n', '')
				#colq=0
				#if TTYSIZE==0 or linexq>26:
					#if TTYSIZE==1:
						#ttyfn=ttyfontB.render(fnx, True, (255, 255, 255), (0, 0, 0)).convert()
						#upt=screensurf.blit(ttyfn, (0, (lineq*18)))
						##updtblits.extend([upt])
					#else:
						#ttyfn=ttyfont.render(fnx, True, (255, 255, 255), (0, 0, 0)).convert()
						#upt=screensurf.blit(ttyfn, (0, (lineq*9)))
						##updtblits.extend([upt])
					#lineq +=1
				#linexq +=1
		
			
		#print ("ttystyle" + str(ttystyle))
		#screensurf.blit(libSBTCVMsurf, (45, 40))
		#biglibSBTCVM=pygame.transform.scale(libSBTCVMsurf, (648, 486))
			
		pygame.display.update()
		#abt=libSBTCVM.abtslackline(abt, jline)
		extradraw=0
	if USRWAIT==1:
		evhappenflg2=0
		while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_RETURN:
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					pmenret=vmui.pausemenu()
					if pmenret=="s":
						stopflag=1
						abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
						abt=libSBTCVM.abtslackline(abt, "User stop.")
						vmexeclog("VMSYSHALT: USER STOP")
						evhappenflg2=1
						break
					else:
						break
				if event.type == KEYDOWN and event.key == K_F7:
					pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
					pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F2:
					stepbystep=1
					STEPLED=LEDGREENON
					upt=screensurf.blit(STEPLED, (750, 512))
					updtblits.extend([upt])
					break
				if event.type == KEYDOWN and event.key == K_F10:
					ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
					for IOitm in RAMbank:
						ramdmp.write("A:" + str(IOitm) + " D:" + RAMbank[IOitm] + "\n")
					ramdmp.close()
					
					for threaddex in BTSTACK:
						print (str(BTSTACK[threaddex].qxtact) + " " + threaddex)
					libtrom.manualdumptroms()
					break
				if event.type == KEYDOWN and event.key == K_F4:
					if disablereadouts==1:
						disablereadouts=0
						print "readouts enabled"
					elif disablereadouts==0:
						print "readouts disabled"
						disablereadouts=1
					#STEPLED=LEDGREENON
					break
		abt=libSBTCVM.abtslackline(abt, ("\n"))
		USRWAIT=0
	
	
	if USRYN==1:
		evhappenflg2=0
		while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_y:
					EXECADDRNEXT=curdata
					EXECCHANGE=1
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_n:
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					pmenret=vmui.pausemenu()
					if pmenret=="s":
						stopflag=1
						abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
						abt=libSBTCVM.abtslackline(abt, "User stop.")
						vmexeclog("VMSYSHALT: USER STOP")
						evhappenflg2=1
						break
					else:
						break
				if event.type == KEYDOWN and event.key == K_F7:
					pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
					pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F2:
					stepbystep=1
					STEPLED=LEDGREENON
					upt=screensurf.blit(STEPLED, (750, 512))
					updtblits.extend([upt])
					break
				if event.type == KEYDOWN and event.key == K_F10:
					ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
					for IOitm in RAMbank:
						ramdmp.write("A:" + str(IOitm) + " D:" + RAMbank[IOitm] + "\n")
					ramdmp.close()
					for threaddex in BTSTACK:
						print (str(BTSTACK[threaddex].qxtact) + " " + threaddex)
					libtrom.manualdumptroms()
					break
				if event.type == KEYDOWN and event.key == K_F4:
					if disablereadouts==1:
						disablereadouts=0
						print "readouts enabled"
					elif disablereadouts==0:
						print "readouts disabled"
						disablereadouts=1
					#STEPLED=LEDGREENON
					break
		abt=libSBTCVM.abtslackline(abt, ("\n"))
		USRYN=0
	
	#print(EXECADDR)
	if stepbystep==1:
		#this is used when step-by-step mode is enabled
		evhappenflg2=0
		while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_RETURN:
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_LSHIFT:
					stepcont=1
					evhappenflg2=1
					break
				if event.type == KEYUP and event.key == K_LSHIFT:
					stepcont=0
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					pmenret=vmui.pausemenu()
					if pmenret=="s":
						stopflag=1
						abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
						abt=libSBTCVM.abtslackline(abt, "User stop.")
						vmexeclog("VMSYSHALT: USER STOP")
						evhappenflg2=1
						break
					else:
						break
				if event.type == KEYDOWN and event.key == K_F7:
					pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
					pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F2:
					stepbystep=0
					STEPLED=LEDGREENOFF
					upt=screensurf.blit(STEPLED, (750, 512))
					updtblits.extend([upt])
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_F10:
					ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
					for IOitm in RAMbank:
						ramdmp.write("A:" + str(IOitm) + " D:" + RAMbank[IOitm] + "\n")
					for threaddex in BTSTACK:
						print (str(BTSTACK[threaddex].qxtact) + " " + threaddex)
					ramdmp.close()
					libtrom.manualdumptroms()
					break
			if stepcont==1:
				break
				
		
	else:
		#...otherwise this is used to passivly check for imput
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				pmenret=vmui.pausemenu()
				if pmenret=="s":
					stopflag=1
					abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
					abt=libSBTCVM.abtslackline(abt, "User stop.")
					vmexeclog("VMSYSHALT: USER STOP")
					break
				else:
					break
			if event.type == KEYDOWN and event.key == K_F7:
				pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
				pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
				break
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
				break
			if event.type == KEYDOWN and event.key == K_F10:
				ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
				for IOitm in RAMbank:
					ramdmp.write("A:" + str(IOitm) + " D:" + RAMbank[IOitm] + "\n")
				ramdmp.close()
				for threaddex in BTSTACK:
					print (str(BTSTACK[threaddex].qxtact) + " " + threaddex)
				libtrom.manualdumptroms()
				break
			if event.type == KEYDOWN and event.key == K_F2:
				stepbystep=1
				STEPLED=LEDGREENON
				upt=screensurf.blit(STEPLED, (750, 512))
				updtblits.extend([upt])
				break
			if event.type == KEYDOWN and event.key == K_F4:
				if disablereadouts==1:
					disablereadouts=0
					print "readouts enabled"
				elif disablereadouts==0:
					print "readouts disabled"
					disablereadouts=1
				#STEPLED=LEDGREENON
				break
			if event.type == KEYDOWN and (event.key == K_1 or event.key == K_KP1) and key1 == 1:
				EXECADDRNEXT=key1adr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_2 or event.key == K_KP2) and key2 == 1:
				EXECADDRNEXT=key2adr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_3 or event.key == K_KP3) and key3 == 1:
				EXECADDRNEXT=key3adr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_4 or event.key == K_KP4) and key4 == 1:
				EXECADDRNEXT=key4adr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_5 or event.key == K_KP5) and key5 == 1:
				EXECADDRNEXT=key5adr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_6 or event.key == K_KP6) and key6 == 1:
				EXECADDRNEXT=key6adr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_7 or event.key == K_KP7) and key7 == 1:
				EXECADDRNEXT=key7adr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_8 or event.key == K_KP8) and key8 == 1:
				EXECADDRNEXT=key8adr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_9 or event.key == K_KP9) and key9 == 1:
				EXECADDRNEXT=key9adr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_0 or event.key == K_KP0) and key0 == 1:
				EXECADDRNEXT=key0adr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_MINUS or event.key == K_UNDERSCORE or event.key == K_KP_MINUS) and keyhyp == 1:
				EXECADDRNEXT=keyhypadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_PLUS or event.key == K_EQUALS or event.key == K_KP_PLUS) and keypos == 1:
				EXECADDRNEXT=keyposadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_a and keya == 1:
				EXECADDRNEXT=keyaadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_b and keyb == 1:
				EXECADDRNEXT=keybadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_c and keyc == 1:
				EXECADDRNEXT=keycadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_d and keyd == 1:
				EXECADDRNEXT=keydadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_e and keye == 1:
				EXECADDRNEXT=keyeadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_f and keyf == 1:
				EXECADDRNEXT=keyfadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_g and keyg == 1:
				EXECADDRNEXT=keygadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_h and keyh == 1:
				EXECADDRNEXT=keyhadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_i and keyi == 1:
				EXECADDRNEXT=keyiadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_j and keyj == 1:
				EXECADDRNEXT=keyjadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_k and keyk == 1:
				EXECADDRNEXT=keykadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_l and keyl == 1:
				EXECADDRNEXT=keyladr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_m and keym == 1:
				EXECADDRNEXT=keymadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_n and keyn == 1:
				EXECADDRNEXT=keynadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_o and keyo == 1:
				EXECADDRNEXT=keyoadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_p and keyp == 1:
				EXECADDRNEXT=keypadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_q and keyq == 1:
				EXECADDRNEXT=keyqadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_r and keyr == 1:
				EXECADDRNEXT=keyradr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_s and keysx == 1:
				EXECADDRNEXT=keysadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_t and keyt == 1:
				EXECADDRNEXT=keytadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_u and keyu == 1:
				EXECADDRNEXT=keyuadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_v and keyv == 1:
				EXECADDRNEXT=keyvadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_w and keyw == 1:
				EXECADDRNEXT=keywadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_x and keyx == 1:
				EXECADDRNEXT=keyxadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_y and keyy == 1:
				EXECADDRNEXT=keyyadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_z and keyz == 1:
				EXECADDRNEXT=keyzadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and event.key == K_SPACE and keyspace == 1:
				EXECADDRNEXT=keyspaceadr
				EXECCHANGE=2
				break
			if event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_KP_ENTER) and keyret == 1:
				EXECADDRNEXT=keyretadr
				EXECCHANGE=2
				break
			
	
	if curinst=="--":
		stopflag=1
		abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
		abt=libSBTCVM.abtslackline(abt, "End Of Rom.")
	#check the current rom. 
	if EXECADDRraw=="+------":
		stopflag=1
		abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
		abt=libSBTCVM.abtslackline(abt, "End Of RomBus.")
	#print "eek " + EXECADDRNEXT
	#increment the program counter (EXEC addr)
	EXECADDR=libbaltcalc.btadd(EXECADDR, "+")
	EXECADDRraw=EXECADDR
	#print EXECADDR
	EXECADDR=libSBTCVM.trunkto6(EXECADDR)
	#print "ook " + EXECADDRNEXT
	if EXECCHANGE==1:
		EXECCHANGE=0
		#print("ding")
		contaddr=EXECADDR
		EXECADDR=EXECADDRNEXT
		EXECADDRraw=EXECADDR
		#print EXECADDR
	#change the thread used here to be selectable via regset.
	#only one thread can be affected by keyboard interrupts at a time.
	if EXECCHANGE==2:
		EXECCHANGE=0
		#print("ding")
		if btcurthread=="--":
			
			contaddr=EXECADDR
			EXECADDR=EXECADDRNEXT
			EXECADDRraw=EXECADDR
		else:
			BTSTACK["--"].contaddr=EXECADDR
			BTSTACK["--"].EXECADDR=EXECADDRNEXT
			BTSTACK["--"].EXECADDRraw=EXECADDRNEXT
	#if all threads close, stop VM and print apropriate VM SYSHALT message.
	if btthreadcnt<=0:
		stopflag=1
		abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
		abt=libSBTCVM.abtslackline(abt, "NO ACTIVE THREADS!")
		vmexeclog("VMSYSHALT: NO ACTIVE THREADS")
	#thread switcher
	if BTSTACK[btcurthread].qxtact==0:
		stopflag=1
		abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
		abt=libSBTCVM.abtslackline(abt, "T-ACT FAULT")
		vmexeclog("VMSYSHALT: T-ACT FAULT")
	if btthreadcnt>1:
		selnext=0
		vecnext=1
		#print "dong"
		#print btthreadcnt
		#print btcurthread
		#for threaddex in BTSTACK:
		#	print (str(BTSTACK[threaddex].qxtact) + " g " + threaddex)
		#store current thread state in BTSTACK
		if btstopthread==1:
			BTSTACK[btcurthread].qxtact=0
			btthreadcnt -=1
			btstopthread=0
		else:
			BTSTACK[btcurthread]=BTTHREAD(1, EXECADDR, REG1, REG2, contaddr, EXECADDRraw, regsetpoint, TTYBGCOLREG, TTYBGCOL, colvectorreg, monovectorreg, colorreg, tritloadlen, tritoffset, tritdestgnd, threadref, ROMFILE, ROMLAMPFLG, mempoint)
		#iteratively detrmine next thread:
		#for threaditer in ["--", "-0", "-+", "0-", "00", "0+", "+-", "+0", "++", "--", "-0", "-+", "0-", "00", "0+", "+-", "+0", "++", "--", "-0", "-+", "0-", "00", "0+", "+-", "+0", "++"]:
			#if threaditer==btcurthread:
				#selnext=1
			#if BTSTACK[threaditer].qxtact==1 and selnext==1 and threaditer!=btcurthread:
				#btcurthread=threaditer
				##print "AARRRRGGGHH!!!"
				#vecnext=0
		#if selnext==0:
			#stopflag=1
			#abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
			#abt=libSBTCVM.abtslackline(abt, "INTERNAL THREAD SWITCH FAULT")
			#print "tjump"
		instdep=btcurthread
		gotnextth=0
		while gotnextth==0:
			if len(instdep)==1:
				instdep=("0" + instdep)
			if len(instdep)==3:
				instdep="--"
			if BTSTACK[instdep].qxtact==1 and instdep!=btcurthread:
				btcurthread=instdep
				gotnextth=1
				#print "got next thread"
			instdep=libbaltcalc.btadd(instdep, "+")
				
		#load next thread state from BTSTACK entry
		EXECADDR=BTSTACK[btcurthread].EXECADDR
		REG1=BTSTACK[btcurthread].REG1
		REG2=BTSTACK[btcurthread].REG2
		contaddr=BTSTACK[btcurthread].contaddr
		EXECADDRraw=BTSTACK[btcurthread].EXECADDRraw
		regsetpoint=BTSTACK[btcurthread].regsetpoint
		#TTYBGCOLREG=BTSTACK[threaditer].TTYBGCOLREG
		#TTYBGCOL=BTSTACK[threaditer].TTYBGCOL
		colvectorreg=BTSTACK[btcurthread].colvectorreg
		monovectorreg=BTSTACK[btcurthread].monovectorreg
		colorreg=BTSTACK[btcurthread].colorreg
		tritloadlen=BTSTACK[btcurthread].tritloadlen
		tritoffset=BTSTACK[btcurthread].tritoffset
		tritdestgnd=BTSTACK[btcurthread].tritdestgnd
		threadref=BTSTACK[btcurthread].threadref
		ROMFILE=BTSTACK[btcurthread].ROMFILE
		ROMLAMPFLG=BTSTACK[btcurthread].ROMLAMPFLG
		mempoint=BTSTACK[btcurthread].mempoint
		#change the Thread status display.
		if (disablereadouts==0 or stepbystep==1) and fskipcnt == fskip:
			curthrtex=lgdispfont.render(btcurthread, True, (127, 0, 255), (0, 0, 0)).convert()
			upt=screensurf.blit(curthrtex, (170, 522))
			updtblits.extend([upt])
		
		#print EXECADDR
	if stopflag==1:
		abt=libSBTCVM.abtslackline(abt, "Press enter to exit.")
		#screensurf.fill((0,127,255))
		#screensurf.blit(vmbg, (0, 0))
	
		#these show the instruction and data in the instruction/data box :)
		insttext=smldispfont.render(curinst, True, (0, 255, 255), (0, 0, 0))
		datatext=smldispfont.render(curdata, True, (0, 255, 127), (0, 0, 0))
		screensurf.blit(insttext, (8, 522))
		screensurf.blit(datatext, (8, 566))
		#these draw the register displays :)
		reg1text=lgdispfont.render(REG1, True, (255, 0, 127), (0, 0, 0))
		reg2text=lgdispfont.render(REG2, True, (255, 127, 0), (0, 0, 0))
		screensurf.blit(reg1text, (219, 521))
		screensurf.blit(reg2text, (219, 564))
		#and here is what draws the ROM address display :)
		ROMadrtex=lgdispfont.render(EXECADDR, True, (0, 127, 255), (0, 0, 0))
		screensurf.blit(ROMadrtex, (425, 564))
		#and the current rom display :)
		CURROMTEXT=(ROMLAMPFLG)
		curROMtex=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0))
		screensurf.blit(curROMtex, (126, 522))
		#LED LAMPS
		screensurf.blit(CPULEDSTANDBY, (749, 505))
		#STEP
		screensurf.blit(STEPLED, (750, 512))
		screensurf.blit(COLORDISPBIG, (649, 1))
		screensurf.blit(MONODISPBIG, (649, 150))
		CURROMTEXT=("ROM " + ROMLAMPFLG)
		reg2text=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0))
		lineq=0
		linexq=0
		if ttystyle==0:
			libSBTCVMsurf.fill(TTYBGCOL)
			for fnx in abt:
				fnx=fnx.replace('\n', '')
				colq=0
				if TTYSIZE==0 or linexq>26:
					for qlin in fnx:
						#print qlin
						charq=libSBTCVM.charlookupdict.get(qlin)
						#print charq
						if TTYSIZE==1:
							libSBTCVM.charblit2(libSBTCVMsurf, colq, lineq, charq)
						else:
							libSBTCVM.charblit(libSBTCVMsurf, colq, lineq, charq)
						colq +=1
					lineq +=1
				linexq +=1
			upt=screensurf.blit(libSBTCVMsurf, (0, 0))
			updtblits.extend([upt])
		lineq=0
		linexq=0
		#if ttystyle==1:
			#print (chr(27) + "[2J" + chr(27) + "[H")
			#for fnx in abt:
				#fnx=fnx.replace('\n', '')
				#colq=0
				#print ("TTY|" + fnx)
				#lineq +=1
				#linexq +=1
		lineq=0
		linexq=0
		#disabled as its too buggy
		#if ttystyle==2:
			#for fnx in abt:
				#fnx=fnx.replace('\n', '')
				#colq=0
				#if TTYSIZE==0 or linexq>26:
					#if TTYSIZE==1:
						#ttyfn=ttyfontB.render(fnx, True, (255, 255, 255), (0, 0, 0)).convert()
						#upt=screensurf.blit(ttyfn, (0, (lineq*18)))
						##updtblits.extend([upt])
					#else:
						#ttyfn=ttyfont.render(fnx, True, (255, 255, 255), (0, 0, 0)).convert()
						#upt=screensurf.blit(ttyfn, (0, (lineq*9)))
						##updtblits.extend([upt])
					#lineq +=1
				#linexq +=1
		pygame.display.update()
	
	
	time.sleep(CPUWAIT)
	
	evhappenflg2=0

#print "foobar"
if logromexit==1:
	print "logging TROM MEMORY into CAP dir..."
	libtrom.dumptroms()
#print "postlog"
if logIOexit==1:
	print "logging final IObus state into CAP dir..."
	ramdmp=open((os.path.join('CAP', 'IOBUS.dmp')),  'w')
	for IOitm in RAMbank:
		ramdmp.write("A:" + str(IOitm) + " D:" + RAMbank[IOitm] + "\n")
	ramdmp.close()
#"exitloop"
if vmexeclogflg==1:
	vmexeclog("--END OF VM EXEC--")
	vmexeclog("final clock tic: " + str(exlogclockticnum) + " |final time passed: " + format((exlogcurtime), '.11f'))
	vmexeclog("aprox operations/second: " + format((exlogclockticnum / exlogcurtime), '.11f'))
	vmexlogf.close()
if trackopsec==1:
	print ("final clock tic: " + str(exlogclockticnum) + " |final time passed: " + format((exlogcurtime), '.11f'))
	print ("aprox operations/second: " + format((exlogclockticnum / exlogcurtime), '.11f'))
#if vmexeclogflg==1:
	#exlogclockticnum += 1
	#exlogcurtime=time.time()
	
if KIOSKMODE==0:
	evhappenflg3=0
	while evhappenflg3==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == K_RETURN:
					evhappenflg3=1
					break
else:
	print "KIOSK MODE ACTIVE, SKIP WAIT ON EXIT."


