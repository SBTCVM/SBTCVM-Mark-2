

#important notice: please keep variables inside class except for (see below)
#notice: these plugins will be in the "plugins" directory in accordance to the plugin system.
#Plugin classes should be prefixed with "PLUGIN_" the text following such should match SDAPNAME!

class PLUGIN_testpkg_testwid:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="TEST"
		#taskid is set automatically
		self.taskid=0
		
		self.widx=140
		self.widy=140
		#x and y are required.
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy)).convert(self.screensurf)
		self.widsurf.fill(framebg)
		consolewrite("TEST: Test Tool running")
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
	def render(self):
		self.labtx=simplefont.render("window order: " + str(self.wo), True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 0))
		self.labtx=simplefont.render("taskid: " + str(self.taskid), True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 20))
		self.labtx=simplefont.render("space = new instance", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 40))
		self.labtx=simplefont.render("q = close this window", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 60))
		self.labtx=simplefont.render("e = test sig protect 1", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 80))
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
		consolewrite("TEST: click")
	#similar to click, except it receves MOUSEBUTTONUP events that fall within widbox.
	def clickup(self, event):
		consolewrite("TEST: clickup")
	#keydown and keyup are given pygame KEYDOWN and KEYUP events.
	def keydown(self, event):
		consolewrite("TEST: Keydown")
		#print event.unicode
		if event.key==pygame.K_SPACE:
			self.newinstance=1
		if event.key==pygame.K_q:
			self.selfquit=1
		if event.key==pygame.K_e:
			self.testsigprotect1=1
	def keyup(self, event):
		consolewrite("TEST: Keyup")
	#close is called when the window is to be closed.
	def close(self):
		consolewrite("TEST: Window Close")
	#hostquit is called when the host program is going to quit.
	def hostquit(self):
		consolewrite("TEST: Host Program Quit")
	def sig(self):
		if self.newinstance==1:
			self.newinstance=0
			consolewrite("TEST: Sending mini tool launch signal")
			return (0, PLUGIN_testpkg_testwid(self.screensurf, 0))
		if self.testsigprotect1==1:
			self.testsigprotect1=0
			consolewrite("TEST: Testing Signal Protection on task closing.")
			return ("TASKMAN", 0, 0)
			
		if self.selfquit==1:
			self.selfquit=0
			consolewrite("TEST: Sending selfquit signal")
			return (1, 0)
		return
	def que(self, signal):
		return

#Refrence to class of plugin util
SDAPPLUGREF=PLUGIN_testpkg_testwid
#plugin execname
SDAPNAME="testpkg_testwid"
SDAPLABEL="Test Tool"
#plugin icon refrence (60 x 60 pixels is preferred) set to None for placeholder
SDAPICON="testtool.png"
#plugin directory (set to None if none)
SDAPDIR="testpkg.sdap"
#category ID: 0=main 1=Games, 2=Welcome, 3=Demos, 4=Mini Tools 5=Plugins (default, will be listed in plugins regardless) should be a list.
SDAPCAT=[4]