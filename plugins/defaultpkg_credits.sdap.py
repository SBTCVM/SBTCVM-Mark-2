

#important notice: please keep variables inside class except for (see below)
#notice: these plugins will be in the "plugins" directory in accordance to the plugin system.
#Plugin classes should be prefixed with "PLUGIN_" the text following such should match SDAPNAME!
class PLUGIN_defaultpkg_qcredscroll:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="Credits"
		#taskid is set automatically
		self.taskid=0
		self.pixjmp=14
		self.widx=600
		self.widy=370
		#x and y are required.
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy))
		self.widsurf.fill(libthemeconf.creditbg)
		self.texttable=texttable=["","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
		self.frametoup=getframes(self.x, self.y, self.widsurf)
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
		self.abt = open(os.path.join("VMSYSTEM", "L_CREDIT.TXT"))
		self.scrollsurf=pygame.Surface((600, 410))
		self.scrollmask=pygame.Surface((600, 370))
		self.scrollsurfyaw=-20
		self.scrollmaskyaw=0
		self.scrollsurfwid=0
		self.slide=0
		self.GFXLOGOCRED=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'GFXLOGO-CAT.png')).convert()
		self.sbtccat=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'SBTCCAT34.png')).convert()
		self.slidecnt=0
		self.hbar=pygame.Surface((190, 4))
		self.hbar.fill(libthemeconf.credittext)
	def render(self):
		if self.slide==0:
			self.flid=self.abt.readline()
			self.flid=self.flid.replace('\n', '')
			if self.flid=="-<END>-":
				self.abt.seek(0)
				self.flid=self.abt.readline()
				self.flid=self.flid.replace('\n', '')
			self.texttable.pop(0)
			self.texttable.append(self.flid)
			
			#self.slidecnt=0
			self.pixcnt1=0
			
			self.scrollmaskyaw=0
			self.scrollsurfyaw=-20
			self.scrollsurf.fill(libthemeconf.creditbg)
			#screensurf.fill((255, 255, 255))
			for self.qlid in self.texttable:
				if self.qlid=="-<GFXLOGO>-":
					self.abttextbox=self.GFXLOGOCRED.get_rect()
					self.abttextbox.centerx=self.scrollsurf.get_rect().centerx
					self.abttextbox.y=self.pixcnt1
					self.scrollsurf.blit(self.GFXLOGOCRED, self.abttextbox)
				elif self.qlid=="-<HBAR>-":
					self.abttextbox=self.hbar.get_rect()
					self.abttextbox.centerx=self.scrollsurf.get_rect().centerx
					self.abttextbox.y=self.pixcnt1
					self.scrollsurf.blit(self.hbar, self.abttextbox)
				elif self.qlid=="-<SBTCCAT>-":
					self.abttextbox=self.sbtccat.get_rect()
					self.abttextbox.centerx=self.scrollsurf.get_rect().centerx
					self.abttextbox.y=self.pixcnt1
					self.scrollsurf.blit(self.sbtccat, self.abttextbox)
				elif self.qlid!="":
					self.abttext=simplefont.render(self.qlid, True, libthemeconf.credittext, libthemeconf.creditbg)
					self.abttextbox=self.abttext.get_rect()
					self.abttextbox.centerx=self.scrollsurf.get_rect().centerx
					self.abttextbox.y=self.pixcnt1
					self.scrollsurf.blit(self.abttext, self.abttextbox)
				self.pixcnt1 += self.pixjmp
				self.slide=1
		if self.slide==1:
			if self.slidecnt==14:
				self.slidecnt=0
				self.slide=0
				self.pixcnt1=0
			else:
				
				self.widsurf.blit(self.scrollsurf, (0, self.scrollsurfyaw))
				#self.widsurf.blit(self.scrollmask, (self.scrollsurfwid, self.scrollmaskyaw))
				self.scrollsurfyaw -= 1
				self.slidecnt += 1
			#time.sleep(.05)
			#pygame.display.update()
		#scrollmask.blit(scrollsurf, (0, scrollsurfyaw))
		#widsurf.blit(scrollmask, (scrollsurfwid, scrollmaskyaw))
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
		return
	def que(self, signal):
		return









#Refrence to class of plugin util
SDAPPLUGREF=PLUGIN_defaultpkg_qcredscroll
#plugin execname
SDAPNAME="defaultpkg_qcredscroll"
SDAPLABEL="Credits"
#plugin icon refrence (60 x 60 pixels is preferred) set to None for placeholder
SDAPICON="credits.png"
#plugin directory (set to None if none)
SDAPDIR="defaultpkg.sdap"
#category ID: 0=main 1=Games, 2=Welcome, 3=Demos, 4=Mini Tools 5=Plugins (default, will be listed in plugins regardless) should be a list.
SDAPCAT=[0, 2, 4]