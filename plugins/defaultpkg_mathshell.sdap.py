
class PLUGIN_defaultpkg_mathshell:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="Math Shell"
		#taskid is set automatically
		self.taskid=0
		self.widx=140
		self.widy=140
		self.helptext=vmui.listline("""Math Shell help:
btdec [bt] = convert balanced ternary integer to decimal
decbt [dec] = convert decimal integer to balanced ternary
invert [bt] = invert a balanced ternary integer
mpi [dec] = max positive integer of [dec] trits
mni [dec] = max negative integer of [dec] trits
mcv [dec] = max combinations value of [dec] trits
add [bt] [bt] = add two balanced ternary integers
sub [bt] [bt] = subtract two balanced ternary integers
div [bt] [bt] = divide two balanced ternary integers
mul [bt] [bt] = multiply two balanced ternary integers
""")
		#x and y are required.
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy)).convert(self.screensurf)
		self.widsurf.fill(framebg)
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
		self.startshell=1
		self.quitnow=0
		self.printlist=list()
	def render(self):
		return
		#drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title, self.wo)
	def movet(self, xoff, yoff):
		self.x -= xoff
		self.y -= yoff
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		self.closerect=self.frametoup[2]
		self.widbox=self.frametoup[0]
		self.framerect=self.frametoup[1]
	#click is given pygame MOUSEBUTTONDOWN events that fall within widbox
	def click(self, event):
		return
	#similar to click, except it receves MOUSEBUTTONUP events that fall within widbox.
	def clickup(self, event):
		return
	#keydown and keyup are given pygame KEYDOWN and KEYUP events.
	def keydown(self, event):
		return
	def keyup(self, event):
		return
	#close is called when the window is to be closed.
	def close(self):
		return
	#hostquit is called when the host program is going to quit.
	def hostquit(self):
		return
	def sig(self):
		if self.startshell==1:
			self.startshell=0
			self.quitnow=1
			consolewrite("Math Shell: starting instance of shell")
			return (0, shell(self.screensurf, 0, argument=self))	
		if self.quitnow==1:
			self.quitnow=0
			consolewrite("Math Shell: closing main program and entering Shell Ghost mode.")
			return (1, 1)
		return
	def que(self, signal):
		if signal[0]==102:
			return ["Math Shell Ready."]
		if signal[0]==101:
			self.listret=self.printlist
			self.printlist=list()
			return self.listret
		
		if signal[0]==100:
			self.cmdlist=(signal[1]).split(" ", 1)
			self.cmd=(self.cmdlist[0]).lower()
			if self.cmd=="help":
				return self.helptext
			if self.cmd=="btdec":
				try:
					self.arg=self.cmdlist[1]
					return [str(libbaltcalc.btint(self.arg).dec())]
				except IndexError:
					return ["please specify one balanced ternary integer"]
			if self.cmd=="invert":
				try:
					self.arg=self.cmdlist[1]
					return [str(libbaltcalc.btint(self.arg).invert())]
				except IndexError:
					return ["please specify one balanced ternary integer"]
			if self.cmd=="decbt":
				try:
					self.arg=self.cmdlist[1]
					#print libbaltcalc.DECTOBT(int(arg))
					return [str(libbaltcalc.btint(int(self.arg)))]
				except IndexError:
					return ["please specify one decimal integer."]
				except TypeError:
					return ["Please specify one decimal integer."]
				except ValueError:
					return ["Please specify one decimal integer."]
			if self.cmd=="mpi":
				try:
					self.arg=self.cmdlist[1]
					#print libbaltcalc.DECTOBT(int(arg))
					if abs(int(self.arg))<=100:
						return [str(libbaltcalc.mpi(int(self.arg)))]
					else:
						return ["argument is too large"]
				except IndexError:
					return ["please specify one decimal integer."]
				except TypeError:
					return ["Please specify one decimal integer."]
				except ValueError:
					return ["Please specify one decimal integer."]
			if self.cmd=="mni":
				try:
					self.arg=self.cmdlist[1]
					#print libbaltcalc.DECTOBT(int(arg))
					if abs(int(self.arg))<=100:
						return [str(libbaltcalc.mni(int(self.arg)))]
					else:
						return ["argument is too large"]
				except IndexError:
					return ["please specify one decimal integer."]
				except TypeError:
					return ["Please specify one decimal integer."]
				except ValueError:
					return ["Please specify one decimal integer."]
			if self.cmd=="mcv":
				try:
					self.arg=self.cmdlist[1]
					#print libbaltcalc.DECTOBT(int(arg))
					if abs(int(self.arg))<=100:
						return [str(libbaltcalc.mcv(int(self.arg)))]
					else:
						return ["argument is too large"]
				except IndexError:
					return ["please specify one decimal integer."]
				except TypeError:
					return ["Please specify one decimal integer."]
				except ValueError:
					return ["Please specify one decimal integer."]
			if self.cmd=="add":
				try:
					self.arg=self.cmdlist[1]
					self.arglst=self.arg.split(" ")
					self.arg1=self.arglst[0]
					self.arg2=self.arglst[1]
					
					return [str(libbaltcalc.btint(self.arg1) + libbaltcalc.btint(self.arg2))]
				except IndexError:
					return ["please specify two balanced ternary integers"]
			if self.cmd=="sub":
				try:
					self.arg=self.cmdlist[1]
					self.arglst=self.arg.split(" ")
					self.arg1=self.arglst[0]
					self.arg2=self.arglst[1]
					
					return [str(libbaltcalc.btint(self.arg1) - libbaltcalc.btint(self.arg2))]
				except IndexError:
					return ["please specify two balanced ternary integers"]
			if self.cmd=="div":
				try:
					self.arg=self.cmdlist[1]
					self.arglst=self.arg.split(" ")
					self.arg1=self.arglst[0]
					self.arg2=self.arglst[1]
					
					return [str(libbaltcalc.btint(self.arg1) // libbaltcalc.btint(self.arg2))]
				except ZeroDivisionError:
					return ["ERROR: DIVISION BY ZERO"]
				except IndexError:
					return ["please specify two balanced ternary integers"]
			if self.cmd=="mul":
				try:
					self.arg=self.cmdlist[1]
					self.arglst=self.arg.split(" ")
					self.arg1=self.arglst[0]
					self.arg2=self.arglst[1]
					
					return [str(libbaltcalc.btint(self.arg1) * libbaltcalc.btint(self.arg2))]
				except IndexError:
					return ["please specify two balanced ternary integers"]


#Refrence to class of plugin util
SDAPPLUGREF=PLUGIN_defaultpkg_mathshell
#plugin execname
SDAPNAME="defaultpkg_mathshell"
SDAPLABEL="Math Shell"
#plugin icon refrence (60 x 60 pixels is preferred) set to None for placeholder
SDAPICON="mathshell.png"
#plugin directory (set to None if none)
SDAPDIR="defaultpkg.sdap"
#category ID: 0=main 1=Games, 2=Welcome, 3=Demos, 4=Mini Tools 5=Plugins (default, will be listed in plugins regardless) should be a list.
SDAPCAT=[4]