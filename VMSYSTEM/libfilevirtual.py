import time
import copy
import sys
import os



#psudo virtual filesystem helper library for SBTCVM

validtypeext=["png", "jpg", "jpeg", "gif", "streg", "trom", "tasm", "txt", "md", "log", "dmp"]

def directorymask(pathstr, filestr):
	if ".git" in pathstr or ".git" in filestr:
		return 0
	else:
		return 1
	

def filevalid(filestr, pathlist):
	pathstr=os.path.join(*pathlist)
	pathjoin=os.path.join(pathstr, filestr)
	if os.path.isdir(pathjoin):
		return directorymask(pathstr, filestr)
	for ftype in validtypeext:
		if (filestr.lower()).endswith("." + ftype):
			return 1
	return 0

def isdir(filestr, pathlist):
	pathstr=os.path.join(*pathlist)
	pathjoin=os.path.join(pathstr, filestr)
	if os.path.isdir(pathjoin):
		return directorymask(pathstr, filestr)
	return 0

def diriterate(pathlist):
	pathlistret=sorted(os.listdir(os.path.join(*pathlist)), key=str.lower)
	if pathlist[0]=="." and len(pathlist)>1:
		pathlistret=[".."] + pathlistret
	return pathlistret


def dirlist(pathlist):
	retlist=[]
	retlist.extend([">>Directory Listing for: " + os.path.join(*pathlist)])
	for fname in diriterate(pathlist):
		if filevalid(fname, pathlist):
			if os.path.isdir(os.path.join(os.path.join(*pathlist), fname)):
				retlist.extend([" DIR | " + fname])
			else:
				retlist.extend(["     | " + fname])
	return retlist

def dir_cdup(pathlist):
	if pathlist[0]=="." and len(pathlist)>1:
		pathlist.remove(pathlist[(len(pathlist) -1)])
	return pathlist

def dir_cd(pathlist, dirstr):
	if dirstr=="..":
		return dir_cdup(pathlist)
	elif dirstr=="/":
		return ['.']
	elif os.path.isdir(os.path.join(os.path.join(*pathlist), dirstr)):
		pathlist.extend([dirstr])
		return pathlist
	return None