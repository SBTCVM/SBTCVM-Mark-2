#!/usr/bin/env python
import os
import sys
import wave
import struct
import VMSYSTEM.libSBTCVM as libSBTCVM
import VMSYSTEM.libbaltcalc as libbaltcalc
VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")

def wavargfind(arg):
	lowarg=arg.lower()
	argisfile=0
	qfilewasvalid=0
	for extq in ["", ".WAV", ".wav"]:
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


try:
	cmd=sys.argv[1]
except:
	cmd=None
if cmd=="-h" or cmd=="--help" or cmd=="help":
	print '''This is SBTCVM Mark 2's Ternary Wave toolkit.
commands:
MK2-TWAV.py -h (--help) (help): this text
MK2-TWAV.py -v (--version)
MK2-TWAV.py -a (--about): about MK2-TWAV.py
MK2-TWAV.py -2k [wavefile] convert 16bit signed, mono, 2000Hz wave file to 2Khz SBTCVM Sample.
MK2-TWAV.py -4k [wavefile] convert 16bit signed, mono, 4000Hz wave file to 4Khz SBTCVM Sample.'''
elif cmd=="-v" or cmd=="--version":
	print "SBTCVM Mark 2 Ternary Wave toolkit v1.0.0"
elif cmd==None:
	print "tip: use MK2-TWAV.py -h for help."
elif cmd=="-a" or cmd=="--about":
	print '''#SBTCVM Mark 2 Ternary Wave toolkit

v1.0.0

Copyright (c) 2016-2018 Thomas Leathers and Contributors 

  SBTCVM Mark 2 Ternary Wave toolkit is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Mark 2 Ternary Wave toolkit is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Mark 2 Ternary Wave toolkit. If not, see <http://www.gnu.org/licenses/>
'''
elif cmd=="-2k" or cmd=="-4k":
	try:
		twav=wavargfind(sys.argv[2])
	except:
		sys.exit("ERROR: Must specify wave file.")
	#waveFile = wave.open('hello-2000HzQualitysample.wav', 'r')
	#waveFile = wave.open('helloworld2.wav', 'r')
	#waveFile = wave.open('musictest3.wav', 'r')
	waveFile = wave.open(twav, 'r')
	print("checking input file for correct format...")
	#check for valid input file.
	if waveFile.getnchannels()!=1:
		sys.exit("ERROR. AUDIO MUST BE MONO!")
	if waveFile.getsampwidth()!=2:
		sys.exit("ERROR. AUDIO MUST BE 16bit!")
	if waveFile.getframerate()!=2000 and cmd=="-2k":
		sys.exit("ERROR. AUDIO MUST BE 2000Khz!")
	if waveFile.getframerate()!=4000 and cmd=="-4k":
		sys.exit("ERROR. AUDIO MUST BE 4000Khz!")
	print("passed.")
	
	assmflename=twav
	assmnamelst=assmflename.rsplit('.', 1)
	tasmfile=(assmnamelst[0] + (".tasm"))
	outfile=open(tasmfile, "w")
	outfile.write("#Autoconverted by MK2-TWAV: SBTCVM's Ternary Wave conversion toolkit.\n#Converted from: \"" + twav + "\"\n")
	if cmd=="-2k":
		freqnumxxx="---------"
		freqstr="2Khz 1-trit SBTCVM Mark 2 sample format."
	else:
		freqnumxxx="--------0"
		freqstr="4Khz 1-trit SBTCVM Mark 2 sample format."
	length = waveFile.getnframes()
	#write information comments and add functional test routine.
	#notice how the length is linear-bias encoded (length-9841). this lets the length be much larger.
	outfile.write('''
#tip: replace the 1s with 2s, 3s, or 4s to change the sample channel.
#MK2-TWAV.py automatically calculates sample length for you. 
#if you are writing a specialty utility, see its code.
#format: ''' + freqstr + '''

setreg1|>wavhead
IOwrite1|>sam1off
setreg1|''' + libSBTCVM.trunkto6(libbaltcalc.DECTOBT(length-9841)) + '''
IOwrite1|>sam1len
setreg1|'''+ freqnumxxx +'''
IOwrite1|>sam1freq
IOwrite1|>sam1play
userwait
stop
''')
	outfile.write("null|")
	#outfile=open("outdata.twav", "w")
	if cmd=="-2k":
		print("Please wait. processing wave into Ternary 1-trit 2Khz audio...")
	else:
		print("Please wait. processing wave into Ternary 1-trit 4Khz audio...")
	
	cnt=1
	roll=9
	firstline=1
	#iterate through wave file frames and convert each data point to trits...
	for i in range(0,length): 
		#print waveData
		data = struct.unpack("<h", waveFile.readframes(1))
		wavdata=(int(data[0]))
		#print(wavdata)
		if wavdata>2000:
			outfile.write("+")
		elif wavdata<-2000:
			outfile.write("-")
		else:
			outfile.write("0")
		if cnt<roll:
			cnt+=1
		else:
			cnt=1
			#add wavhead refrence label
			if firstline==1:
				firstline=0
				outfile.write("|wavhead\nnull|")
			else:
				outfile.write("\nnull|")
	#ensure data is not short on last word.
	while cnt<=roll:
		outfile.write("0")
		cnt+=1
	outfile.write("|endpoint")
	print("Done.")