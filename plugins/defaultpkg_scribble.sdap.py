
#important notice: please keep variables inside class except for (see below)
#notice: these plugins will be in the "plugins" directory in accordance to the plugin system.
#Plugin classes should be prefixed with "PLUGIN_" the text following such should match SDAPNAME!


class PLUGIN_defaultpkg_scribble:
	def __init__(self, screensurf, windoworder, xpos=0, ypos=0, argument=None):
		#screensurf is the surface to blit the window to
		self.screensurf=screensurf
		#wo is a sorting variable used to sort the windows in a list
		self.wo=windoworder
		#title is the name of the window
		self.title="Scribble"
		#taskid is set automatically
		self.taskid=0
		
		self.widx=324
		self.widy=283
		self.x=xpos
		self.y=ypos
		self.widsurf=pygame.Surface((self.widx, self.widy)).convert(self.screensurf)
		self.widsurf.fill(framebg)
		self.labtx=simplefont.render("click left box or use a,s,d to cycle color [27 colors]", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 0))
		self.labtx=simplefont.render("click the right box or use c to change pen size", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 20))
		self.labtx=simplefont.render("click inside this window to begin.", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 40))
		self.labtx=simplefont.render("z is undo, x is fill", True, frametext, framebg)
		self.widsurf.blit(self.labtx, (0, 60))
		self.paintsurf=pygame.Surface((self.widx, self.widy-40)).convert(self.widsurf)
		self.paintsurf.fill((255, 255, 255))
		self.paintsurfbak=self.paintsurf.copy()
		self.paintrect=self.paintsurf.get_rect()
		self.paintrect.x = (self.x)
		self.paintrect.y = (self.y)
		self.pensize=1
		self.color1rect=pygame.Rect(self.x, (self.y + self.widy - 38), 30, 30)
		self.colorRrect=pygame.Rect(self.x + 96, (self.y + self.widy - 38), 50, 30)
		self.colorGrect=pygame.Rect(self.x + 148, (self.y + self.widy - 38), 50, 30)
		self.colorBrect=pygame.Rect(self.x + 200 , (self.y + self.widy - 38), 50, 30)
		#self.sizesmall=pygame.Rect(self.x + 30, (self.y + self.widy - 40), self.pensize, self.pensize)
		self.sizerect=pygame.Rect(self.x + 32, (self.y + self.widy - 38), 30, 30)
		self.newrect=pygame.Rect(self.x + 64, (self.y + self.widy - 38), 30, 30)
		self.penlist=[1, 2, 3, 4, 5, 7, 9, 10, 15, 20, 30]
		self.penindex=0
		self.colorr=0
		self.colorb=0
		self.colorg=0
		self.frametoup=getframes(self.x, self.y, self.widsurf, resizebar=1)
		self.scrib=0
		#these rects are needed
		#frame close button rect
		self.closerect=self.frametoup[2]
		#rect of window content
		self.widbox=self.frametoup[0]
		#frame rect
		self.framerect=self.frametoup[1]
		self.firstclick=1
		self.redraw=0
		self.labtx2=simplefont.render("size", True, framebg, frametext)
		self.labtx3=simplefont.render("RD (a)", True, framebg, frametext)
		self.labtx4=simplefont.render("GN (s)", True, framebg, frametext)
		self.labtx5=simplefont.render("BL (d)", True, framebg, frametext)
	def render(self):
		self.scribblecolor=(self.colorr, self.colorg, self.colorb)
		if self.firstclick==2:
			self.firstclick=0
			self.widsurf.blit(self.paintsurf, (0, 0))
		if self.redraw==1:
			self.redraw=0
			self.widsurf.blit(self.paintsurf, (0, 0))
		if self.scrib==1:
			self.dx=self.sx
			self.dy=self.sy
			self.mpos=pygame.mouse.get_pos()
			self.sx=(self.mpos[0] - self.x)
			self.sy=(self.mpos[1] - self.y)
			pygame.draw.line(self.paintsurf, self.scribblecolor, (self.dx, self.dy), (self.sx, self.sy), self.penlist[self.penindex])
			self.widsurf.blit(self.paintsurf, (0, 0))
		
		#self.labtx=simplefont.render("window order: " + str(self.wo), True, frametext, framebg)
		#self.widsurf.blit(self.labtx, (0, 0))
		drawframe(self.framerect, self.closerect, self.widbox, self.widsurf, self.screensurf, self.title, self.wo)
		pygame.draw.rect(self.screensurf, self.scribblecolor, self.color1rect, 0)
		pygame.draw.rect(self.screensurf, framediv, self.color1rect, 1)
		pygame.draw.rect(self.screensurf, frametext, self.sizerect, 0)
		pygame.draw.rect(self.screensurf, frametext, self.newrect, 0)
		pygame.draw.rect(self.screensurf, (self.colorr, 0, 0), self.colorRrect, 0)
		pygame.draw.rect(self.screensurf, (0, self.colorg, 0), self.colorGrect, 0)
		pygame.draw.rect(self.screensurf, (0, 0, self.colorb), self.colorBrect, 0)
		
		pygame.draw.rect(self.screensurf, (255, 0, 0), self.colorRrect, 1)
		pygame.draw.rect(self.screensurf, (0, 255, 0), self.colorGrect, 1)
		pygame.draw.rect(self.screensurf, (0, 0, 255), self.colorBrect, 1)
		self.labtx=simplefont.render(str(self.penlist[self.penindex]), True, framebg, frametext)
		self.screensurf.blit(self.labtx, (self.x + 32, (self.y + self.widy - 38)))
		
		self.screensurf.blit(self.labtx2, (self.x + 64, (self.y + self.widy - 38)))
		self.screensurf.blit(self.labtx3, (self.x + 96 + 2, (self.y + 2 + self.widy - 38)))
		self.screensurf.blit(self.labtx4, (self.x + 148 + 2, (self.y + 2 + self.widy - 38)))
		self.screensurf.blit(self.labtx5, (self.x + 200 + 2, (self.y + 2 + self.widy - 38)))
	def movet(self, xoff, yoff):
		self.x -= xoff
		self.y -= yoff
		self.frametoup=getframes(self.x, self.y, self.widsurf, resizebar=1)
		self.closerect=self.frametoup[2]
		self.widbox=self.frametoup[0]
		self.framerect=self.frametoup[1]
		self.paintrect.x = (self.x)
		self.paintrect.y = (self.y)
		self.color1rect=pygame.Rect(self.x, (self.y + self.widy - 38), 30, 30)
		self.colorRrect=pygame.Rect(self.x + 96, (self.y + self.widy - 38), 50, 30)
		self.colorGrect=pygame.Rect(self.x + 148, (self.y + self.widy - 38), 50, 30)
		self.colorBrect=pygame.Rect(self.x + 200 , (self.y + self.widy - 38), 50, 30)
		self.sizerect=pygame.Rect(self.x + 32, (self.y + self.widy - 38), 30, 30)
		self.newrect=pygame.Rect(self.x + 64, (self.y + self.widy - 38), 30, 30)
	def resizet(self, xoff, yoff):
		#manipulate your window surface x and y sizes like so: if want only x or only y, manipulate only that.
		self.widx -= xoff
		self.widy -= yoff
		#check the size to ensure it isn't too small (or invalid)
		if self.widx<140:
			self.widx=140
		if self.widy<140:
			self.widy=140
		self.redraw=1
		self.color1rect=pygame.Rect(self.x, (self.y + self.widy - 38), 30, 30)
		self.colorRrect=pygame.Rect(self.x + 96, (self.y + self.widy - 38), 50, 30)
		self.colorGrect=pygame.Rect(self.x + 148, (self.y + self.widy - 38), 50, 30)
		self.colorBrect=pygame.Rect(self.x + 200 , (self.y + self.widy - 38), 50, 30)
		#self.sizesmall=pygame.Rect(self.x + 30, (self.y + self.widy - 40), self.pensize, self.pensize)
		self.sizerect=pygame.Rect(self.x + 32, (self.y + self.widy - 38), 30, 30)
		#redefine your widsurf, and refresh rects, also do any needed sdap-specific operations.
		self.widsurf=pygame.Surface((self.widx, self.widy)).convert(self.screensurf)
		self.widsurf.fill(framebg)
		self.newrect=pygame.Rect(self.x + 64, (self.y + self.widy - 38), 30, 30)
		#TO SHOW THE RESIZEBAR AT THE BOTTOM OF WINDOW YOU MUST SPECIFY resizebar=1 !!!
		self.frametoup=getframes(self.x, self.y, self.widsurf, resizebar=1)
		self.closerect=self.frametoup[2]
		self.widbox=self.frametoup[0]
		self.framerect=self.frametoup[1]
	def newpaintsurf(self):
		self.paintsurf2=pygame.Surface((self.widx, self.widy-40)).convert(self.widsurf)
		self.paintsurf2.fill((255, 255, 255))
		self.paintsurf2.blit(self.paintsurf, (0, 0))
		self.paintsurf=self.paintsurf2
		self.paintrect=self.paintsurf.get_rect()
		self.paintrect.x = (self.x)
		self.paintrect.y = (self.y)
		self.redraw=1
	def click(self, event):
		if self.firstclick==1:
			self.firstclick=2
		elif self.newrect.collidepoint(event.pos) == 1:
			self.newpaintsurf()
		elif self.sizerect.collidepoint(event.pos) == 1 and (event.button==1 or event.button==4):
			if self.penindex==(len(self.penlist) - 1):
				self.penindex=0
			else:
				self.penindex += 1
		elif self.sizerect.collidepoint(event.pos) == 1 and event.button==5:
			if self.penindex==0:
				self.penindex=len(self.penlist) - 1
			else:
				self.penindex -= 1
		elif self.colorRrect.collidepoint(event.pos) == 1 and (event.button==1 or event.button==4):
			if self.colorr==0:
				self.colorr=127
			elif self.colorr==127:
				self.colorr=255
			elif self.colorr==255:
				self.colorr=0
		elif self.colorGrect.collidepoint(event.pos) == 1 and (event.button==1 or event.button==4):
			if self.colorg==0:
				self.colorg=127
			elif self.colorg==127:
				self.colorg=255
			elif self.colorg==255:
				self.colorg=0
		elif self.colorBrect.collidepoint(event.pos) == 1 and (event.button==1 or event.button==4):
			if self.colorb==0:
				self.colorb=127
			elif self.colorb==127:
				self.colorb=255
			elif self.colorb==255:
				self.colorb=0
		elif self.colorBrect.collidepoint(event.pos) == 1 and event.button==5:
			if self.colorb==255:
				self.colorb=127
			elif self.colorb==127:
				self.colorb=0
			elif self.colorb==0:
				self.colorb=255
		elif self.colorRrect.collidepoint(event.pos) == 1 and event.button==5:
			if self.colorr==255:
				self.colorr=127
			elif self.colorr==127:
				self.colorr=0
			elif self.colorr==0:
				self.colorr=255
		elif self.colorGrect.collidepoint(event.pos) == 1 and event.button==5:
			if self.colorg==255:
				self.colorg=127
			elif self.colorg==127:
				self.colorg=0
			elif self.colorg==0:
				self.colorg=255
		elif self.color1rect.collidepoint(event.pos) == 1:
			if self.colorr==0:
				self.colorr=127
			elif self.colorr==127:
				self.colorr=255
			elif self.colorr==255:
				self.colorr=0
				if self.colorg==0:
					self.colorg=127
				elif self.colorg==127:
					self.colorg=255
				elif self.colorg==255:
					self.colorg=0
					if self.colorb==0:
						self.colorb=127
					elif self.colorb==127:
						self.colorb=255
					elif self.colorb==255:
						self.colorb=0
		elif self.paintrect.collidepoint(event.pos) == 1:
			self.paintsurfbak=self.paintsurf.copy()
			self.sx=(event.pos[0] - self.x)
			self.sy=(event.pos[1] - self.y)
			self.scrib=1
	def clickup(self, event):
		self.scrib=0
	def keydown(self, event):
		
		if event.key==pygame.K_a:
			if self.colorr==0:
				self.colorr=127
			elif self.colorr==127:
				self.colorr=255
			elif self.colorr==255:
				self.colorr=0
		if event.key==pygame.K_s:
			if self.colorg==0:
				self.colorg=127
			elif self.colorg==127:
				self.colorg=255
			elif self.colorg==255:
				self.colorg=0
		if event.key==pygame.K_d:
			if self.colorb==0:
				self.colorb=127
			elif self.colorb==127:
				self.colorb=255
			elif self.colorb==255:
				self.colorb=0
		if event.key==pygame.K_z and self.firstclick==0:
			self.paintsurfq=self.paintsurfbak
			self.paintsurfbak=self.paintsurf
			self.paintsurf=self.paintsurfq
			self.redraw=1
		if event.key==pygame.K_x and self.firstclick==0:
			self.paintsurfbak=self.paintsurf.copy()
			self.scribblecolor=(self.colorr, self.colorg, self.colorb)
			self.paintsurf.fill(self.scribblecolor)
			self.redraw=1
		if event.key==pygame.K_c:
			if self.penindex==(len(self.penlist) - 1):
				self.penindex=0
			else:
				self.penindex += 1
	def keyup(self, event):
		return
	def close(self):
		return
	def hostquit(self):
		return
	def sig(self):
		return
	def que(self, signal):
		return



#Refrence to class of plugin util
SDAPPLUGREF=PLUGIN_defaultpkg_scribble
#plugin execname
SDAPNAME="defaultpkg_scribble"
SDAPLABEL="Scribble"
#plugin icon refrence (60 x 60 pixels is preferred) set to None for placeholder
SDAPICON="scribble.png"
#plugin directory (set to None if none)
SDAPDIR="defaultpkg.sdap"
#category ID: 0=main 1=Games, 2=Welcome, 3=Demos, 4=Mini Tools 5=Plugins (default, will be listed in plugins regardless) should be a list.
SDAPCAT=[4]