# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003-2004 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

# TextScreen.py - display Loading screen

###################################################

import GemRB
from GUIDefines import *
from GUICommon import GameWindow

TextScreen = None
TextArea = None
Chapter = 0
TableName = ""

def StartTextScreen ():
	global TextScreen, TextArea, Chapter, TableName

	GemRB.LoadWindowPack ("GUICHAP", 640, 480)
	TableName = GemRB.GetGameString (STR_LOADMOS)

	#if there is no preset loadpic, try to determine it from the chapter
	if TableName == "":
		Chapter = GemRB.GetGameVar ("CHAPTER") & 0x7fffffff
		TableName = "CHPTXT"+str(Chapter)
		#set ID according to the Chapter?

	print "TableName:", TableName
	Table = GemRB.LoadTableObject (TableName)
	LoadPic = Table.GetValue (-1, -1)
	print "Loadpic:", LoadPic
	TextScreen = GemRB.LoadWindowObject (62)
	TextScreen.SetFrame ()
	if LoadPic != "":
		TextScreen.SetPicture (LoadPic)
	TextArea = TextScreen.GetControl (2)
	TextArea.SetFlags (IE_GUI_TEXTAREA_SMOOTHSCROLL)
	TextArea.SetEvent (IE_GUI_TEXTAREA_OUT_OF_TEXT, "FeedScroll")

	#done
	Button=TextScreen.GetControl (0)
	Button.SetText (11973)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "EndTextScreen")
	Button.SetFlags (IE_GUI_BUTTON_DEFAULT|IE_GUI_BUTTON_CANCEL,OP_OR)

	#replay
	Button=TextScreen.GetControl (3)
	Button.SetText (16510)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "ReplayTextScreen")

	GemRB.HideGUI ()
	GameWindow.SetVisible(WINDOW_INVISIBLE) #removing the gamecontrol screen

	TextScreen.SetVisible (WINDOW_VISIBLE)
	TextArea.Rewind (300)
	GemRB.DisplayString (17556, 0xff0000)
	GemRB.GamePause (1, 1)
	return

def FeedScroll ():
	global TextScreen, TextArea, Chapter, TableName

	#this is a rather primitive selection but works for the games
	Table = GemRB.LoadTableObject (TableName)
	Value = Table.GetValue (0, 1)
	print "Value", Value
	if Value == "REPUTATION":
		line = 2
	else:
		line = 1
	Value = Table.GetValue (line, 1)

	TextArea.Append (Value, -1, 6)
	return

def ReplayTextScreen ():
	global TextScreen, TextArea

	TextArea.SetEvent (IE_GUI_TEXTAREA_OUT_OF_TEXT, "FeedScroll")
	TextArea.Rewind (300)
	return

def EndTextScreen ():
	global TextScreen

	TextScreen.SetVisible (WINDOW_INVISIBLE)
	if TextScreen:
		TextScreen.Unload ()
	GameWindow.SetVisible(WINDOW_VISIBLE) #enabling gamecontrol screen
	GemRB.UnhideGUI ()
	GemRB.GamePause (0, 1)
	return
