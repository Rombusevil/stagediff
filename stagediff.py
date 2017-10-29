#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import sys
import os
from subprocess import Popen, PIPE
from picker.picker import *

__author__ = 'Iber Parodi Siri'


def change_dir(path):
    """ Changes current working directory to the specified """
    if path is not '.':
        os.chdir(path)
    else:
        os.getcwd()

def process_args():
    """ Validates number of args and uses the first arg to change directories """
    args = sys.argv
    if len(args) is not 2:
        show_help()
    else:
        # Changes this script's working directory to the one in the first argument
        change_dir(str(args[1]))

def show_help():
    """ Prints help text """
    print ""
    print "Supply path of git project"
    print "Examples: "
    print "  stagediff ."
    print "  stagediff /home/user/proj"
    print ""
    sys.exit()

def get_git_status():
    """ returns a list with the 'git status --porcelain' output """
    gitstatus = Popen(["git", "status", "--porcelain"], stdout=PIPE)

    # Create a list with the output of the command
    return gitstatus.stdout.read().splitlines()

def start_running():
    """ Main function """
    files = get_git_status()

    if files:
        selected_items = None
        cursor_pos = 0

        running = True
        while running:
            # This is blocking, launch the curses interface
            picker = Picker(title='Git status',
                            footer="'->' diff, '<-' revert, 'space' stage, "
                            +"'enter' commit, 'q' quit",
                            options=files,
                            options_selected=selected_items,
                            cursor_pos=cursor_pos)
            opts = picker.getSelected()

            if opts is not False:
                selected_items = opts["checked"] # Store the list of checked items

                if opts["highlighted"] is not None:
                    cursor_pos = opts["highlighted"] # Store cursor pos to restore
                    raw_line = files[opts["highlighted"]]
                    is_modified = raw_line[0:2] == ' M'
                    is_untracked = raw_line[0:2] == '??'
                    highlighted_file = raw_line[3:].split(" ")[0]

                    # LEFT key pressed, reverting highlighted file
                    if opts["revert"] is True and not is_untracked:
                        print "REVERTING..."
                        confirm = raw_input("Revert all changes to "
                                            +str(highlighted_file)+"? [y/n]")
                        if confirm == 'y':
                            cmd = Popen(["git checkout -- "+str(highlighted_file)], shell=True)
                            cmd.wait()

                    # RIGHT Key pressed, lauch git diff then (only if the file to diff was modified)
                    elif is_modified:
                        # This is blocking, launch confiured diff tool
                        # I'm using git d for using vimdiff as a difftool
                        diff = Popen(["git d "+str(highlighted_file)], shell=True)
                        diff.wait()

                # ENTER Key pressed
                elif opts["checked"]:
                    if opts["commit"] is True:
                        files = ' '.join([e[3:] for e in opts["checked"]])

                        # stage selected files to commit
                        add = Popen(["git add "+files], shell=True)
                        add.wait()

                        # commit changes
                        commit = Popen(["git commit "], shell=True)
                        commit.wait()
                        running = False
                else:
                    print "Nothing to do here ..."
            else:
                # Q was pressed, so we quit
                running = False
    else:
        print "Nothing to do here ..."



process_args()
start_running()
