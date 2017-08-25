#!/usr/bin/env python
import os
#used by list function to search for important files.
pathlist=[(os.path.join("VMSYSTEM", "ROMS")), "VMSYSTEM", "ROMS", "VMUSER"]
keyftypes=["streg", "trom", "tasm"]

listhelptext='''
The main uses of list are to list important file types like troms, SBTCVM
assembly files, and so on, that SBTCVM can see without explicit paths.
list types : list known important file type keywords
list paths : list paths searched by sbtcvm for important file types
list [type] : look for the specified type.'''

helptext='''Commands: 
run [arguments]   : SBTCVM command line launcher. use "run help" for help.
asm [arguments]   : SBTCVM assembler. "asm help" for help.
gfx [arguments]   : SBTCVM graphics toolkit. use "gfx help" for help.
tools (t) [arguments] : SBTCVM tools launcher. use "t help" for help.
mainmenu          : Start SBTCVM's main menu.
list [type]       : use "list help" for help on the list command.
help              : this text
version           : version info
about             : about info
quit              : quit SBTCVM command shell

math commands:
add    : add two balanced ternary integers (separated by a space)
sub    : subtract two balanced ternary integers (separated by a space)
div    : divide two balanced ternary integers (separated by a space)
mul    : multiply two balanced ternary integers (separated by a space)
btdec  : convert a balanced ternary integer to decimal
decbt  : convert a decimal integer to balanced ternary
invert : invert a balanced ternary integer
mpi    : calculate the Max Positive Integer for a given number of trits
mni    : calculate the Max Negative Integer for a given number of trits
mcv    : calculate the Max Combinations Value for a given number of trits
'''

abouttext='''SBTCVM MK2-CS command shell
This program uses a combination of short names for SBTCVM command line
utilities and special commands to aid in SBTCVM usage.

v2.0.3

Copyright (c) 2016-2017 Thomas Leathers and Contributors

  SBTCVM MK2-CS command shell is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM MK2-CS command shell is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM MK2-CS command shell. If not, see <http://www.gnu.org/licenses/>
'''

versiontext="SBTCVM MK2-CS Command Shell v2.0.3"
