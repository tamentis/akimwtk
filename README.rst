akimwtk - Alex Kidd in Miracle World ToolKit
============================================

This intend to be a set of python script to access the state of the game
while playing. While the initial scripts will be aimed at gathering data, the
ultimate goal is to write a learning bot using genetic algorithms.

requirements
============
 - Dega 1.16-pre1
 - Python 2.5 (and dev headers/tools)

In order to compile pydega.so, you need to type::

    make pydega.so

If you are using a 64-bit architecture, add "-fPIC" to the OPTFLAGS variable
at the top of the Makefile and add Z80=z80jb to switch to the Mame Z80
core (no assembly).

memory.py
=========
This script is meant to be run from dega-1.16pre1. It will spawn the memory
editor with the current view of the level (blocks, money, etc.).


