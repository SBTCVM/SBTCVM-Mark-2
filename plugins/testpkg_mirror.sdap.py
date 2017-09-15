
#important notice: please keep variables inside class except for (see below)
#notice: these plugins will be in the "plugins" directory in accordance to the plugin system.
#Plugin classes should be prefixed with "PLUGIN_" the text following such should match SDAPNAME!
class PLUGIN_testpkg_mirror:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="mirror"
		#taskid is set automatically
		self.taskid=0
		self.widx=140
		self.widy=140
		self.argument=argument
		#x and y are required.
		self.x=xpos
		self.y=ypos
		self.mx=0
		self.my=0
		self.widsurf=pygame.Surface((self.widx, self.widy))
		self.widsurf.fill(framebg)
		consolewrite("mirror: running")
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		if self.argument==None:
			self.newinstance=1
			self.labtx=simplefont.render("point mirror", True, frametext, framebg)
		else:
			self.newinstance=0
			self.labtx=simplefont.render("point origin", True, frametext, framebg)
		#frame rect
		self.framerect=self.frametoup[1]
		self.selfquit=0
		self.testsigprotect1=0
	def render(self):
		if self.argument!=None:
			self.widsurf.fill(framebg)
			self.widsurf.blit(self.labtx, (0, 0))
			self.mpos=pygame.mouse.get_pos()
			self.mx=(self.mpos[0] - self.x)
			self.my=(self.mpos[1] - self.y)
			self.argument.que([0, self.mx, self.my])
			pygame.draw.line(self.widsurf, frametext, (70, 70), (self.mx, self.my))
		else:
			self.widsurf.fill(framebg)
			self.widsurf.blit(self.labtx, (0, 0))
			pygame.draw.line(self.widsurf, frametext, (70, 70), (self.mx, self.my))
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title)
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
		if self.newinstance==1:
			self.newinstance=0
			self.otherinst=PLUGIN_testpkg_mirror(self.screensurf, 0, argument=self)
			return (0, self.otherinst)
		#return
	def que(self, signal):
		if self.argument==None:
			if signal[0]==0:
				self.mx=signal[1]
				self.my=signal[2]
#Refrence to class of plugin util
SDAPPLUGREF=PLUGIN_testpkg_mirror
#plugin execname
SDAPNAME="testpkg_mirror"
SDAPLABEL="mirror test"
#plugin icon refrence (60 x 60 pixels is preferred) set to None for placeholder
SDAPICON="test.png"
#plugin directory (set to None if none)
SDAPDIR="testpkg.sdap"
#category ID: 0=main 1=Games, 2=Welcome, 3=Demos, 4=Mini Tools 5=Plugins (default, will be listed in plugins regardless) should be a list.
SDAPCAT=[4]

