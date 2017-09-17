

class PLUGIN_testpkg_testshell:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="Shell que Test"
		#taskid is set automatically
		self.taskid=0
		self.widx=140
		self.widy=140
		#x and y are required.
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy)).convert(self.screensurf)
		self.widsurf.fill(framebg)
		consolewrite("plugTEST: test plugin running")
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
		self.newinstance=0
		self.selfquit=0
		self.testsigprotect1=0
		self.launchshell=1
		self.printlist=list()
	def render(self):
		self.labtx=simplefont.render("Test Plugin", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 0))
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title, self.wo)
	def movet(self, xoff, yoff):
		self.x -= xoff
		self.y -= yoff
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		self.closerect=self.frametoup[2]
		self.widbox=self.frametoup[0]
		self.framerect=self.frametoup[1]
	#click is given pygame MOUSEBUTTONDOWN events that fall within widbox
	def click(self, event):
		self.printlist.extend(["click"])
		return
	#similar to click, except it receves MOUSEBUTTONUP events that fall within widbox.
	def clickup(self, event):
		self.printlist.extend(["clickup"])
		return
	#keydown and keyup are given pygame KEYDOWN and KEYUP events.
	def keydown(self, event):
		self.printlist.extend(["keydown"])
		return
	def keyup(self, event):
		self.printlist.extend(["keyup"])
		return
	#close is called when the window is to be closed.
	def close(self):
		self.printlist.extend(["The main window has closed", " but the input from the shell will still be returned.", "programs can use this to create various shells"])
		return
	#hostquit is called when the host program is going to quit.
	def hostquit(self):
		return
	def sig(self):
		if self.launchshell==1:
			self.launchshell=0
			return (0, shell(self.screensurf, 0, argument=self))
		return
	def que(self, signal):
		if signal[0]==102:
			return ["Shell Ready.", "Clicks and keystrokes in main window will be printed to shell.", "Anything sent will be retuned."]
		if signal[0]==101:
			self.listret=self.printlist
			self.printlist=list()
			return self.listret
		
		if signal[0]==100:
			return [signal[1]]
		return



SDAPPLUGREF=PLUGIN_testpkg_testshell
#plugin execname
SDAPNAME="testpkg_testshell"
SDAPLABEL="Shell que test"
#plugin icon refrence (60 x 60 pixels is preferred) set to None for placeholder
SDAPICON="test.png"
#plugin directory (set to None if none)
SDAPDIR="testpkg.sdap"
#category ID: 0=main 1=Games, 2=Welcome, 3=Demos, 4=Mini Tools 5=Plugins (default, will be listed in plugins regardless) should be a list.
SDAPCAT=[4]