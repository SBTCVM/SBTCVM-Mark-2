#!/usr/bin/env python
import libSBTCVM
import os
import sys
import libvmconf
TROMA="intro.trom"
TROMB=("DEFAULT.TROM")
TROMC=("DEFAULT.TROM")
TROMD=("DEFAULT.TROM")
TROME=("DEFAULT.TROM")
TROMF=("DEFAULT.TROM")

libtromready=0
tromlogging=0
logreads=0
logwrites=0



VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")
def loadtrom(filenameg):
	if os.path.isfile(filenameg):
		return(open(filenameg, "r"))
	elif os.path.isfile(os.path.join("ROMS", filenameg)):
		return(open(os.path.join("ROMS", filenameg), "r"))
	elif os.path.isfile(os.path.join("VMUSER", filenameg)):
		return(open(os.path.join("VMUSER", filenameg), "r"))
	elif os.path.isfile(os.path.join("VMSYSTEM", filenameg)):
		return(open(os.path.join("VMSYSTEM", filenameg), "r"))
	elif os.path.isfile(os.path.join(VMSYSROMS, filenameg)):
		return(open(os.path.join(VMSYSROMS, filenameg), "r"))
	else:
		#print ("FATAL ERROR: libtrom: NONEXISTENT TROM! (" + filenameg + ")")
		sys.exit("FATAL ERROR: libtrom: NONEXISTENT TROM! (" + filenameg + ")")
		

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



tromlogging=int(libvmconf.getconf("log", "tromlogging"))
if tromlogging==0:
	logreads=0
	logwrites=0
if tromlogging==1:
	logreads=1
	logwrites=1
if tromlogging==1:
	tromlog1=open(os.path.join('CAP', "libtrom.log"), "w")

def redefA(filenameq):
	global AROM
	global TROMA
	global ROMDICT
	AROM= {}
	TROMA=filenameq
	TROMAfile=loadtrom(filenameq)
	linecnt=1
	for rmline in TROMAfile:
		rmline=rmline.replace("\n", "")
		AROM[linecnt]=rmline
		linecnt += 1
	TROMAfile.close()
	ROMDICT={TROMA: AROM, TROMB: BROM, TROMC: CROM, TROME: EROM, TROMF: FROM}
	if tromlogging==1:
		tromlog1.write("Change in TROM files.  Logging TROM filename again:\n")
		tromlog1.write("TROMA:" + TROMA + "\n")

def redefB(filenameq):
	global BROM
	global TROMB
	global ROMDICT
	BROM= {}
	TROMB=filenameq
	TROMBfile=loadtrom(filenameq)
	linecnt=1
	for rmline in TROMBfile:
		rmline=rmline.replace("\n", "")
		BROM[linecnt]=rmline
		linecnt += 1
	TROMBfile.close()
	ROMDICT={TROMA: AROM, TROMB: BROM, TROMC: CROM, TROME: EROM, TROMF: FROM}
	if tromlogging==1:
		tromlog1.write("Change in TROM files.  Logging TROM filename again:\n")
		tromlog1.write("TROMB:" + TROMB + "\n")

def redefC(filenameq):
	global CROM
	global TROMC
	global ROMDICT
	CROM= {}
	TROMC=filenameq
	TROMCfile=loadtrom(filenameq)
	linecnt=1
	for rmline in TROMCfile:
		rmline=rmline.replace("\n", "")
		CROM[linecnt]=rmline
		linecnt += 1
	TROMCfile.close()
	ROMDICT={TROMA: AROM, TROMB: BROM, TROMC: CROM, TROME: EROM, TROMF: FROM}
	if tromlogging==1:
		tromlog1.write("Change in TROM files.  Logging TROM filename again:\n")
		tromlog1.write("TROMC:" + TROMC + "\n")

def redefD(filenameq):
	global DROM
	global TROMD
	global ROMDICT
	DROM= {}
	TROMD=filenameq
	TROMDfile=loadtrom(filenameq)
	linecnt=1
	for rmline in TROMDfile:
		rmline=rmline.replace("\n", "")
		DROM[linecnt]=rmline
		linecnt += 1
	TROMDfile.close()
	ROMDICT={TROMA: AROM, TROMB: BROM, TROMC: CROM, TROME: EROM, TROMF: FROM}
	if tromlogging==1:
		tromlog1.write("Change in TROM files.  Logging TROM filename again:\n")
		tromlog1.write("TROMD:" + TROMD + "\n")


def redefE(filenameq):
	global EROM
	global TROME
	global ROMDICT
	EROM= {}
	TROME=filenameq
	TROMEfile=loadtrom(filenameq)
	linecnt=1
	for rmline in TROMEfile:
		rmline=rmline.replace("\n", "")
		EROM[linecnt]=rmline
		linecnt += 1
	TROMEfile.close()
	ROMDICT={TROMA: AROM, TROMB: BROM, TROMC: CROM, TROME: EROM, TROMF: FROM}
	if tromlogging==1:
		tromlog1.write("Change in TROM files.  Logging TROM filename again:\n")
		tromlog1.write("TROME:" + TROME + "\n")


def redefF(filenameq):
	global FROM
	global TROMF
	global ROMDICT
	FROM= {}
	TROMF=filenameq
	TROMFfile=loadtrom(filenameq)
	linecnt=1
	for rmline in TROMFfile:
		rmline=rmline.replace("\n", "")
		FROM[linecnt]=rmline
		linecnt += 1
	TROMFfile.close()
	ROMDICT={TROMA: AROM, TROMB: BROM, TROMC: CROM, TROME: EROM, TROMF: FROM}
	if tromlogging==1:
		tromlog1.write("Change in TROM files.  Logging TROM filename again:\n")
		tromlog1.write("TROMF:" + TROMF + "\n")

#load TROMS from TROM files to respective dictionaries
print "libtrom: parsing TROMs into dictionaries..."
if tromlogging==1:
	tromlog1.write("Load TROMs into dictionaries... \n")
AROM= {}
TROMAfile=loadtrom(TROMA)
linecnt=1
for rmline in TROMAfile:
	rmline=rmline.replace("\n", "")
	AROM[linecnt]=rmline
	linecnt += 1
TROMAfile.close()
BROM= {}
TROMBfile=loadtrom(TROMB)
linecnt=1
for rmline in TROMBfile:
	rmline=rmline.replace("\n", "")
	BROM[linecnt]=rmline
	linecnt += 1
TROMBfile.close()
CROM= {}
TROMCfile=loadtrom(TROMC)
linecnt=1
for rmline in TROMCfile:
	rmline=rmline.replace("\n", "")
	CROM[linecnt]=rmline
	linecnt += 1
TROMCfile.close()
DROM= {}
TROMDfile=loadtrom(TROMD)
linecnt=1
for rmline in TROMDfile:
	rmline=rmline.replace("\n", "")
	DROM[linecnt]=rmline
	linecnt += 1
TROMDfile.close()
EROM= {}
TROMEfile=loadtrom(TROME)
linecnt=1
for rmline in TROMEfile:
	rmline=rmline.replace("\n", "")
	EROM[linecnt]=rmline
	linecnt += 1
TROMEfile.close()
FROM= {}
TROMFfile=loadtrom(TROMF)
linecnt=1
for rmline in TROMFfile:
	rmline=rmline.replace("\n", "")
	FROM[linecnt]=rmline
	linecnt += 1
TROMFfile.close()
if tromlogging==1:
	tromlog1.write("Done.  Logging TROM filenames for refrence:\n")
	tromlog1.write("TROMA:" + TROMA + "\n")
	tromlog1.write("TROMB:" + TROMB + "\n")
	tromlog1.write("TROMC:" + TROMC + "\n")
	tromlog1.write("TROMD:" + TROMD + "\n")
	tromlog1.write("TROME:" + TROME + "\n")
	tromlog1.write("TROMF:" + TROMF + "\n")
else:
	print "done."


ROMDICT={TROMA: AROM, TROMB: BROM, TROMC: CROM, TROME: EROM, TROMF: FROM}

libtromready=1

#read instruction function

def tromreadinst(romaddr, ROMNAME):
	line=libSBTCVM.numstruct(romaddr)
	#n = open(ROMNAME)
	linecnt=1
	#for fdelta in n:
	#	if linecnt==line:
	if ROMNAME==TROMA:
		fdelta=AROM[line]
		if logreads==1:
			tromlog1.write("READ INST. TROMA, Addr:" + romaddr + " line:" + str(line) + "\n")
	elif ROMNAME==TROMB:
		fdelta=BROM[line]
		if logreads==1:
			tromlog1.write("READ INST. TROMB, Addr:" + romaddr + " line:" + str(line) + "\n")
	elif ROMNAME==TROMC:
		fdelta=CROM[line]
		if logreads==1:
			tromlog1.write("READ INST. TROMC, Addr:" + romaddr + " line:" + str(line) + "\n")
	elif ROMNAME==TROMD:
		fdelta=DROM[line]
		if logreads==1:
			tromlog1.write("READ INST. TROMD, Addr:" + romaddr + " line:" + str(line) + "\n")
	elif ROMNAME==TROME:
		fdelta=EROM[line]
		if logreads==1:
			tromlog1.write("READ INST. TROME, Addr:" + romaddr + " line:" + str(line) + "\n")
	elif ROMNAME==TROMF:
		fdelta=FROM[line]
		if logreads==1:
			tromlog1.write("READ INST. TROMF, Addr:" + romaddr + " line:" + str(line) + "\n")
	dataret=((fdelta[0]) + (fdelta[1]) + (fdelta[2]) + (fdelta[3]) + (fdelta[4]) + (fdelta[5]))
			
	return dataret
	#	linecnt += 1

#set data function

def tromsetdata(romaddr, datax, ROMNAME):
	line=libSBTCVM.numstruct(romaddr)
	global AROM
	global BROM
	global CROM
	global DROM
	global EROM
	global FROM
	global ROMDICT
	if ROMNAME==TROMA:
		inst=(AROM[line])[0] + (AROM[line])[1] + (AROM[line])[2] + (AROM[line])[3] + (AROM[line])[4] + (AROM[line])[5]
		AROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET DATA. TROMA, Addr:" + romaddr + " line:" + str(line) + " Data:" + datax + "\n")
	elif ROMNAME==TROMB:
		inst=(BROM[line])[0] + (BROM[line])[1] + (BROM[line])[2] + (BROM[line])[3] + (AROM[line])[4] + (AROM[line])[5]
		BROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET DATA. TROMB, Addr:" + romaddr + " line:" + str(line) + " Data:" + datax + "\n")
	elif ROMNAME==TROMC:
		inst=(CROM[line])[0] + (CROM[line])[1] + (CROM[line])[2] + (CROM[line])[3] + (AROM[line])[4] + (AROM[line])[5]
		CROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET DATA. TROMC, Addr:" + romaddr + " line:" + str(line) + " Data:" + datax + "\n")
	elif ROMNAME==TROMD:
		inst=(DROM[line])[0] + (DROM[line])[1] + (DROM[line])[2] + (DROM[line])[3] + (AROM[line])[4] + (AROM[line])[5]
		DROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET DATA. TROMD, Addr:" + romaddr + " line:" + str(line) + " Data:" + datax + "\n")
	elif ROMNAME==TROME:
		inst=(EROM[line])[0] + (EROM[line])[1] + (EROM[line])[2] + (EROM[line])[3] + (AROM[line])[4] + (AROM[line])[5]
		EROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET DATA. TROME, Addr:" + romaddr + " line:" + str(line) + " Data:" + datax + "\n")
	elif ROMNAME==TROMF:
		inst=(FROM[line])[0] + (FROM[line])[1] + (FROM[line])[2] + (FROM[line])[3] + (AROM[line])[4] + (AROM[line])[5]
		FROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET DATA. TROMF, Addr:" + romaddr + " line:" + str(line) + " Data:" + datax + "\n")
	ROMDICT[ROMNAME][line]=(inst + datax)

#set instruction function


def tromsetinst(romaddr, inst, ROMNAME):
	line=libSBTCVM.numstruct(romaddr)
	global AROM
	global BROM
	global CROM
	global DROM
	global EROM
	global FROM
	global ROMDICT
	if ROMNAME==TROMA:
		datax=(AROM[line])[6] + (AROM[line])[7] + (AROM[line])[8] + (AROM[line])[9] + (AROM[line])[10] + (AROM[line])[11] + (AROM[line])[12] + (AROM[line])[13] + (AROM[line])[14]
		AROM[line]=(inst + datax)
		if logwrites==1:
			
			tromlog1.write("SET inst. TROMA, Addr:" + romaddr + " line:" + str(line) + " inst:" + inst + "\n")
	elif ROMNAME==TROMB:
		datax=(BROM[line])[6] + (BROM[line])[7] + (BROM[line])[8] + (BROM[line])[9] + (BROM[line])[10] + (BROM[line])[11] + (BROM[line])[12] + (BROM[line])[13] + (BROM[line])[14]
		BROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET inst. TROMB, Addr:" + romaddr + " line:" + str(line) + " inst:" + inst + "\n")
	elif ROMNAME==TROMC:
		datax=(CROM[line])[6] + (CROM[line])[7] + (CROM[line])[8] + (CROM[line])[9] + (CROM[line])[10] + (CROM[line])[11] + (CROM[line])[12] + (CROM[line])[13] + (CROM[line])[14]
		CROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET inst. TROMC, Addr:" + romaddr + " line:" + str(line) + " inst:" + inst + "\n")
	elif ROMNAME==TROMD:
		datax=(DROM[line])[6] + (DROM[line])[7] + (DROM[line])[8] + (DROM[line])[9] + (DROM[line])[10] + (DROM[line])[11] + (DROM[line])[12] + (DROM[line])[13] + (DROM[line])[14]
		DROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET inst. TROMD, Addr:" + romaddr + " line:" + str(line) + " inst:" + inst + "\n")
	elif ROMNAME==TROME:
		datax=(EROM[line])[6] + (EROM[line])[7] + (EROM[line])[8] + (EROM[line])[9] + (EROM[line])[10] + (EROM[line])[11] + (EROM[line])[12] + (EROM[line])[13] + (EROM[line])[14]
		EROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET inst. TROME, Addr:" + romaddr + " line:" + str(line) + " inst:" + inst + "\n")
	elif ROMNAME==TROMF:
		datax=(FROM[line])[6] + (FROM[line])[7] + (FROM[line])[8] + (FROM[line])[9] + (FROM[line])[10] + (FROM[line])[11] + (FROM[line])[12] + (FROM[line])[13] + (FROM[line])[14]
		FROM[line]=(inst + datax)
		if logwrites==1:
			tromlog1.write("SET inst. TROMF, Addr:" + romaddr + " line:" + str(line) + " inst:" + inst + "\n")
	ROMDICT[ROMNAME][line]=(inst + datax)

	
def tromreaddata(romaddr, ROMNAME):
	line=libSBTCVM.numstruct(romaddr)
	#n = open(ROMNAME)
	linecnt=1
	if ROMNAME==TROMA:
		fdelta=AROM[line]
		if logreads==1:
			tromlog1.write("READ DATA. TROMA, Addr:" + romaddr + " line:" + str(line) + "\n")
	elif ROMNAME==TROMB:
		fdelta=BROM[line]
		if logreads==1:
			tromlog1.write("READ DATA. TROMB, Addr:" + romaddr + " line:" + str(line) + "\n")
	elif ROMNAME==TROMC:
		fdelta=CROM[line]
		if logreads==1:
			tromlog1.write("READ DATA. TROMC, Addr:" + romaddr + " line:" + str(line) + "\n")
	elif ROMNAME==TROMD:
		fdelta=DROM[line]
		if logreads==1:
			tromlog1.write("READ DATA. TROMD, Addr:" + romaddr + " line:" + str(line) + "\n")
	elif ROMNAME==TROME:
		fdelta=EROM[line]
		if logreads==1:
			tromlog1.write("READ DATA. TROME, Addr:" + romaddr + " line:" + str(line) + "\n")
	elif ROMNAME==TROMF:
		fdelta=FROM[line]
		if logreads==1:
			tromlog1.write("READ DATA. TROMF, Addr:" + romaddr + " line:" + str(line) + "\n")
	#for fdelta in n:
	#	if linecnt==line:
	dataret=((fdelta[6]) + (fdelta[7]) + (fdelta[8]) + (fdelta[9]) + (fdelta[10]) + (fdelta[11]) + (fdelta[12]) + (fdelta[13]) + (fdelta[14]))
	return dataret
	#	linecnt += 1


def dumptroms():
	ROMAdmp=open(os.path.join('CAP', "TROMA.dmp"), "w")
	#itercnt=1
	for itm in AROM:
		ROMAdmp.write(AROM[itm])
		ROMAdmp.write('\n')
	ROMAdmp.close()
	ROMBdmp=open(os.path.join('CAP', "TROMB.dmp"), "w")
	#itercnt=1
	for itm in BROM:
		ROMBdmp.write(BROM[itm])
		ROMBdmp.write('\n')
	ROMBdmp.close()
	ROMCdmp=open(os.path.join('CAP', "TROMC.dmp"), "w")
	#itercnt=1
	for itm in CROM:
		ROMCdmp.write(CROM[itm])
		ROMCdmp.write('\n')
	ROMCdmp.close()
	ROMDdmp=open(os.path.join('CAP', "TROMD.dmp"), "w")
	#itercnt=1
	for itm in DROM:
		ROMDdmp.write(DROM[itm])
		ROMDdmp.write('\n')
	ROMDdmp.close()
	ROMEdmp=open(os.path.join('CAP', "TROME.dmp"), "w")
	#itercnt=1
	for itm in EROM:
		ROMEdmp.write(EROM[itm])
		ROMEdmp.write('\n')
	ROMEdmp.close()
	ROMFdmp=open(os.path.join('CAP', "TROMF.dmp"), "w")
	#itercnt=1
	for itm in FROM:
		ROMFdmp.write(FROM[itm])
		ROMFdmp.write('\n')
	ROMFdmp.close()

def manualdumptroms():
	ROMAdmp=open(os.path.join('CAP', "TROMAman.dmp"), "w")
	#itercnt=1
	for itm in AROM:
		ROMAdmp.write(AROM[itm])
		ROMAdmp.write('\n')
	ROMAdmp.close()
	ROMBdmp=open(os.path.join('CAP', "TROMBman.dmp"), "w")
	#itercnt=1
	for itm in BROM:
		ROMBdmp.write(BROM[itm])
		ROMBdmp.write('\n')
	ROMBdmp.close()
	ROMCdmp=open(os.path.join('CAP', "TROMCman.dmp"), "w")
	#itercnt=1
	for itm in CROM:
		ROMCdmp.write(CROM[itm])
		ROMCdmp.write('\n')
	ROMCdmp.close()
	ROMDdmp=open(os.path.join('CAP', "TROMDman.dmp"), "w")
	#itercnt=1
	for itm in DROM:
		ROMDdmp.write(DROM[itm])
		ROMDdmp.write('\n')
	ROMDdmp.close()
	ROMEdmp=open(os.path.join('CAP', "TROMEman.dmp"), "w")
	#itercnt=1
	for itm in EROM:
		ROMEdmp.write(EROM[itm])
		ROMEdmp.write('\n')
	ROMEdmp.close()
	ROMFdmp=open(os.path.join('CAP', "TROMFman.dmp"), "w")
	#itercnt=1
	for itm in FROM:
		ROMFdmp.write(FROM[itm])
		ROMFdmp.write('\n')
	ROMFdmp.close()


#print(tromreadinst("------", "BOOTUP.TROM"))
#print(tromreaddata("------", "BOOTUP.TROM"))



