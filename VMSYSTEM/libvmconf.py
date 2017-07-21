#!/usr/bin/env python
import xml.etree.ElementTree as ET
import os
import sys
import time


if os.path.isfile(os.path.join("VMUSER", "CFG", "common.xml")):
	conftree = ET.parse(os.path.join("VMUSER", "CFG", "common.xml"))
	confroot = conftree.getroot()
elif os.path.isfile(os.path.join("VMSYSTEM", "CFG", "common.xml")):
	conftreedef = ET.parse(os.path.join("VMSYSTEM", "CFG", "common.xml"))
	confrootdef = conftreedef.getroot()
	makeconf=open(os.path.join("VMUSER", "CFG", "common.xml"), "w")
	conftreedef.write(makeconf)
	makeconf.close()
	conftree = ET.parse(os.path.join("VMUSER", "CFG", "common.xml"))
	confroot = conftree.getroot()
else:
	sys.exit("ERROR: libvmconf: UNABLE TO LOAD: common.xml")
	

def getconf(category, attrib):
	cattag=confroot.find(category)
	return cattag.attrib.get(attrib)
def setconf(category, attrib, value):
	cattag=confroot.find(category)
	cattag.set(attrib, value)
def saveconf():
	conftree.write(os.path.join("VMUSER", "CFG", "common.xml"))
def resetconf():
	if os.path.isfile(os.path.join("VMSYSTEM", "CFG", "common.xml")):
		global conftree
		global confroot
		conftree = ET.parse(os.path.join("VMSYSTEM", "CFG", "common.xml"))
		confroot = conftree.getroot()
	else:
		sys.exit("ERROR: libvmconf: UNABLE TO LOAD: common.xml")