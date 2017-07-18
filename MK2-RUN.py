#!/usr/bin/env python

import VMSYSTEM.libSBTCVM as libSBTCVM
import VMSYSTEM.libbaltcalc as libbaltcalc
import sys
import os


VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")
try:
	cmd=sys.argv[1]
except:
	cmd=None
if cmd=="-h" or cmd=="--help" or cmd=="help":
	print '''This is MK2-RUN.py, a command line launcher for SBTCVM Mark 2
commands:
MK2-RUN.py -h (--help) (help): this text
MK2-RUN.py -v (--version)
MK2-RUN.py -a (--about): about MK2-RUN.py
MK2-RUN.py -r (--run) [trom file]: run a trom as TROMA
MK2-RUN.py [trom file]: run a trom as TROMA
MK2-RUN.py -r (--run) [streg file]: run specified streg file.
MK2-RUN.py [streg file]: run specified streg file.
MK2-RUN.py -le (--log_exec): same as -r but activates exec logging.
MK2-RUN.py -tos: report aprox operations/second at end of execution.

note:
MK2-RUN.py is equipped with a searching capacity. 
trying to run "example" wopuld match "example.streg" and "example.trom"
also the subdirectories: "VMUSER", "VMSYSTEM", and "ROMS" are searched as well.
'''
elif cmd=="-v" or cmd=="--version":
	print "SBTCVM MK2-RUN launcher v2.0.2"
elif cmd=="-a" or cmd=="--about":
	print '''#SBTCVM Mark 2 commandline launcher


v2.0.2

(c)2016-2017 Thomas Leathers and Contributors

  SBTCVM Mark 2 commandline launcher is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Mark 2 commandline launcher is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Mark 2 commandline launcher. If not, see <http://www.gnu.org/licenses/>
'''
elif cmd==None:
	print "tip: use MK2-RUN.py -h for help."
elif cmd=="-r" or cmd=="--run" or cmd[0]!="-" or cmd=="-k" or cmd=="-le" or cmd=="--log_exec" or cmd=="-tos":
	if cmd[0]!="-":
		arg=sys.argv[1]
	else:
		arg=sys.argv[2]
		print arg
	if cmd=="-le" or cmd=="--log_exec":
		GLOBLOGEXEC=1
	if cmd=="-tos":
		GLOBOPSEC=1
	if cmd=="-k":
		GLOBKIOSK=1
	lowarg=arg.lower()
	argisfile=0
	qfilewasvalid=0
	for extq in ["", ".streg", ".STREG", ".TROM", ".trom"]:
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
			if qlowarg.endswith(".trom") and os.path.isfile(qarg):
				print "SBTCVM TROM file detected."
				GLOBRUNFLG=qarg
				VMFILE=open('SBTCVM_MK2.py', 'r')
				EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
				exec(EXECVM)
				qfilewasvalid=1
				break
			
			elif qlowarg.endswith(".streg") and os.path.isfile(qarg):
				print "SBTCVM trom execution group file, detected."
				GLOBSTREG=qarg
				VMFILE=open('SBTCVM_MK2.py', 'r')
				EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
				exec(EXECVM)
				qfilewasvalid=1
				break
			else:
				print "not valid."
				argisfile=0
				
	if qfilewasvalid==0:
		print "File not found."

			
			