#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as libbaltcalc
from VMSYSTEM.libbaltcalc import btint
import VMSYSTEM.libvmcmdshell as cmdshell

try:
	import readline
except ImportError:
	print "failed to load readline."

import sys
import os
from subprocess import call
VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")
try:
	cmd=sys.argv[1]
except:
	cmd=None
if cmd=="-h" or cmd=="--help" or cmd=="help":
	print '''This is MK2-CS.py, a command shell for SBTCVM Mark 2
commands:
MK2-CS.py -h (--help) (help): this text
MK2-CS.py -v (--version)
MK2-CS.py -a (--about): about MK2-RUN.py
'''
elif cmd=="-v" or cmd=="--version":
	print cmdshell.versiontext
elif cmd=="-a" or cmd=="--about":
	print cmdshell.abouttext
elif cmd==None:
	qflg=0
	usrinp=""
	print cmdshell.versiontext
	print "ready."
	while qflg!=1:
		userinp=raw_input((':'))
		usercalllst=userinp.split(" ", 1)
		if (usercalllst[0]).lower()=="help":
			print cmdshell.helptext
		elif (usercalllst[0]).lower()=="about":
			print cmdshell.abouttext
		elif (usercalllst[0]).lower()=="version":
			print cmdshell.versiontext
		elif (usercalllst[0]).lower()=="list":
			try:
				if (usercalllst[1]).lower()=="types":
					for typename in cmdshell.keyftypes:
						print typename
				elif (usercalllst[1]).lower()=="paths":
					for typename in cmdshell.pathlist:
						print typename
				elif (usercalllst[1]).lower()=="help":
					print cmdshell.listhelptext
				else:
					for dittype in cmdshell.keyftypes:
						if (usercalllst[1]).lower()==dittype:
							for diter in cmdshell.pathlist:
								for fname in os.listdir(diter):
									fnamelo=fname.lower()
									if fnamelo.endswith(("." + dittype)): 
										print(os.path.join(diter, fname))
			except IndexError:
				for diter in cmdshell.pathlist:
					for fname in os.listdir(diter):
						fnamelo=fname.lower()
						for dittype in cmdshell.keyftypes:
							if fnamelo.endswith("." + dittype):
								print(os.path.join(diter, fname))
		#these simply call another python process altogether to re-use the command line syntax of these utilities:
		elif (usercalllst[0]).lower()=="asm":
			try:
				arglst=list((usercalllst[1]).split(" "))
				arglst2=list(["python", "SBTCVM-asm2.py"])
				arglst2.extend(arglst)
				call(arglst2)
			except IndexError:
				call(["python", "SBTCVM-asm2.py"])
			
		elif (usercalllst[0]).lower()=="run":
			try:
				arglst=list((usercalllst[1]).split(" "))
				arglst2=list(["python", "MK2-RUN.py"])
				arglst2.extend(arglst)
				call(arglst2)
			except IndexError:
				call(["python", "MK2-RUN.py"])
		elif (usercalllst[0]).lower()=="gfx":
			try:
				arglst=list((usercalllst[1]).split(" "))
				arglst2=list(["python", "MK2-GFX.py"])
				arglst2.extend(arglst)
				call(arglst2)
			except IndexError:
				call(["python", "MK2-GFX.py"])
		elif (usercalllst[0]).lower()=="t" or (usercalllst[0]).lower()=="tools":
			try:
				arglst=list((usercalllst[1]).split(" "))
				arglst2=list(["python", "MK2-TOOLS.py"])
				arglst2.extend(arglst)
				call(arglst2)
			except IndexError:
				call(["python", "MK2-TOOLS.py"])
		elif (usercalllst[0]).lower()=="mainmenu":
				call(["python", "MK2-MENU.py"])
		elif (usercalllst[0]).lower()=="quit":
			qflg=1
		elif (usercalllst[0]).lower()=="btdec":
			try:
				arg=usercalllst[1]
				print btint(arg).dec()
			except IndexError:
				print "please specify one balanced ternary integer"
		elif (usercalllst[0]).lower()=="invert":
			try:
				arg=usercalllst[1]
				print btint(arg).invert()
			except IndexError:
				print "please specify one balanced ternary integer"
		elif (usercalllst[0]).lower()=="decbt":
			try:
				arg=usercalllst[1]
				#print libbaltcalc.DECTOBT(int(arg))
				print btint(int(arg))
			except IndexError:
				print "please specify one decimal integer"
			except TypeError:
				print "Please specify one decimal integer."
			except ValueError:
				print "Please specify one decimal integer."
		elif (usercalllst[0]).lower()=="mpi":
			try:
				arg=usercalllst[1]
				#calculate the MPI of the user-specifed number of trits
				print libbaltcalc.mpi(int(arg))
			except IndexError:
				print "please specify one decimal integer"
			except TypeError:
				print "Please specify one decimal integer."
			except ValueError:
				print "Please specify one decimal integer."
		elif (usercalllst[0]).lower()=="mni":
			try:
				arg=usercalllst[1]
				#calculate the MPI of the user-specifed number of trits
				print libbaltcalc.mni(int(arg))
			except IndexError:
				print "please specify one decimal integer"
			except TypeError:
				print "Please specify one decimal integer."
			except ValueError:
				print "Please specify one decimal integer."
		elif (usercalllst[0]).lower()=="mcv":
			try:
				arg=usercalllst[1]
				print libbaltcalc.mcv(int(arg))
			except IndexError:
				print "please specify one decimal integer"
			except TypeError:
				print "Please specify one decimal integer."
			except ValueError:
				print "Please specify one decimal integer."
		elif (usercalllst[0]).lower()=="add":
			try:
				arg=usercalllst[1]
				arglst=arg.split(" ")
				arg1=arglst[0]
				arg2=arglst[1]
				
				print (btint(arg1) + btint(arg2))
			except IndexError:
				print "please specify two balanced ternary integers separated by a space."
		elif (usercalllst[0]).lower()=="mul":
			try:
				arg=usercalllst[1]
				arglst=arg.split(" ")
				arg1=arglst[0]
				arg2=arglst[1]
				
				print (btint(arg1) * btint(arg2))
			except IndexError:
				print "please specify two balanced ternary integers separated by a space."
		elif (usercalllst[0]).lower()=="sub":
			try:
				arg=usercalllst[1]
				arglst=arg.split(" ")
				arg1=arglst[0]
				arg2=arglst[1]
				
				print (btint(arg1) - btint(arg2))
			except IndexError:
				print "please specify two balanced ternary integers separated by a space."
		elif (usercalllst[0]).lower()=="div":
			try:
				arg=usercalllst[1]
				arglst=arg.split(" ")
				arg1=arglst[0]
				arg2=arglst[1]
				
				print (btint(arg1) // btint(arg2))
			except ZeroDivisionError:
				print "ERROR: DIVISION BY ZERO"
			except IndexError:
				print "please specify two balanced ternary integers separated by a space."
		elif (usercalllst[0]).lower()!="":
			print "Unknown Command. Type \"help\" for help."
		
		
		
else:
	print "tip: use MK2-CS.py -h for help."
#elif cmd=="-s" or cmd=="--shell" or cmd[0]!="-":
	
			