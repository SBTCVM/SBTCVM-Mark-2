#!/usr/bin/env python
import VMSYSTEM.libtrom as libtrom
import pygame
import subprocess
from pygame.locals import *
import time
import os
import VMSYSTEM.libSBTCVM as libSBTCVM
import VMSYSTEM.libbaltcalc as libbaltcalc
import VMSYSTEM.libvmui as vmui
import sys
import VMSYSTEM.libvmconf as libvmconf
import VMSYSTEM.libthemeconf as libthemeconf
import VMSYSTEM.libSBTGA as libSBTGA
from random import randint
pygame.display.init()

print "SBTCVM Mark 2 Starting up..."

#SBTCVM Mark 2
#Simple Balanced Ternary Computer Virtual Machine
#
#v2.0.3
#
# Copyright (c) 2016-2018 Thomas Leathers and Contributors 
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
	def __init__(self, qxtactg, EXECADDRg, REG1g, REG2g, contaddrg, EXECADDRrawg, regsetpointg, TTYBGCOLREGg, TTYBGCOLg, colvectorregg, monovectorregg, colorregg, tritloadleng, tritoffsetg, tritdestgndg, threadrefg, ROMFILEg, ROMLAMPFLGg, mempointg, timewaitg, waittillg):
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
		self.mempoint=mempointg
		self.timewait=timewaitg
		self.waittill=waittillg
#ROMFILE=TROMA
#ROMLAMPFLG="A"


windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'icon64.png'))
pygame.display.set_icon(windowicon)

disablereadouts=int(libvmconf.getconf("video", "disablereadouts"))


screensurf=pygame.display.set_mode((950, 600))
simplefont = pygame.font.SysFont(None, 16)

#used for smaller data displays (inst. data etc.)
#smldispfont = pygame.font.SysFont(None, 16)
smldispfont = pygame.font.Font(os.path.join("VMSYSTEM", "SBTCVMreadout.ttf"), 16)
#used in larger data displays (register displays, etc.)
#lgdispfont = pygame.font.SysFont(None, 20)
lgdispfont = pygame.font.Font(os.path.join("VMSYSTEM", "SBTCVMreadout.ttf"), 16)



#
#position bank:
hudsize=44
pausebtnx=3
pausebtny=3
sysmx=46
sysmy=3
ttyyoffset=44
#ttyxoffset=0
colordispx=649
colordispy=1 + hudsize
cdispscale=148 + 148
mdispscale=144
mdispx=649
mdispy=150 + 148 + hudsize
statybegin=360
statx=800
statjump=30
statrect=(statx, statybegin - 15, 150, 300)
hudrect=pygame.Rect(0, 0, 950, hudsize)



vmbg=pygame.Surface((950, 600)).convert()
vmbg.fill(libthemeconf.vmbg)

#vmbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VMBG.png')).convert()
pygame.draw.rect(vmbg, libthemeconf.hudbg, hudrect, 0)
pygame.draw.rect(vmbg, libthemeconf.vmstatbg, statrect, 0)

staty=statybegin-15
for label in ["instruction", "data", "register 1", "register 2", "address", "current rom", "thread"]:
	labgx=simplefont.render(label, True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
	vmbg.blit(labgx, (statx, staty))
	staty += statjump

#pauseicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'PAUSEBTN.png')).convert()

sbtcvmbadge=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'SBTCVMbadge.png')).convert()
vmbg.blit(sbtcvmbadge, ((950-120), 0))

fmicon=pygame.image.load(os.path.join("VMSYSTEM", "GFX", 'filemenuicon.png')).convert_alpha()
pauseicon=vmui.makemenubtn("FILE", icon=fmicon)
sysmenuicon=vmui.makemenubtn("SYSTEM", width=80)
pausex=vmbg.blit(pauseicon, (pausebtnx, pausebtny))
sysmenux=vmbg.blit(sysmenuicon, (sysmx, sysmy))
screensurf.blit(vmbg, (0, 0))
#init in non-kiosk mode for now, SBTCVM will re-init once it knows the kioskmode state.
vmui.initui(screensurf, 0)
pygame.display.update()
libSBTCVM.glyphoptim(screensurf)
pygame.display.set_caption("SBTCVM Mark 2", "SBTCVM Mark 2")
pygame.font.init()


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
#LEDGREENON=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-GREEN.png')).convert()
#LEDGREENOFF=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-GREEN-OFF.png')).convert()
#CPU
#CPULEDACT=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-BLUE.png')).convert()
#CPULEDSTANDBY=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-ORANGE.png')).convert()

COLORDISP=pygame.Surface((27, 27)).convert()
MONODISP=pygame.Surface((9, 9)).convert()
COLORDISP.fill((127, 127, 127))
MONODISP.fill((127, 127, 127))

#this list is what is displayed on the TTY on VM boot.
#the header text is so far in this list so it appears correct in 27 line mode
abt=["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "SBTCVM", "Mark 2", "v2.0.3", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "ready", ""]
abtpref=["This is different", "Mark 2", "v2.0.0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "ready"]
abtclear=["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
#abt54clear=["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
#ttysize:
#0=72x54 (9x9 chars)
#1=72x27 (9x18 chars)

TTYMODE=0
TTYSIZE=1
mixrate=int(libvmconf.getconf("audio", "mixrate"))
pygame.mixer.init(frequency=mixrate , size=-16)

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



CPUWAIT=float(libvmconf.getconf("cpu", "cpuwait"))
stepbystep=int(libvmconf.getconf("cpu", "stepbystep"))
vmexeclogflg=int(libvmconf.getconf("log", "vmexec"))
logromexit=int(libvmconf.getconf("log", "romexit"))
logIOexit=int(libvmconf.getconf("log", "ioexit"))
disablereadouts=int(libvmconf.getconf("video", "disablereadouts"))
fskip=int(libvmconf.getconf("video", "fskip"))
ttystyle=int(libvmconf.getconf("video", "ttystyle"))
DEFAULTSTREG=libvmconf.getconf("bootup", "DEFAULTSTREG")

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
	libtrom.redefB(TROMB)
	libtrom.redefC(TROMC)
	libtrom.redefD(TROMD)
	libtrom.redefE(TROME)
	libtrom.redefF(TROMF)
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

sysmdisread0=vmui.menuitem("status readouts (off)", "READ0")
sysmdisread1=vmui.menuitem("status readouts (on)", "READ1")
sysmstep0=vmui.menuitem("step-by-step debugging (off)", "STEP0")
sysmstep1=vmui.menuitem("step-by-step debugging (on)", "STEP1")
sysmtty0=vmui.menuitem("TTY (on)", "TTY0")
sysmtty1=vmui.menuitem("TTY (off)", "TTY1")
sysmmemorydmp=vmui.menuitem("Generate Memory *.DMPs", "DMP")
sysmcapplot=vmui.menuitem("Capture plotters", "DISPDMP")
sysmcapscr=vmui.menuitem("Capture screenshot", "SCSHOT")
sysmhalted=vmui.menuitem("(System halted)", "SYSHLT", noclick=1)
def sysmenu(x=sysmx, y=(sysmy+40), posthalt=0):
	pygame.mixer.pause()
	global disablereadouts
	global stepbystep
	global ttystyle
	global ttyredraw
	global ttyredrawfull
	if disablereadouts==1:
		sysmdisread=sysmdisread0
	else:
		sysmdisread=sysmdisread1
	if stepbystep==1:
		sysmstep=sysmstep1
	else:
		sysmstep=sysmstep0
	if ttystyle==0:
		sysmtty=sysmtty0
	else:
		sysmtty=sysmtty1
	if posthalt==1:
		sysmmen=[sysmhalted, sysmmemorydmp, sysmcapplot, sysmcapscr]
	else:
		sysmmen=[sysmdisread, sysmstep, sysmtty, sysmmemorydmp, sysmcapplot, sysmcapscr]
	menuret=vmui.menuset(sysmmen, x, y, reclick=0, scrndest='SCREENSHOT.png', fontsize=26)
	if menuret=="READ0":
		disablereadouts=0
	if menuret=="READ1":
		disablereadouts=1
	if menuret=="STEP0":
		stepbystep=1
	if menuret=="STEP1":
		stepbystep=0
	if menuret=="TTY0":
		ttystyle=1
	if menuret=="TTY1":
		ttystyle=0
		ttyredraw=1
		ttyredrawfull=1
	if menuret=="DISPDMP":
		pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
		pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
	if menuret=="SCSHOT":
		pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
	if menuret=="DMP":
		ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
		for IOitm in IOdumplist:
			ramdmp.write(RAMbank[IOitm] + "\n")
		ramdmp.close()
		for threaddex in BTSTACK:
			print (str(BTSTACK[threaddex].qxtact) + " " + threaddex)
		libtrom.manualdumptroms()
	pygame.mixer.unpause()
	return
		
		

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
if 'GLOBKIOSK' in globals():	
	if KIOSKMODE==1:
		disablereadouts=0
		ttystyle=0
		print "Kiosk mode active... enabling readouts and TTY mode 0..."

#if disablereadouts==1:
	#screensurf=pygame.display.set_mode((950, 600))
	#screensurf.blit(vmbg, (0, 0))
	#pygame.display.update()


TTYBGCOL=libSBTCVM.colorfind("------")
TTYBGCOLREG="------"
quickquit=0

colvectorreg="000000"
monovectorreg="000000"


#keep unused events out of queue
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN])

libSBTCVMsurf=pygame.Surface((648, 486)).convert()
libSBTCVMsurf.fill(TTYBGCOL)
libSBTCVM.glyphoptim(libSBTCVMsurf)
libSBTCVMsurfshort=pygame.Surface((648, 90)).convert(libSBTCVMsurf)
libSBTCVMsurfshort.fill(TTYBGCOL)
#RAMBANK startup begin
RAMbank = {}

#calmlst = open("ORDEREDLIST6.txt")
#screensurf.fill((0,127,255))

shortttybgfix=pygame.Surface((648, 96)).convert()
shortttybgfix.fill(libthemeconf.vmbg)

#build IObus dictionary.
IOdumplist=list()
IOgen="---------"
RAMbank["---------"] = "000000000"
#IOdumplist.extend([IOgen])
while IOgen!="+++++++++":
	IOdumplist.extend([IOgen])
	IOgen=libSBTCVM.trunkto6(libbaltcalc.btadd(IOgen, "+"))
	RAMbank[IOgen] = "000000000"
	
RAMbank["+++++++++"] = "000000000"
IOdumplist.extend([IOgen])
#set Random integer port with an inital random integer
RAMbank["--0------"]=libSBTCVM.trunkto6(libbaltcalc.DECTOBT(randint(-9841,9841)))

ttyredraw=1

#IO read only list. IO addresses in this list are treated as read only. for example:
#the random integer port is read only.
IOreadonly=["--0------"]

MONODISPBIG=pygame.transform.scale(MONODISP, (mdispscale, mdispscale))
COLORDISPBIG=pygame.transform.scale(COLORDISP, (cdispscale, cdispscale))
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
ttyredrawfull=1
updtmdisp=1
updtblits=list()
updtttyprev=list()
updtrandport=1
#upt=screensurf.blit(CPULEDACT, (749, 505))
#updtblits.extend([upt])
#upt=screensurf.blit(STEPLED, (750, 512))
#updtblits.extend([upt])
print "Prep threading system..."
threadref="00"
#vmexeclog("Preping threading system...")

prevCLOCK=2242

ttyredrawfull=1
timewait=0
waittill=time.time()
BTSTACK={"--": BTTHREAD(1, EXECADDR, REG1, REG2, contaddr, EXECADDRraw, regsetpoint, TTYBGCOLREG, TTYBGCOL, colvectorreg, monovectorreg, colorreg, tritloadlen, tritoffset, tritdestgnd, threadref, ROMFILE, ROMLAMPFLG, mempoint, timewait, waittill)}
for cur_id in ["-0","-+","0-","00","0+","+-","+0","++"]:
    BTSTACK[cur_id] = BTTHREAD(0, EXECADDR, REG1, REG2, contaddr, EXECADDRraw, regsetpoint, TTYBGCOLREG, TTYBGCOL, colvectorreg, monovectorreg, colorreg, tritloadlen, tritoffset, tritdestgnd, threadref, ROMFILE, ROMLAMPFLG, mempoint, timewait, waittill)

btthreadcnt=1
btcurthread="--"

curinst="000000"
curdata="000000000"

staty=statybegin
insttext=smldispfont.render(curinst, True, libthemeconf.vminst, libthemeconf.vmstatbg)
datatext=smldispfont.render(curdata, True, libthemeconf.vmdata, libthemeconf.vmstatbg)
upt=screensurf.blit(insttext, (statx, staty))
updtblits.extend([upt])
staty += statjump
upt=screensurf.blit(datatext, (statx, staty))
updtblits.extend([upt])
staty += statjump
#these draw the register displays :)
reg1text=lgdispfont.render(REG1, True, libthemeconf.vmreg1, libthemeconf.vmstatbg)
reg2text=lgdispfont.render(REG2, True, libthemeconf.vmreg2, libthemeconf.vmstatbg)
upt=screensurf.blit(reg1text, (statx, staty))
updtblits.extend([upt])
staty += statjump
upt=screensurf.blit(reg2text, (statx, staty))
updtblits.extend([upt])
staty += statjump
#and here is what draws the ROM address display :)
ROMadrtex=lgdispfont.render(EXECADDR, True, libthemeconf.vmaddr, libthemeconf.vmstatbg)
upt=screensurf.blit(ROMadrtex, (statx, staty))
updtblits.extend([upt])

staty += statjump
#and the current rom display :)
CURROMTEXT=(ROMLAMPFLG)
curROMtex=lgdispfont.render(CURROMTEXT, True, libthemeconf.vmrom, libthemeconf.vmstatbg)
upt=screensurf.blit(curROMtex, (statx, staty))
updtblits.extend([upt])
staty += statjump
staty += statjump
if stepbystep==0:	
	labgx=simplefont.render("Clock: Step by Step", True, libthemeconf.vmstatbg, libthemeconf.vmstatbg).convert()
	upt2=screensurf.blit(labgx, (statx, staty))
	labgx=simplefont.render("Clock: Normal run", True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
	upt=screensurf.blit(labgx, (statx, staty))
else:
	labgx=simplefont.render("Clock: Normal run", True, libthemeconf.vmstatbg, libthemeconf.vmstatbg).convert()
	upt2=screensurf.blit(labgx, (statx, staty))
	labgx=simplefont.render("Clock: Step by Step", True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
	upt=screensurf.blit(labgx, (statx, staty))
updtblits.extend([upt])
updtblits.extend([upt2])

curthrtex=lgdispfont.render(btcurthread, True, libthemeconf.vmcurth, libthemeconf.vmstatbg).convert()
upt=screensurf.blit(curthrtex, (statx, (statybegin + (statjump*6))))
updtblits.extend([upt])

ttyblitsprev=list()
ttyblits=list()

exlogclockticnum=0


#SBTGA setup
#SBTGA Bus
dispmembus=libtrom.AROM
#SBTGA display mode SB should be default
dispmode="SB"
#master valid mode list
displist=["G0", "G2", "SB", "G3", "G4"]
#all Modes that should disable TTY rendering need to be in here!
dispttyover=["G0", "G2", "G3", "G4"]
#default SBTGA offset.
dispoffset="000000000"
updatedisp=0
SBTGADEV=libSBTGA.buffdisplay(screensurf, dispmembus, dispoffset, mode=dispmode)


#3 voice sound gen volume control (fine tune to prevent clipping!)
voicechanvol=0.5

svoice1sam=pygame.mixer.Sound(libSBTCVM.mk23voicesample("0000000"))
svoice2sam=pygame.mixer.Sound(libSBTCVM.mk23voicesample("0000000"))
svoice3sam=pygame.mixer.Sound(libSBTCVM.mk23voicesample("0000000"))
svoice1sam.set_volume(voicechanvol)
svoice2sam.set_volume(voicechanvol)
svoice3sam.set_volume(voicechanvol)
sv1bak=svoice1sam
sv2bak=svoice2sam
sv3bak=svoice3sam
#for f in BTSTACK:
#	print str(BTSTACK[f].qxtact) + " " + f
#for f in BTSTACK:
#	print str(BTSTACK[f].qxtact) + " " + f	
print "SBTCVM Mark 2 Ready. the VM will now begin."
#vmexeclog("SBTCVM Mark 2 Ready. the VM will now begin.")
initaltime=time.time()


while stopflag==0:
	#instruction load
	EXECADDRNUM=libSBTCVM.numstruct(EXECADDR)
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
	#logging and track operations/second
	if trackopsec==1 and timewait==0:
		exlogclockticnum += 1
		exlogcurtime=(time.time() - initaltime)
	elif vmexeclogflg==1 and timewait==0:
		exlogclockticnum += 1
		exlogcurtime=(time.time() - initaltime)
		vmexeclog("data: " + curdata + " |Inst: " + curinst + " |adr: " + EXECADDR +  " |Mem point: " + mempoint +" |thread: " + btcurthread + " |exec bank: " + ROMLAMPFLG + " |reg1: " + REG1 + " |reg2: " + REG2 + " |tic #: " + str(exlogclockticnum) + " |secs: " + format((exlogcurtime), '.11f'))
	#main render
	if fskipcnt == fskip or stepbystep==1:
		if disablereadouts==0 or stepbystep==1:
			#screensurf.blit(vmbg, (0, 0))
			#these show the instruction and data in the instruction/data box :)
			staty=statybegin
			if prevINST!=curinst:
				insttext=smldispfont.render(curinst, True, libthemeconf.vminst, libthemeconf.vmstatbg).convert()
				prevINST=curinst
				upt=screensurf.blit(insttext, (statx, staty))
				updtblits.extend([upt])
			staty += statjump
			if prevDATA!=curdata:
				datatext=smldispfont.render(curdata, True, libthemeconf.vmdata, libthemeconf.vmstatbg).convert()
				prevDATA=curdata
				upt=screensurf.blit(datatext, (statx, staty))
				updtblits.extend([upt])
			staty += statjump
			#these draw the register displays :)
			if prevREG1!=REG1:
				reg1text=lgdispfont.render(REG1, True, libthemeconf.vmreg1, libthemeconf.vmstatbg).convert()
				prevREG1=REG1
				upt=screensurf.blit(reg1text, (statx, staty))
				updtblits.extend([upt])
			staty += statjump
			if prevREG2!=REG2:
				reg2text=lgdispfont.render(REG2, True, libthemeconf.vmreg2, libthemeconf.vmstatbg).convert()
				prevREG2=REG2
				upt=screensurf.blit(reg2text, (statx, staty))
				updtblits.extend([upt])
			staty += statjump
			#and here is what draws the ROM address display :)
			ROMadrtex=lgdispfont.render(EXECADDR, True, libthemeconf.vmaddr, libthemeconf.vmstatbg).convert()
			upt=screensurf.blit(ROMadrtex, (statx, staty))
			updtblits.extend([upt])
			staty += statjump
			#and the current rom display :)
			CURROMTEXT=(ROMLAMPFLG)
			if prevROM!=CURROMTEXT:
				curROMtex=lgdispfont.render(CURROMTEXT, True, libthemeconf.vmrom, libthemeconf.vmstatbg).convert()
				prevROM=CURROMTEXT
				upt=screensurf.blit(curROMtex, (statx, staty))
				updtblits.extend([upt])
			staty += statjump
			staty += statjump
			if prevCLOCK!=stepbystep:
				prevCLOCK=stepbystep
				if stepbystep==0:
					
					labgx=simplefont.render("Clock: Step by Step", True, libthemeconf.vmstatbg, libthemeconf.vmstatbg).convert()
					upt2=screensurf.blit(labgx, (statx, staty))
					labgx=simplefont.render("Clock: Normal run", True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
					upt=screensurf.blit(labgx, (statx, staty))
				else:
					labgx=simplefont.render("Clock: Normal run", True, libthemeconf.vmstatbg, libthemeconf.vmstatbg).convert()
					upt2=screensurf.blit(labgx, (statx, staty))
					labgx=simplefont.render("Clock: Step by Step", True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
					upt=screensurf.blit(labgx, (statx, staty))
				updtblits.extend([upt])
				updtblits.extend([upt2])
		else:
			staty=statybegin + (statjump * 7)
			if prevCLOCK!=stepbystep:
				prevCLOCK=stepbystep
				if stepbystep==0:
					
					labgx=simplefont.render("Clock: Step by Step", True, libthemeconf.vmstatbg, libthemeconf.vmstatbg).convert()
					upt2=screensurf.blit(labgx, (statx, staty))
					labgx=simplefont.render("Clock: Normal run", True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
					upt=screensurf.blit(labgx, (statx, staty))
				else:
					labgx=simplefont.render("Clock: Normal run", True, libthemeconf.vmstatbg, libthemeconf.vmstatbg).convert()
					upt2=screensurf.blit(labgx, (statx, staty))
					labgx=simplefont.render("Clock: Step by Step", True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
					upt=screensurf.blit(labgx, (statx, staty))
				updtblits.extend([upt])
				updtblits.extend([upt2])
			
		#LED LAMPS
		#CPU
		#screensurf.blit(CPULEDACT, (749, 505))
		#STEP
		
		if updtcdisp==1:
			updtcdisp=0
			COLORDISPBIG=pygame.transform.scale(COLORDISP, (cdispscale, cdispscale))
			upt=screensurf.blit(COLORDISPBIG, (colordispx, colordispy))
			updtblits.extend([upt])
		if updtmdisp==1:
			updtmdisp=0
			MONODISPBIG=pygame.transform.scale(MONODISP, (mdispscale, mdispscale))
			upt=screensurf.blit(MONODISPBIG, (mdispx, mdispy))
			updtblits.extend([upt])
		if abtpref!=abt or ttyredraw==1:
			abtpref=abt
			ttyredraw=0
			lineq=0
			linexq=0
			if ttystyle==0 and dispmode not in dispttyover:
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
								xq=libSBTCVM.charblit2(libSBTCVMsurf, colq, lineq, charq)
							else:
								xq=libSBTCVM.charblit(libSBTCVMsurf, colq, lineq, charq)
							xq[1].y += ttyyoffset
							ttyblits.extend([xq[1]])
							colq +=1
						lineq +=1
					linexq +=1		
				upt=screensurf.blit(libSBTCVMsurf, (0, ttyyoffset))
				if ttyredrawfull==1:
					updtblits.extend([upt])
					ttyredrawfull=0
				else:
					updtblits = updtblits + ttyblits + ttyblitsprev
				#updtblits.extend([upt])
				#updtblits.append(ttyblits)
				#updtblits.append(ttyblitsprev)
				
				#print updtblits
				ttyblitsprev=ttyblits
				ttyblits=list()
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
	#bypass instruction parser in entirety if in timewait mode.
	if timewait==1:
		pass
	#ROM READ (first register)
	elif curinst=="------":
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
			if curdata=="--0---+-+":
				if REG1=="---------":
					dispmode="G0"
				elif REG1=="--------+":
					dispmode="G2"
				elif REG1=="-------0-":
					dispmode="G3"
				elif REG1=="-------00":
					dispmode="G4"
				else:
					dispmode="SB"
				ttyredraw=1
				ttyredrawfull=1
				upt=screensurf.blit(shortttybgfix, (0, 504))
				updtblits.extend([upt])
				SBTGADEV.setmode(dispmode)
			if curdata=="--0---+0-":
				dispoffset=REG1
				SBTGADEV.setoffset(dispoffset)
			if curdata=="--0---+00":
				updatedisp=1
		else:
			print "address \"" + curdata + "\" is read-only."
	#IO WRITE REG2
	elif curinst=="----0+":
		if curdata not in IOreadonly:
			rambnkcur=RAMbank[curdata]
			RAMbank[curdata] = tritlen(REG2, rambnkcur)
			if curdata=="--0---+-+":
				if REG2=="---------":
					dispmode="G0"
				elif REG2=="--------+":
					dispmode="G2"
				elif REG2=="-------0-":
					dispmode="G3"
				elif REG2=="-------00":
					dispmode="G4"
				else:
					dispmode="SB"
				ttyredraw=1
				ttyredrawfull=1
				upt=screensurf.blit(shortttybgfix, (0, 504))
				updtblits.extend([upt])
				SBTGADEV.setmode(dispmode)
			if curdata=="--0---+0-":
				dispoffset=REG2
				SBTGADEV.setoffset(dispoffset)
			if curdata=="--0---+00":
				updatedisp=1
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
		timewait=1
		waittill=(time.time()+libSBTCVM.timedecode(curdata))
		#waitchop=curdata[5]
		#if waitchop=="+":
		#	waitmagn=0.3
		#elif waitchop=="-":
		#	waitmagn=0.1
		#else:
		#	waitmagn=0.2
		#time.sleep(( waitmagn))
	#asks user if goto to adress is desired
	elif curinst=="--0+--":
		abt=libSBTCVM.abtslackline(abt, ("GOTO: (" + curdata + ") Y or N?"))
		abt=libSBTCVM.abtslackline(abt, "")
		ttyredraw=1
		USRYN=1
		extradraw=1	
	#user wait
	elif curinst=="--0+-0":
		abt=libSBTCVM.abtslackline(abt, ("Press enter to continue."))
		abt=libSBTCVM.abtslackline(abt, "")
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
			ttyredrawfull=1
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
			qxp=BTTHREAD(0, EXECADDR, REG1, REG2, contaddr, EXECADDRraw, regsetpoint, TTYBGCOLREG, TTYBGCOL, colvectorreg, monovectorreg, colorreg, tritloadlen, tritoffset, tritdestgnd, threadref, ROMFILE, ROMLAMPFLG, "---------", 0, time.time())
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
	#3 VOICE SOUND:
	elif curinst=="-00-++":
		sndvcode=curdata[0]
		sndccode=curdata[1]
		sndfreqcode=(curdata[2] + curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8])
		if sndccode=="+":
			if sndvcode=="+":
				sv1bak=svoice1sam
				svoice1sam=pygame.mixer.Sound(libSBTCVM.mk23voicesample(sndfreqcode))
				svoice1sam.set_volume(voicechanvol)
			if sndvcode=="0":
				sv2bak=svoice2sam
				svoice2sam=pygame.mixer.Sound(libSBTCVM.mk23voicesample(sndfreqcode))
				svoice2sam.set_volume(voicechanvol)
			if sndvcode=="-":
				sv3bak=svoice3sam
				svoice3sam=pygame.mixer.Sound(libSBTCVM.mk23voicesample(sndfreqcode))
				svoice3sam.set_volume(voicechanvol)
		if sndccode=="0":
			if sndvcode=="+":
				sv1bak.stop()
				svoice1sam.stop()
				svoice1sam.play(-1)
			if sndvcode=="0":
				sv2bak.stop()
				svoice2sam.stop()
				svoice2sam.play(-1)
			if sndvcode=="-":
				sv3bak.stop()
				svoice3sam.stop()
				svoice3sam.play(-1)
		if sndccode=="-":
			if sndvcode=="+":
				sv1bak.stop()
				svoice1sam.stop()
			if sndvcode=="0":
				sv2bak.stop()
				svoice2sam.stop()
			if sndvcode=="-":
				sv3bak.stop()
				svoice3sam.stop()
	#NULL INSTRUCTION (new variant) (compilers should use this in place of the legacy code.)
	#elif curinst=="000000":
	#	
	#	print("")
	if updtrandport==1:
		updtrandport=0
		RAMbank["--0------"]=libSBTCVM.trunkto6(libbaltcalc.DECTOBT(randint(-9841,9841)))
	
	if updatedisp==1:
		updatedisp=0
		upt=SBTGADEV.render(x=0, y=ttyyoffset)
		updtblits.extend([upt])
	#needed by user quering opcodes such as 0+--	
	if extradraw==1:
		#screensurf.blit(vmbg, (0, 0))
		#these show the instruction and data in the instruction/data box :)
		staty=statybegin
		insttext=smldispfont.render(curinst, True, libthemeconf.vminst, libthemeconf.vmstatbg)
		datatext=smldispfont.render(curdata, True, libthemeconf.vmdata, libthemeconf.vmstatbg)
		screensurf.blit(insttext, (statx, staty))
		staty += statjump
		screensurf.blit(datatext, (statx, staty))
		staty += statjump
		#these draw the register displays :)
		reg1text=lgdispfont.render(REG1, True, libthemeconf.vmreg1, libthemeconf.vmstatbg)
		reg2text=lgdispfont.render(REG2, True, libthemeconf.vmreg2, libthemeconf.vmstatbg)
		screensurf.blit(reg1text, (statx, staty))
		staty += statjump
		screensurf.blit(reg2text, (statx, staty))
		staty += statjump
		#and here is what draws the ROM address display :)
		ROMadrtex=lgdispfont.render(EXECADDR, True, libthemeconf.vmaddr, libthemeconf.vmstatbg)
		screensurf.blit(ROMadrtex, (statx, staty))
		staty += statjump
		#and the current rom display :)
		CURROMTEXT=(ROMLAMPFLG)
		curROMtex=lgdispfont.render(CURROMTEXT, True, libthemeconf.vmrom, libthemeconf.vmstatbg)
		screensurf.blit(curROMtex, (statx, staty))
		staty += statjump
		staty += statjump
		if stepbystep==0:	
			labgx=simplefont.render("Clock: Step by Step", True, libthemeconf.vmstatbg, libthemeconf.vmstatbg).convert()
			upt2=screensurf.blit(labgx, (statx, staty))
			labgx=simplefont.render("Clock: Normal run", True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
			upt=screensurf.blit(labgx, (statx, staty))
		else:
			labgx=simplefont.render("Clock: Normal run", True, libthemeconf.vmstatbg, libthemeconf.vmstatbg).convert()
			upt2=screensurf.blit(labgx, (statx, staty))
			labgx=simplefont.render("Clock: Step by Step", True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
			upt=screensurf.blit(labgx, (statx, staty))
		updtblits.extend([upt])
		updtblits.extend([upt2])
		screensurf.blit(COLORDISPBIG, (colordispx, colordispy))
		screensurf.blit(MONODISPBIG, (mdispx, mdispy))
		#TTY drawer :)
		#abtpref=abt
		#ttyredraw=0
		lineq=0
		linexq=0
		if ttystyle==0 and dispmode not in dispttyover:
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
			upt=screensurf.blit(libSBTCVMsurf, (0, ttyyoffset))
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
					
				if event.type == MOUSEBUTTONDOWN:
					if sysmenux.collidepoint(event.pos)==1 and event.button==1:
						sysmenu()
					if pausex.collidepoint(event.pos)==1 and event.button==1:
						pmenret=vmui.pausemenu()
						if pmenret=="s":
							stopflag=1
							abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
							abt=libSBTCVM.abtslackline(abt, "User stop.")
							vmexeclog("VMSYSHALT: USER STOP")
							evhappenflg2=1
							break
						if pmenret=="qs":
							stopflag=1
							abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
							abt=libSBTCVM.abtslackline(abt, "User stop.")
							vmexeclog("VMSYSHALT: USER STOP")
							evhappenflg2=1
							quickquit=1
							break
						else:
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
					if pmenret=="qs":
						stopflag=1
						abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
						abt=libSBTCVM.abtslackline(abt, "User stop.")
						vmexeclog("VMSYSHALT: USER STOP")
						evhappenflg2=1
						quickquit=1
						break
					else:
						break
				if event.type == KEYDOWN and event.key == K_F1:
					subprocess.Popen(["python", "helpview.py", "vmhelp.xml"])
				if event.type == KEYDOWN and event.key == K_F7:
					pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
					pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F2:
					stepbystep=1
					break
				if event.type == KEYDOWN and event.key == K_F10:
					ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
					for IOitm in IOdumplist:
						ramdmp.write(RAMbank[IOitm] + "\n")
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
					updtcdisp=1
					ttyredraw=1
					updtmdisp=1
					ttyredrawfull=1
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
				if event.type == MOUSEBUTTONDOWN:
					if sysmenux.collidepoint(event.pos)==1 and event.button==1:
						sysmenu()
					if pausex.collidepoint(event.pos)==1 and event.button==1:
						pmenret=vmui.pausemenu()
						if pmenret=="s":
							stopflag=1
							abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
							abt=libSBTCVM.abtslackline(abt, "User stop.")
							vmexeclog("VMSYSHALT: USER STOP")
							evhappenflg2=1
							break
						if pmenret=="qs":
							stopflag=1
							abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
							abt=libSBTCVM.abtslackline(abt, "User stop.")
							vmexeclog("VMSYSHALT: USER STOP")
							evhappenflg2=1
							quickquit=1
							break
						else:
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
					if pmenret=="qs":
						stopflag=1
						abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
						abt=libSBTCVM.abtslackline(abt, "User stop.")
						vmexeclog("VMSYSHALT: USER STOP")
						evhappenflg2=1
						quickquit=1
						break
					else:
						break
				if event.type == KEYDOWN and event.key == K_F1:
					subprocess.Popen(["python", "helpview.py", "vmhelp.xml"])
				if event.type == KEYDOWN and event.key == K_F7:
					pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
					pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F2:
					stepbystep=1
					break
				if event.type == KEYDOWN and event.key == K_F10:
					ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
					for IOitm in IOdumplist:
						ramdmp.write(RAMbank[IOitm] + "\n")
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
					updtcdisp=1
					ttyredraw=1
					updtmdisp=1
					ttyredrawfull=1
					break
		abt=libSBTCVM.abtslackline(abt, ("\n"))
		USRYN=0
	
	#print(EXECADDR)
	if stepbystep==1 and timewait==0:
		#this is used when step-by-step mode is enabled
		evhappenflg2=0
		while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_RETURN:
					evhappenflg2=1
					break
				if event.type == MOUSEBUTTONDOWN:
					if sysmenux.collidepoint(event.pos)==1 and event.button==1:
						sysmenu()
						if stepbystep==0:
							evhappenflg2=1
							break
					if pausex.collidepoint(event.pos)==1 and event.button==1:
						pmenret=vmui.pausemenu()
						if pmenret=="s":
							stopflag=1
							abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
							abt=libSBTCVM.abtslackline(abt, "User stop.")
							vmexeclog("VMSYSHALT: USER STOP")
							evhappenflg2=1
							break
						if pmenret=="qs":
							stopflag=1
							abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
							abt=libSBTCVM.abtslackline(abt, "User stop.")
							vmexeclog("VMSYSHALT: USER STOP")
							evhappenflg2=1
							quickquit=1
							break
						else:
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
					if pmenret=="qs":
						stopflag=1
						abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
						abt=libSBTCVM.abtslackline(abt, "User stop.")
						vmexeclog("VMSYSHALT: USER STOP")
						evhappenflg2=1
						quickquit=1
						break
					else:
						break
				if event.type == KEYDOWN and event.key == K_F1:
					subprocess.Popen(["python", "helpview.py", "vmhelp.xml"])
				if event.type == KEYDOWN and event.key == K_F7:
					pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
					pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F2:
					stepbystep=0
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_F4:
					if disablereadouts==1:
						disablereadouts=0
						print "readouts enabled"
					elif disablereadouts==0:
						print "readouts disabled"
						disablereadouts=1
					updtcdisp=1
					ttyredraw=1
					updtmdisp=1
					ttyredrawfull=1
					break
				if event.type == KEYDOWN and event.key == K_F10:
					ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
					for IOitm in IOdumplist:
						ramdmp.write(RAMbank[IOitm] + "\n")
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
				if pmenret=="qs":
					stopflag=1
					abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
					abt=libSBTCVM.abtslackline(abt, "User stop.")
					vmexeclog("VMSYSHALT: USER STOP")
					evhappenflg2=1
					quickquit=1
					break
				else:
					break
			if event.type == MOUSEBUTTONDOWN:
				if sysmenux.collidepoint(event.pos)==1 and event.button==1:
					sysmenu()
				if pausex.collidepoint(event.pos)==1 and event.button==1:
					pmenret=vmui.pausemenu()
					if pmenret=="s":
						stopflag=1
						abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
						abt=libSBTCVM.abtslackline(abt, "User stop.")
						vmexeclog("VMSYSHALT: USER STOP")
						evhappenflg2=1
						break
					if pmenret=="qs":
						stopflag=1
						abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
						abt=libSBTCVM.abtslackline(abt, "User stop.")
						vmexeclog("VMSYSHALT: USER STOP")
						evhappenflg2=1
						quickquit=1
						break
					else:
						break
			if event.type == KEYDOWN and event.key == K_F1:
					subprocess.Popen(["python", "helpview.py", "vmhelp.xml"])
			if event.type == KEYDOWN and event.key == K_F7:
				pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
				pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
				break
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
				break
			if event.type == KEYDOWN and event.key == K_F10:
				ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
				for IOitm in IOdumplist:
					ramdmp.write(RAMbank[IOitm] + "\n")
				ramdmp.close()
				for threaddex in BTSTACK:
					print (str(BTSTACK[threaddex].qxtact) + " " + threaddex)
				libtrom.manualdumptroms()
				break
			if event.type == KEYDOWN and event.key == K_F2:
				stepbystep=1
				break
			if event.type == KEYDOWN and event.key == K_F4:
				if disablereadouts==1:
					disablereadouts=0
					print "readouts enabled"
				elif disablereadouts==0:
					print "readouts disabled"
					disablereadouts=1
				updtcdisp=1
				ttyredraw=1
				updtmdisp=1
				ttyredrawfull=1
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
	#exit timewait state for current thread if waittill time has been reached or passed.
	if time.time()>=waittill:
		timewait=0
	#print "eek " + EXECADDRNEXT
	#increment the program counter (EXEC addr)
	if timewait!=1:
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
			BTSTACK[btcurthread].timewait=0
			btthreadcnt -=1
			btstopthread=0
		else:
			BTSTACK[btcurthread]=BTTHREAD(1, EXECADDR, REG1, REG2, contaddr, EXECADDRraw, regsetpoint, TTYBGCOLREG, TTYBGCOL, colvectorreg, monovectorreg, colorreg, tritloadlen, tritoffset, tritdestgnd, threadref, ROMFILE, ROMLAMPFLG, mempoint, timewait, waittill)
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
		timewait=BTSTACK[btcurthread].timewait
		waittill=BTSTACK[btcurthread].waittill
		#change the Thread status display.
		if (disablereadouts==0 or stepbystep==1) and fskipcnt == fskip:
			curthrtex=lgdispfont.render(btcurthread, True, libthemeconf.vmcurth, libthemeconf.vmstatbg).convert()
			#upt=screensurf.blit(curthrtex, (170, 522))
			upt=screensurf.blit(curthrtex, (statx, (statybegin + (statjump*6))))
			updtblits.extend([upt])
		
		#print EXECADDR
	if stopflag==1:
		abt=libSBTCVM.abtslackline(abt, "Press enter to exit.")
		abt=libSBTCVM.abtslackline(abt, "")
		#screensurf.fill((0,127,255))
		#screensurf.blit(vmbg, (0, 0))
	
		staty=statybegin
		insttext=smldispfont.render(curinst, True, libthemeconf.vminst, libthemeconf.vmstatbg)
		datatext=smldispfont.render(curdata, True, libthemeconf.vmdata, libthemeconf.vmstatbg)
		screensurf.blit(insttext, (statx, staty))
		staty += statjump
		screensurf.blit(datatext, (statx, staty))
		staty += statjump
		#these draw the register displays :)
		reg1text=lgdispfont.render(REG1, True, libthemeconf.vmreg1, libthemeconf.vmstatbg)
		reg2text=lgdispfont.render(REG2, True, libthemeconf.vmreg2, libthemeconf.vmstatbg)
		screensurf.blit(reg1text, (statx, staty))
		staty += statjump
		screensurf.blit(reg2text, (statx, staty))
		staty += statjump
		#and here is what draws the ROM address display :)
		ROMadrtex=lgdispfont.render(EXECADDR, True, libthemeconf.vmaddr, libthemeconf.vmstatbg)
		screensurf.blit(ROMadrtex, (statx, staty))
		staty += statjump
		#and the current rom display :)
		CURROMTEXT=(ROMLAMPFLG)
		curROMtex=lgdispfont.render(CURROMTEXT, True, libthemeconf.vmrom, libthemeconf.vmstatbg)
		screensurf.blit(curROMtex, (statx, staty))
		#LED LAMPS
		#screensurf.blit(CPULEDSTANDBY, (749, 505))
		#STEP
		#screensurf.blit(STEPLED, (750, 512))
		staty += statjump
		staty += statjump
		if stepbystep==0:	
			labgx=simplefont.render("Clock: Step by Step", True, libthemeconf.vmstatbg, libthemeconf.vmstatbg).convert()
			upt2=screensurf.blit(labgx, (statx, staty))
			labgx=simplefont.render("Clock: System Halted", True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
			upt=screensurf.blit(labgx, (statx, staty))
		else:
			labgx=simplefont.render("Clock: Normal run", True, libthemeconf.vmstatbg, libthemeconf.vmstatbg).convert()
			upt2=screensurf.blit(labgx, (statx, staty))
			labgx=simplefont.render("Clock: System Halted", True, libthemeconf.vmstattext, libthemeconf.vmstatbg).convert()
			upt=screensurf.blit(labgx, (statx, staty))
		updtblits.extend([upt])
		updtblits.extend([upt2])
		screensurf.blit(COLORDISPBIG, (colordispx, colordispy))
		screensurf.blit(MONODISPBIG, (mdispx, mdispy))
		CURROMTEXT=("ROM " + ROMLAMPFLG)
		reg2text=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0))
		lineq=0
		linexq=0
		if ttystyle==0 and dispmode not in dispttyover:
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
			upt=screensurf.blit(libSBTCVMsurf, (0, ttyyoffset))
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
	for IOitm in IOdumplist:
		ramdmp.write(RAMbank[IOitm] + "\n")
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

if quickquit==0:
	evhappenflg3=0
	while evhappenflg3==0:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				if sysmenux.collidepoint(event.pos)==1 and event.button==1:
					sysmenu(posthalt=1)
				if pausex.collidepoint(event.pos)==1 and event.button==1:
					pmenret=vmui.pausemenu(posthalt=1)
					if pmenret=="s":
						evhappenflg3=1
						break
					if pmenret=="qs":
						evhappenflg3=1
						break
					else:
						break
			if event.type == pygame.KEYDOWN and event.key == K_RETURN:
				evhappenflg3=1
				break
			if event.type == KEYDOWN and event.key == K_F1:
				subprocess.Popen(["python", "helpview.py", "vmhelp.xml"])
			if event.type == KEYDOWN and event.key == K_F7:
				pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
				pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
			if event.type == KEYDOWN and event.key == K_F10:
				ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
				for IOitm in IOdumplist:
					ramdmp.write(RAMbank[IOitm] + "\n")
				ramdmp.close()
				for threaddex in BTSTACK:
					print (str(BTSTACK[threaddex].qxtact) + " " + threaddex)
				libtrom.manualdumptroms()



