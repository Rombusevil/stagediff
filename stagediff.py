#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Iber Parodi Siri'

"""
    This file is part of stagediff.

    stagediff is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    stagediff is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with stagediff.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys, os
from picker.picker import *
from subprocess import Popen, PIPE

args = sys.argv
if len(args) is not 2:
    print("")
    print("Supply path of git project")
    print("Examples: ")
    print("  stagediff .")
    print("  stagediff /home/user/proj")
    print("")
    sys.exit()

# Changes this script's working directory to the one in the first argument
path = str(args[1])
if path is not '.':
    os.chdir(path)
else:
    os.getcwd()

# Run the command that prints the list of commited files that are modified:
#       git status --porcelain | grep " M" | cut -d" " -f3
gitSts  = Popen(["git", "status", "--porcelain"], stdout =PIPE)
pending = Popen(["grep"," M"], stdin =gitSts.stdout, stdout=PIPE)
pending = Popen(["cut", "-d", " ", "-f3"], stdin =pending.stdout, stdout=PIPE)

# Create a list with the output of the command
list = pending.stdout.read().splitlines()

if list:
    selectedItems = None
    cursorPos = 0

    running = True
    while running:
        # This is blocking, launch the curses interface
        p = Picker( title = 'Modified files',
                    footer="Right arrow = show diff, Space = stage for commit, Enter = commit, q = quit",
                    options= list,
                    options_selected = selectedItems,
                    cursor_pos = cursorPos)
        opts = p.getSelected()

        if opts is not False:
            selectedItems = opts["checked"] # Store the list of checked items

            # RIGHT Key pressed, lauch git diff then
            if opts["diff"] is not None:
                cursorPos = opts["diff"] # Store cursor pos to restore
                fileToDiff = list[opts["diff"]]

                # This is blocking, launch vimdiff
                # I'm using git d for using vimdiff as a difftool
                diff = Popen(["git d "+str(fileToDiff)], shell=True)
                diff.wait()

            # ENTER Key pressed
            else:
                if opts["checked"]:
                    files = ' '.join(opts["checked"])

                    # stage selected files to commit
                    add = Popen(["git add "+files], shell=True)
                    add.wait()

                    # commit changes
                    commit = Popen(["git commit "], shell=True)
                    commit.wait()
                else:
                    print("Nothing to do here ...")
                running = False
        else:
            # Q was presses, so we quit
            running = False
else:
    print("Nothing to do here ...")
