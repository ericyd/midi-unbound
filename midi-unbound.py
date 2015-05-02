# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #
#	
#	PROGRAM INFORMATION:
#	====================
#	TITLE:		MIDI Unbound
#	AUTHOR:		Eric Dauenhauer
#	VERSION:	1.0
#	COPYRIGHT:	Copyright 2014 Eric Dauenhauer
#	LICENSE:	GNU GPL License (see gpl.txt in main directory)
#
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#
# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #



#############################
#
#	Load necessary modules
#
#############################
import os
import sys

#if os.name == 'nt':
#	pass #windows
#else:
#	pass #other

try:
	import wx
	import wx._core
	if os.name == 'nt':
		import wx.activex
	wx_loaded = True
except ImportError:
	print ('You need the wxPython module for this program (its the GUI toolkit).\nGo to http://wiki.wxpython.org/How%20to%20install%20wxPython for how to install this on your system\n\n')
	wx_loaded = False

try:
	import autopy		# enables text entry
	import autopy.key
	autopy_loaded = True
except ImportError:
	if wx_loaded == True:
		autowx = wx.App()
		wx.MessageBox('You need the autopy module for this program. \n To install on Windows, go to\n\n      https://pypi.python.org/pypi/autopy/.\n\nFor other OS, simply run:\n\n      easy_install autopy', 'Autopy Import Error', wx.OK)
	else:
		print ('You need the autopy module for this program. \nTo install on Windows, go to \nhttps://pypi.python.org/pypi/autopy/.\nFor other OS, simply run: \neasy_install autopy\n\n')
	autopy_loaded = False

try:
	import mido
	if os.name == 'nt':
		import mido.backends.pygame
		from pygame import Color
		midobackend = mido.Backend('mido.backends.pygame')
	else:
		import mido.backends.portmidi
		midobackend = mido.Backend('mido.backends.portmidi')
	mido_loaded = True
except ImportError:
	if wx_loaded == True:
		midowx = wx.App()
		wx.MessageBox('You need the mido module for this program. \nTo install with pip, simply run: pip install mido. \nOtherwise, source downloads are available here:\nhttps://pypi.python.org/pypi/mido/1.1.6#downloads\nor here:\nhttps://github.com/olemb/mido/', 'Mido Import Error', wx.OK)
	else:
		print ('You need the mido module for this program. \nTo install with pip, simply run: pip install mido. \nOtherwise, source downloads are available here:\nhttps://pypi.python.org/pypi/mido/1.1.6#downloads\nor here:\nhttps://github.com/olemb/mido/\n\n')
	mido_loaded = False

import subprocess 	# enables commands to be processed
import time
import threading

try:
	import lxml.etree as ET
	lxml_loaded = True
except ImportError:
	import xml.etree.ElementTree as ET
	lxml_loaded = False

#############################
#
#	Set Global Variables
#
#############################

inport = 'default'
NewRowList = []
numrows = 5	
going = True
mgoing = True # for MIDI capture

midiInputList = midobackend.get_input_names()
midiOpenList = [midobackend.open_input(name) for name in midobackend.get_input_names()]


keyMap = {
	wx.WXK_BACK : "<BACK>",
	wx.WXK_TAB : "<TAB>",
	wx.WXK_RETURN : "<RETURN>",
	wx.WXK_ESCAPE : "<ESCAPE>",
	wx.WXK_SPACE : "<SPACE>",
	wx.WXK_DELETE : "<DELETE>",
	wx.WXK_START : "<START>",
	wx.WXK_LBUTTON : "<LBUTTON>",
	wx.WXK_RBUTTON : "<RBUTTON>",
	wx.WXK_CANCEL : "<CANCEL>",
	wx.WXK_MBUTTON : "<MBUTTON>",
	wx.WXK_CLEAR : "<CLEAR>",
	wx.WXK_SHIFT : "<SHIFT>",
	wx.WXK_ALT : "<ALT>",
	wx.WXK_MENU : "<MENU>",
	wx.WXK_PAUSE : "<PAUSE>",
	wx.WXK_CAPITAL : "<CAPSLOCK>",
	#wx.WXK_PRIOR : "<PRIOR>",
	#wx.WXK_NEXT : "<NEXT>",
	wx.WXK_END : "<END>",
	wx.WXK_HOME : "<HOME>",
	wx.WXK_LEFT : "<LEFT>",
	wx.WXK_UP : "<UP>",
	wx.WXK_RIGHT : "<RIGHT>",
	wx.WXK_DOWN : "<DOWN>",
	wx.WXK_SELECT : "<SELECT>",
	wx.WXK_PRINT : "<PRINT>",
	wx.WXK_EXECUTE : "<EXECUTE>",
	wx.WXK_SNAPSHOT : "<SNAPSHOT>",
	wx.WXK_INSERT : "<INSERT>",
	wx.WXK_HELP : "<HELP>",
	wx.WXK_NUMPAD0 : "<NUMPAD0>",
	wx.WXK_NUMPAD1 : "<NUMPAD1>",
	wx.WXK_NUMPAD2 : "<NUMPAD2>",
	wx.WXK_NUMPAD3 : "<NUMPAD3>",
	wx.WXK_NUMPAD4 : "<NUMPAD4>",
	wx.WXK_NUMPAD5 : "<NUMPAD5>",
	wx.WXK_NUMPAD6 : "<NUMPAD6>",
	wx.WXK_NUMPAD7 : "<NUMPAD7>",
	wx.WXK_NUMPAD8 : "<NUMPAD8>",
	wx.WXK_NUMPAD9 : "<NUMPAD9>",
	wx.WXK_MULTIPLY : "<MULTIPLY>",
	wx.WXK_ADD : "<ADD>",
	wx.WXK_SEPARATOR : "<SEPARATOR>",
	wx.WXK_SUBTRACT : "<SUBTRACT>",
	wx.WXK_DECIMAL : "<DECIMAL>",
	wx.WXK_DIVIDE : "<DIVIDE>",
	wx.WXK_F1 : "<F1>",
	wx.WXK_F2 : "<F2>",
	wx.WXK_F3 : "<F3>",
	wx.WXK_F4 : "<F4>",
	wx.WXK_F5 : "<F5>",
	wx.WXK_F6 : "<F6>",
	wx.WXK_F7 : "<F7>",
	wx.WXK_F8 : "<F8>",
	wx.WXK_F9 : "<F9>",
	wx.WXK_F10 : "<F10>",
	wx.WXK_F11 : "<F11>",
	wx.WXK_F12 : "<F12>",
	wx.WXK_F13 : "<F13>",
	wx.WXK_F14 : "<F14>",
	wx.WXK_F15 : "<F15>",
	wx.WXK_F16 : "<F16>",
	wx.WXK_F17 : "<F17>",
	wx.WXK_F18 : "<F18>",
	wx.WXK_F19 : "<F19>",
	wx.WXK_F20 : "<F20>",
	wx.WXK_F21 : "<F21>",
	wx.WXK_F22 : "<F22>",
	wx.WXK_F23 : "<F23>",
	wx.WXK_F24 : "<F24>",
	wx.WXK_NUMLOCK : "<NUMLOCK>",
	wx.WXK_SCROLL : "<SCROLL>",
	wx.WXK_PAGEUP : "<PAGEUP>",
	wx.WXK_PAGEDOWN : "<PAGEDOWN>",
	wx.WXK_NUMPAD_SPACE : "<NUMPAD_SPACE>",
	wx.WXK_NUMPAD_TAB : "<NUMPAD_TAB>",
	wx.WXK_NUMPAD_ENTER : "<NUMPAD_ENTER>",
	wx.WXK_NUMPAD_F1 : "<NUMPAD_F1>",
	wx.WXK_NUMPAD_F2 : "<NUMPAD_F2>",
	wx.WXK_NUMPAD_F3 : "<NUMPAD_F3>",
	wx.WXK_NUMPAD_F4 : "<NUMPAD_F4>",
	wx.WXK_NUMPAD_HOME : "<NUMPAD_HOME>",
	wx.WXK_NUMPAD_LEFT : "<NUMPAD_LEFT>",
	wx.WXK_NUMPAD_UP : "<NUMPAD_UP>",
	wx.WXK_NUMPAD_RIGHT : "<NUMPAD_RIGHT>",
	wx.WXK_NUMPAD_DOWN : "<NUMPAD_DOWN>",
	#wx.WXK_NUMPAD_PRIOR : "<NUMPAD_PRIOR>",
	wx.WXK_NUMPAD_PAGEUP : "<NUMPAD_PAGEUP>",
	#wx.WXK_NUMPAD_NEXT : "<NUMPAD_NEXT>",
	wx.WXK_NUMPAD_PAGEDOWN : "<NUMPAD_PAGEDOWN>",
	wx.WXK_NUMPAD_END : "<NUMPAD_END>",
	wx.WXK_NUMPAD_BEGIN : "<NUMPAD_BEGIN>",
	wx.WXK_NUMPAD_INSERT : "<NUMPAD_INSERT>",
	wx.WXK_NUMPAD_DELETE : "<NUMPAD_DELETE>",
	wx.WXK_NUMPAD_EQUAL : "<NUMPAD_EQUAL>",
	wx.WXK_NUMPAD_MULTIPLY : "<NUMPAD_MULTIPLY>",
	wx.WXK_NUMPAD_ADD : "<NUMPAD_ADD>",
	wx.WXK_NUMPAD_SEPARATOR : "<NUMPAD_SEPARATOR>",
	wx.WXK_NUMPAD_SUBTRACT : "<NUMPAD_SUBTRACT>",
	wx.WXK_NUMPAD_DECIMAL : "<NUMPAD_DECIMAL>",
	wx.WXK_NUMPAD_DIVIDE : "<NUMPAD_DIVIDE>",

	wx.WXK_WINDOWS_LEFT : "<WINDOWS_LEFT>",
	wx.WXK_WINDOWS_RIGHT : "<WINDOWS_RIGHT>",
	wx.WXK_WINDOWS_MENU : "<WINDOWS_MENU>",

	wx.WXK_SPECIAL1 : "<SPECIAL1>",
	wx.WXK_SPECIAL2 : "<SPECIAL2>",
	wx.WXK_SPECIAL3 : "<SPECIAL3>",
	wx.WXK_SPECIAL4 : "<SPECIAL4>",
	wx.WXK_SPECIAL5 : "<SPECIAL5>",
	wx.WXK_SPECIAL6 : "<SPECIAL6>",
	wx.WXK_SPECIAL7 : "<SPECIAL7>",
	wx.WXK_SPECIAL8 : "<SPECIAL8>",
	wx.WXK_SPECIAL9 : "<SPECIAL9>",
	wx.WXK_SPECIAL10 : "<SPECIAL10>",
	wx.WXK_SPECIAL11 : "<SPECIAL11>",
	wx.WXK_SPECIAL12 : "<SPECIAL12>",
	wx.WXK_SPECIAL13 : "<SPECIAL13>",
	wx.WXK_SPECIAL14 : "<SPECIAL14>",
	wx.WXK_SPECIAL15 : "<SPECIAL15>",
	wx.WXK_SPECIAL16 : "<SPECIAL16>",
	wx.WXK_SPECIAL17 : "<SPECIAL17>",
	wx.WXK_SPECIAL18 : "<SPECIAL18>",
	wx.WXK_SPECIAL19 : "<SPECIAL19>",
	wx.WXK_SPECIAL2 : "<SPECIAL2>",
}

if 'wxMac' in wx.PlatformInfo:
	keyMap[wx.WXK_RAW_CONTROL] = '<WXK_RAW_CONTROL>'
	keyMap[wx.WXK_CONTROL] = "<CONTROL>"
	keyMap[wx.WXK_COMMAND] = "<COMMAND>"
else:
	keyMap[wx.WXK_COMMAND] = "<COMMAND>"
	keyMap[wx.WXK_CONTROL] = "<CONTROL>"
	
# --------------------------------------------------------------------------


#############################
#
#	Define the rows of widgets
#
#############################

class NewRow(wx.Panel):
	def __init__(self, parent, id, i):
		wx.Panel.__init__(self,parent,id)
		self.initialize(i)
	
	# Generates the widgets within the class	
	def initialize(self, i): 				
		"""Initializes the formation of the GUI widgets for each row"""
		
		# Each row gets their own sizer (vgap, hgap)
		# This is added to the main 'sizer' below
		self.rowSizer = wx.GridBagSizer(5,10) 	
		
		# lock checkbox widget
		self.lock_label = wx.StaticText(self, -1, label='lock')
		self.lock_cb = wx.CheckBox(self)
		
		self.rowSizer.Add(self.lock_label, pos=(0,0), span=(1,1) )
		self.rowSizer.Add(self.lock_cb, pos=(1,0), span=(1,1) )
		
		self.lock_cb.Bind(wx.EVT_CHECKBOX, lambda evt: self.lock(evt, i), self.lock_cb) 

		# MIDI selection widget
		self.midiSelect_label = wx.StaticText(self, -1, label='MIDI Note')
		self.midiSelect_spinctrl = wx.SpinCtrl(self, -1)
		self.midiSelect_spinctrl.SetRange(0,256)
		# MIDI Learn/Unlearn buttons
		self.midiLearn_button = wx.Button(self, -1, label='MIDI Learn') 			
		self.midiUnlearn_button = wx.Button(self, -1, label='MIDI Unlearn')
		
		self.rowSizer.Add(self.midiSelect_label, pos=(0,1), span=(1,2), flag=wx.ALIGN_CENTER_HORIZONTAL)
		self.rowSizer.Add(self.midiSelect_spinctrl, pos=(1,1), span=(1,2), flag=wx.EXPAND)
		self.rowSizer.Add(self.midiLearn_button, pos=(2,1), span=(1,1))
		self.rowSizer.Add(self.midiUnlearn_button, pos=(2,2), span=(1,1))
		
		self.midiLearn_button.Bind(wx.EVT_BUTTON, lambda evt: self.midi_learn(evt, i), self.midiLearn_button) 
		self.midiUnlearn_button.Bind(wx.EVT_BUTTON, lambda evt: self.midi_unlearn(evt, i), self.midiUnlearn_button)
		
		# Event type selection widget
		self.eventSelect_label = wx.StaticText(self, -1, label='Event type')
		eventOptions = ['Keyboard binding', 'Insert text', 'Command']
		self.eventSelect_combobox = wx.ComboBox(self, id=i, choices=eventOptions, style=wx.CB_READONLY)
		
		self.rowSizer.Add(self.eventSelect_label, pos=(0,3), span=(1,1), flag=wx.ALIGN_CENTER_HORIZONTAL)
		self.rowSizer.Add(self.eventSelect_combobox, pos=(1,3), span=(1,1), flag=wx.EXPAND)
		
		self.eventSelect_combobox.Bind(wx.EVT_COMBOBOX, lambda evt: self.event_type_select(evt, i), self.eventSelect_combobox)				# creating a 'lambda' event means that I can pass in other arguments to the callback.  In this case, I pass through 'i', which is the itation number.  REFERENCE: http://wiki.wxpython.org/Passing%20Arguments%20to%20Callbacks
		
		# Event Binding widget
		self.eventBinding_label = wx.StaticText(self, i, label='Event binding')
		self.eventBinding_txtentry = wx.TextCtrl(self, -1, value='', size=(200,5) )
		self.capture_button = wx.Button(self, -1, label='Capture')
		self.capture_button.Hide()
		self.runCommand_button = wx.Button(self, -1, label='Test' )
		self.runCommand_button.Hide()
		
		self.rowSizer.Add(self.eventBinding_label, pos=(0,4), span=(1,2), flag=wx.ALIGN_CENTER_HORIZONTAL)
		self.rowSizer.Add(self.eventBinding_txtentry, pos=(1,4), span=(1,2), flag=wx.EXPAND)
		self.rowSizer.Add(self.capture_button, pos=(2,4), span=(1,1), flag=wx.EXPAND)
		self.rowSizer.Add(self.runCommand_button, pos=(2,5), span=(1,1), flag=wx.EXPAND)
		
		self.capture_button.Bind(wx.EVT_BUTTON, lambda evt: self.capture_keys(evt, i), self.capture_button)
		self.runCommand_button.Bind(wx.EVT_BUTTON, lambda evt: self.execute_event(i), self.runCommand_button)
		
		# Reset checkbox widget
		self.resetbutton = wx.Button(self, -1, label='Reset')
		self.rowSizer.Add(self.resetbutton, pos=(1,6), span=(1,1), flag=wx.EXPAND )
		self.resetbutton.Bind(wx.EVT_BUTTON, lambda evt: self.reset_row(evt, i), self.resetbutton) 
		
		# Line widget (separator at the bottom of each panel)
		self.line = wx.StaticLine(self)
		self.rowSizer.Add(self.line, pos=(3,0), span=(1,7), flag=wx.EXPAND|wx.BOTTOM, border=5)
		
		# apply sizer to the row's panel widget (i.e. container)
		self.SetSizerAndFit(self.rowSizer) 

		# Makes cols 4 and 5 expandable
		# Corresponds to the Event Binding area (i.e. user input area)
		self.rowSizer.AddGrowableCol(4)			
		self.rowSizer.AddGrowableCol(5)


	#############################
	#
	#	Define functions for each row
	#
	#############################
	
	# For all functions, 'i' is passed as the row identifier
	def lock(self, event, i ): 
		"""Disables the row from accidental modification"""
		value = event.IsChecked()
		
		if value:
			for children, values in NewRowList[i].__dict__.iteritems():
				if children != 'this' and children != 'lock_cb' and children != 'lock_label' and children != 'rowSizer':
					values.Enable(False)
		else:
			for children, values in NewRowList[i].__dict__.iteritems():
				if children != 'this' and children != 'lock_cb' and children != 'lock_label' and children != 'rowSizer':
					values.Enable(True)
			
	
	def execute_event(self, i):
		"""Executes the event selected in Event Type and based on the 
		   input of Event Binding"""
		if NewRowList[i].eventSelect_combobox.GetValue() == 'Keyboard binding':		
			userkeys = NewRowList[i].eventBinding_txtentry.GetValue().split()
			tap = None
			mods = [autopy.key.MOD_NONE, autopy.key.MOD_NONE, autopy.key.MOD_NONE, autopy.key.MOD_NONE]
			i = 0
			for keys in userkeys:
				if keys == '+':
					# Don't include the '+' key in actions
					pass	
					
				# Control for F* keys (e.g. F4)	
				elif len(keys) == 4:
					fkey = 'K_' + keys[1:3]
					tap = getattr(autopy.key, fkey)
				
				# Control for modifier keys (e.g. Shift, Alt, Ctrl, Meta)
				elif keys[0] == '<':
					k = 'MOD_' + keys[1:len(keys)-1]
					# useful method to call a variable from a string
					mod = getattr(autopy.key, k)  
					mods[i] = mod
					i += 1
					
				# Control for char keys (e.g. alphanumeric)
				else:
					tap = str(keys)
			
			if tap == None:
				autopy.key.tap(mods[0], mods[1] | mods[2] | mods[3] )
			else:
				autopy.key.tap(tap, mods[0] | mods[1] | mods[2] | mods[3] )
			
		elif NewRowList[i].eventSelect_combobox.GetValue() == 'Insert text': 
			usertext = NewRowList[i].eventBinding_txtentry.GetValue()
			autopy.key.type_string(usertext, 0)
		elif NewRowList[i].eventSelect_combobox.GetValue() == 'Command': 
			commandEntry = NewRowList[i].eventBinding_txtentry.GetValue()
			if len(commandEntry) != 0:
				arguments = commandEntry.split(' ')
				c = threading.Thread(target=self.call_subprocess, args=(arguments,))
				c.start()
				
				#ar = ''
				#for i in args:
				#	ar = str(i)
				#os.system(ar)
			else:
				wx.MessageBox('No command entered for row %d' % i, 'Error: Cannot Execute', wx.OK)
		else:
			pass
		
	def call_subprocess(self, arguments):
		subprocess.call(arguments)


	def capture_keys(self, event, i):
		"""Retrieves pressed keys and sends them to the Insert Text 
		   entry field"""
		# This function is largley taken from wxpython demo KeyEvents.py
		keys = []
		class KeySink(wx.Window):
			def __init__(self, parent):
				wx.Window.__init__(self, parent, -1, style=wx.WANTS_CHARS, name="keys")

				# Bind key events to functions
				self.Bind(wx.EVT_KEY_DOWN, self.log_key_event)
				self.Bind(wx.EVT_KEY_UP, lambda evt: on_key_up() )

			def on_key_down(self, evt):
				self.log_key_event(evt)

			def log_key_event(self, evt):
				keycode = evt.GetKeyCode()
				keyname = keyMap.get(keycode, None)

				# / / Some stuff I don't understand 
				if keyname is None:
					if keycode < 256:
						if keycode == 0:
							keyname = "NUL"
						elif keycode < 27:
							pass
							#keyname = "Ctrl-%s" % unichr(ord('A') + keycode-1)
						else:
							keyname = unichr(keycode)
							#keyname = "\"%s\"" % unichr(keycode)
					else:
						keyname = "(%s)" % keycode
						
				UniChr = ''
				if "unicode" in wx.PlatformInfo:
					UniChr = "\"" + unichr(evt.GetUnicodeKey()) + "\""
				keys.append(keyname)
				# / / End stuff I don't understand

		window = wx.Frame(None, -1, 'Keyboard Shortcut Binding', size=(200,100) ) 
		keypanel = KeySink(window)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		dl = wx.StaticText(window, -1, label="Press Keys", style=wx.ALIGN_CENTER)
		sizer.Add(dl, 10, wx.ALL, 10)
		sizer.Add(keypanel, 0, wx.ALL, 0)
		window.SetSizer(sizer)
		window.Fit()
		window.Layout()
		
		window.Show(True)
		window.Centre()
		keypanel.SetFocus()

		def on_key_up():
			NewRowList[i].eventBinding_txtentry.SetValue('')
			NewRowList[i].eventBinding_txtentry.SetInsertionPoint(0)
			for j in keys:
				NewRowList[i].eventBinding_txtentry.AppendText(j)
				if keys.index(j) != len(keys)-1:
					NewRowList[i].eventBinding_txtentry.AppendText(" + ")
			window.Close()

	
	def reset_row(self, event, i):
		"""Resets an individual row to default state"""
		dial = wx.MessageDialog(None, 'Are you sure to reset this row?', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		ret = dial.ShowModal()
		if ret == wx.ID_YES:
			NewRowList[i].eventBinding_label.SetLabel('Event Binding')
			NewRowList[i].eventBinding_txtentry.SetValue('')
			NewRowList[i].midiSelect_spinctrl.SetValue( 0 )	
			NewRowList[i].eventSelect_combobox.SetValue('')
			NewRowList[i].midiSelect_label.SetLabel('MIDI Note')
			NewRowList[i].capture_button.Hide()
			NewRowList[i].runCommand_button.Hide()
			NewRowList[i].rowSizer.Layout()
		
	def event_type_select(self, event, i):
		"""Adjusts layout of GUI depending on selected Event type"""
		value = NewRowList[i].eventSelect_combobox.GetValue()
		NewRowList[i].eventBinding_label.SetLabel( value )
		if value == 'Keyboard binding': 					
			NewRowList[i].capture_button.Show()			
			NewRowList[i].runCommand_button.Hide()
			NewRowList[i].runCommand_button.Show()	
			NewRowList[i].rowSizer.Layout()				
		elif value == 'Command':
			NewRowList[i].runCommand_button.Show()		
			NewRowList[i].capture_button.Hide()
			NewRowList[i].rowSizer.Layout()
		else:
			NewRowList[i].capture_button.Hide()
			NewRowList[i].runCommand_button.Hide()
			NewRowList[i].rowSizer.Layout()



	def midi_capture(self, i):
		"""Function to read in MIDI data and send values to the 
		   popup window defined in midi_learn"""
		# Local references to these variables will affect the 
		# global instance of the variables
		global inport												
		global mgoing

		# Recieves messages from the MIDI input
		while mgoing:											
			if inport.pending() == 0:
				continue
			else:
				try:
					msg = inport.receive(block=True)

					if msg.type == 'note_on':
						self.m.SetValue( 'MIDI Note # ' + str(msg.note) )
					
					elif msg.type == 'control_change':	
						self.m.SetValue( 'MIDI CC # ' + str(msg.control) )

				except IndexError:
					wx.MessageBox('So sorry! Something went wrong.\n\nPlease try again.', 'Odd MIDI Error', wx.OK)

		
		
		
	def midi_learn(self, event, i):
		"""Initiates a window that displays current MIDI data and 
		   optionally sets that value to the selected row"""
		global inport									
		global going
		global mgoing
		going = False
		
		mgoing = True

		self.m = wx.TextEntryDialog(None, 'Touch your MIDI controller, ever so softly', caption='MIDI Learn')#, value='', style=wx.TextEntryDialogStyle)
		if inport != 'default':
			init = threading.Thread(target=self.midi_capture, args=(i,))
			init.daemon = True
			init.start()
			
			n = self.m.ShowModal()

			if n == wx.ID_OK:
				mgoing = False
				parse = self.m.GetValue().split(' ')
				
				if len(parse) > 2:
					if parse[1] == 'Note':
						NewRowList[i].midiSelect_label.SetLabel('MIDI Note')
					elif parse[1] == 'CC':
						NewRowList[i].midiSelect_label.SetLabel('MIDI CC')	
					NewRowList[i].midiSelect_spinctrl.SetValue( int(parse[-1]) )
				else:
					pass
				
				self.Close()
			
				# Re-initiate the global midi read function, inport_select()
				midiread = threading.Thread(target=frame.inport_select, args=(frame.midiSelect_combobox.GetSelection(),))
				midiread.daemon = True
				midiread.start()
		
			
			else:
				mgoing = False
				self.Close()
				
				# Re-initiate the global midi read function, inport_select()
				midiread = threading.Thread(target=frame.inport_select, args=(frame.midiSelect_combobox.GetSelection(),))
				midiread.daemon = True
				midiread.start()	
		else:
			wx.MessageBox('You must select a MIDI Input\n\nIf none are available, make sure you connected your MIDI device properly', 'Error: No MIDI Input', wx.OK | wx.ALIGN_CENTER_HORIZONTAL)
		
		
	def midi_unlearn(self, event, i):
		"""Resets the MIDI Note/CC value to 0"""
		NewRowList[i].midiSelect_spinctrl.SetValue( 0 )
		NewRowList[i].midiSelect_label.SetLabel('MIDI Note')	



# --------------------------------------------------------------------------



#############################
#
#	Main application class
#
#############################

# Subclass of wx.Frame, the base class for standard windows
class application_wx(wx.Frame): 											
	# Defining __init__ is necessary so the subclass is distinct from the wx.Frame class.
	def __init__(self,parent,id,title): 									
		# We have to call the Frame constructor because this is a subclass of wx.Frame
		wx.Frame.__init__(self,parent,id,title)								
		self.parent = parent 
		# This keeps the initialization logically separate from the generation of GUI widgets
		self.initialize()													
		

	#############################
	#
	#	Define main widgets
	#
	#############################
	def initialize(self):			
		# Binds all closing events to the on_quit function										
		self.Bind(wx.EVT_CLOSE, self.on_quit)

		# Primary container widget; could be changed to a Tab later???
		panel = wx.Panel(self)												
		
		# Sizers are organizers; this one works like an HTML table with rows, cols, and rowspan/colspan
		# parameters are vgap and hgap - gap in pixels between all children 
		# (think of it as cell padding: vertical, horizontal)
		sizer = wx.GridBagSizer() 											
																			
		
		#############################
		#
		#	Menu Bar
		#
		#############################
		
		# Generates a menubar widget
		menuBar = wx.MenuBar() 												
		# creates a menu feature
		fileMenu = wx.Menu()												
		
		# Manually create menu item 
		# wx.MenuItem(parent, id, name \ keyboard shortcut)
		fileReset = wx.MenuItem(fileMenu, -1, '&Reset\tCtrl+R')				
		fileMenu.AppendItem(fileReset)
		
		# Automatically create menu item (preloaded in wx)
		fileSave = fileMenu.Append(wx.ID_SAVE, '&Save', 'Save Settings')
		fileOpen = fileMenu.Append(wx.ID_OPEN, '&Open', 'Load settings')
		fileQuit = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit application') 
		
		# Adds the fileMenu itself to the Menu toolbar.  
		# The '&' creates an accelerator key
		# Whatever character follows the & will be a shortcut key
		menuBar.Append(fileMenu, '&File')									
		
		helpMenu = wx.Menu()
		helpAbout = wx.MenuItem(helpMenu, -1, '&About')
		helpReadme = wx.MenuItem(helpMenu, -1, '&README.txt')
		helpMenu.AppendItem(helpAbout)
		helpMenu.AppendItem(helpReadme)
		menuBar.Append(helpMenu, '&Help')
		
		# Sets the menu bar for the self window to 'menuBar'
		self.SetMenuBar(menuBar)											
		
		self.Bind(wx.EVT_MENU, self.on_quit, fileQuit)
		self.Bind(wx.EVT_MENU, self.on_save, fileSave)	
		self.Bind(wx.EVT_MENU, self.on_open, fileOpen)	
		self.Bind(wx.EVT_MENU, self.global_reset, fileReset)
		self.Bind(wx.EVT_MENU, self.show_about, helpAbout)	
		self.Bind(wx.EVT_MENU, self.show_readme, helpReadme)

		
		
		
		#############################
		#
		#	MIDI Dropdown menu input selector
		#   
		#############################
	
		midiSelect_label = wx.StaticText(panel, -1, label='Choose Input Device')
		sizer.Add(midiSelect_label, pos=(0,0), span=(1,1), flag=wx.EXPAND)
		self.midiSelect_combobox = wx.ComboBox(panel, -1, choices=midiInputList, style=wx.CB_READONLY)
		sizer.Add(self.midiSelect_combobox, pos=(1,0), span=(1,1), flag=wx.EXPAND)
		self.midiSelect_combobox.Bind(wx.EVT_COMBOBOX, self.start_midi_read, self.midiSelect_combobox)
				
		#############################
		# 
		# 	GENERATE ROWS OF WIDGETS FOR EACH TAB
		# 	generates <numrows> rows and appends each to list and sizer
		#############################
		
		for i in xrange(numrows): 						
			newRow = NewRow(panel, -1, i)
			NewRowList.append( newRow )
			sizer.Add(newRow, pos=(i+2,0), span=(1,2), flag=wx.EXPAND)
		
		
		# Parameters for main window
		sizer.AddGrowableCol(1)							
		# Sets the layout manager to sizer
		panel.SetSizerAndFit(sizer)  					
		# Fits window to minimum width and height for the contained widgets 
		self.Fit() 										
		# related to above
		self.Layout()									
		# This forces the window to show up (otherwise it stays hidden)				
		self.Show(True)									
		self.Center()
		


	#############################
	# 
	# DEFINE GLOBAL FUNCTIONS FOR MENU AND MIDI PORTING
	# 
	#############################
	
	def inport_select(self, index):
		"""Continually reads incoming MIDI data and determines if action needs to be taken"""
		global inport 										
		global going
		
		going = True

		# Recieves messages from the MIDI input
		while going:											
			if inport.pending() == 0:
				continue
			else:
				try:
					msg = inport.receive(block=True)

					if msg.type == 'note_on':
						# Compare to all bound MIDI notes: 
						# Iterate through all the rows
						for i in xrange(numrows):					
							if msg.note == NewRowList[i].midiSelect_spinctrl.GetValue():	
								# If the msg.note is equal to the MIDIlearn-ed note, then execute the event
								NewRowList[i].execute_event(i)	
					elif msg.type == 'control_change':	
						pass			

				except IndexError:
					wx.MessageBox('So sorry! Something went wrong.\n\nPlease try again.', 'Odd MIDI Error', wx.OK)

					
	def start_midi_read(self, event):
		"""Starts the global MIDI read process; triggered by a change in the MIDI Input dropdown selector"""
		global inport
		global going
		global midiOpenList
		
		# Kill existing thread
		going = False

		# Get the index of selected MIDI port
		index = event.GetSelection()
		inport = midiOpenList[index]
		
		# Start thread
		midiread = threading.Thread(target=self.inport_select, args=(index,))
		midiread.daemon = True
		midiread.start()

	
	def on_quit(self, e):
		"""Exit all threads and Quits the program"""
		global going
		global mgoing
		m = wx.MessageDialog(None, 'Are you sure you want to quit?\n\nSaving your settings is recommended', 'Quit?', wx.YES_NO )
		n = m.ShowModal()
		if n == wx.ID_YES:
			going = False
			mgoing = False
			self.Destroy()
			
		
	def on_save(self, e):
		"""Saves all active settings into an XML file"""
		now = time.strftime('%m-%d-%Y')
		now2 = time.strftime('%m/%d/%Y, %H:%M:%S')
		defFile = 'settings.' + now + '.xml'
		savefile = wx.FileDialog(self, message='Save Settings File...', defaultDir=os.path.dirname(sys.argv[0]), defaultFile=defFile, wildcard='*.xml',  style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)
		if savefile.ShowModal() == wx.ID_OK:
			outputname = savefile.GetPath()
			
			# Build an XML tree
			root = ET.Element('midi-unbound_settings')

			info = ET.SubElement(root, 'info')
			
			filetype = ET.SubElement(info, 'filetype')
			filetype.text = 'Settings File for MIDI Unbound'
			
			date = ET.SubElement(info, 'date')
			date.text = 'Created %s' % now2
			
			midiin = ET.SubElement(info, 'midi_input')
			midiin.text = self.midiSelect_combobox.GetValue()
			
			settings = ET.SubElement(root, 'settings')

			for i in xrange(numrows):
				row = ET.SubElement(settings, 'row')
				row.set('row_number', '%d' % i)
				row.set('midi_number', '%d' % int(NewRowList[i].midiSelect_spinctrl.GetValue()))
				row.set('midi_label', '%s' % (NewRowList[i].midiSelect_label.GetLabel()))
				row.set('locked', '%s' % str(NewRowList[i].lock_cb.GetValue()))
				row.set('eventType', '%s' % str(NewRowList[i].eventSelect_combobox.GetValue()))
				row.set('eventEntry', '%s' % str(NewRowList[i].eventBinding_txtentry.GetValue()))
			
			if lxml_loaded == True:
				# Creates an element tree based on the root object
				tree = ET.ElementTree(root)					
				# Indents properly
				tree = ET.tostring(tree, pretty_print=True)	
			else:
				# if lxml module isn't loaded...
				tree = ET.tostring(root)
			
			# Opens the selected file in write mode, writes data, closes
			outputsettings = open(outputname, 'w')			
			outputsettings.write(tree)						
			outputsettings.close()

		
	def on_open(self, e):
		"""Loads a settings file and fills the appropriate areas with the correct settings.  Must be an XML file saved from this program"""
		openfile = wx.FileDialog(self, message='Load Settings File...', defaultDir=os.path.dirname(sys.argv[0]),  wildcard='XML files (*.xml)|*.xml|Any files (*)|*', style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
		o = openfile.ShowModal()
		if o == wx.ID_OK:
			path = openfile.GetPath()
			if lxml_loaded == True:					
				tree = ET.parse(path)
			else:
				tree = ET.parse(path)
			root = tree.getroot()
			info = root.find('info')
			if root.tag == 'midi-unbound_settings':
				if info.find('midi_input').text != None:
					self.midiSelect_combobox.SetValue(info.find('midi_input').text)
				else:
					self.midiSelect_combobox.SetValue('')
				for elem in root.iter():
					if elem.tag == 'row':
						i = int(elem.attrib['row_number'])
						# Sets values for each XML tag
						NewRowList[i].midiSelect_spinctrl.SetValue(int(elem.get('midi_number')))	
						if elem.get('locked') == 'False':											
							cb = False
						else:
							cb = True
						NewRowList[i].lock_cb.SetValue(cb)		
						
						# Runs the lock function so that it disables the proper inputs
						NewRowList[i].lock(NewRowList[i].lock_cb, i)					
						NewRowList[i].eventBinding_txtentry.SetValue(str(elem.get('eventEntry')))
						NewRowList[i].eventSelect_combobox.SetValue(str(elem.get('eventType')))
						NewRowList[i].midiSelect_label.SetLabel(str(elem.get('midi_label')))
						# call event_type_select that sets proper layout
						z = lambda evt: NewRowList[i].event_type_select(evt, i) 
						z(NewRowList[i].eventSelect_combobox)
			else:
				wx.MessageBox('This is not a valid settings file.\n\nPlease make sure you are opening a file saved directly from this program', 'Error: Could not load settings', wx.OK)
		openfile.Destroy()

		
	def show_about(self, e):
		"""Shows an About dialog with information about the program"""
		try:
			if os.name == 'nt':
				l = open(os.path.dirname(sys.argv[0]) + '\gpl-3.0.txt', 'r')
			else:
				l = open(os.path.dirname(sys.argv[0]) + '/gpl-3.0.txt', 'r')
			gpl = l.read()
			l.close()
		except:
			gpl = "There was an error loading the GNU GPL text document.\nPlease see <http://www.gnu.org/licenses/>."
		
		# creates a wx.AboutDialogInfo object.
		info = wx.AboutDialogInfo() 
		
		# Fill in the elements of info object
		if os.name == 'nt':
			doc = ET.parse(os.path.dirname(sys.argv[0]) + '\metadata.xml')
		else:
			doc = ET.parse(os.path.dirname(sys.argv[0]) + '/metadata.xml')
		
		about = doc.getroot()
		
		#info.SetIcon(wx.Icon('hunter.png', wx.BITMAP_TYPE_PNG)) # Program image
		info.SetName(about.find('name').text)
		info.SetVersion(about.find('version').text)
		info.SetDescription(about.find('description').text)
		info.SetCopyright(about.find('copyright').text)
		info.SetWebSite(about.find('website').text)
		info.AddDeveloper(about.find('developer').text)
		info.AddDocWriter(about.find('docwriter').text)
		info.AddArtist(about.find('artist').text)
				
		# license, from gpl-3.0.txt
		info.SetLicence(gpl)										

		# call all necessary methods upon the created wx.AboutDialogInfo object.
		wx.AboutBox(info)

		
	def show_readme(self, e):
		"""Displays the contents of README.txt in a scollable window dialog"""
		try:
			if os.name == 'nt':
				r = open(os.path.dirname(sys.argv[0]) + '\README.txt', 'r')
			else:
				r = open(os.path.dirname(sys.argv[0]) + '/README.txt', 'r')
			
			read = r.read()
			r.close()
		except:
			read = 'There was an error loading the README file.\nA copy of the README.txt file should have been included in the root directory of this software.\nIf not, please visit <http://www.ericyd.co.nf> for more information.'
		secondwindow = wx.Frame(self, title='README')
		scrolled = wx.ScrolledWindow(secondwindow, -1)
		scrollSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		TextEntry1 = wx.TextCtrl(scrolled, -1, read, size=(400,300), style=wx.TE_READONLY | wx.TE_WORDWRAP | wx.TE_MULTILINE)
		scrollSizer.Add(TextEntry1, 1, wx.ALL)
		mainSizer.Add(scrolled, 1, wx.ALL)
		
		scrolled.SetScrollbars(0, 5, 0, 2)
		scrolled.SetScrollRate( 1, 1 )
		
		scrolled.SetSizerAndFit(scrollSizer)
		secondwindow.SetSizerAndFit(mainSizer)

		secondwindow.Show()
		secondwindow.Center()
		
		
	def global_reset(self, e):
		"""Resets all rows to default state"""
		dial = wx.MessageDialog(None, 'Are you sure to reset ALL rows?\n\n(note: excludes locked rows)', 'Global Reset', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		ret = dial.ShowModal()
		if ret == wx.ID_YES:
			for i in xrange(numrows):
				if NewRowList[i].lock_cb.GetValue() == False:
					NewRowList[i].eventBinding_label.SetLabel('Event Binding')
					NewRowList[i].eventBinding_txtentry.SetValue('')
					NewRowList[i].midiSelect_spinctrl.SetValue( 0 )	
					NewRowList[i].eventSelect_combobox.SetValue('')
					NewRowList[i].midiSelect_label.SetLabel('MIDI Note')
					NewRowList[i].capture_button.Hide()
					NewRowList[i].runCommand_button.Hide()
					NewRowList[i].rowSizer.Layout()



# We create a 'main' that is executed when the program is run	
if __name__=="__main__":	
	app = wx.App()	
	frame = application_wx(None,-1,'MIDI Unbound')
	
	# Set application icon
	if os.name == 'nt':
		favicon = wx.Icon(os.path.dirname(sys.argv[0]) + '\icon_midi.png', wx.BITMAP_TYPE_PNG, 50, 50)
	else:
		favicon = wx.Icon(os.path.dirname(sys.argv[0]) + '/icon_midi.png', wx.BITMAP_TYPE_PNG, 50, 50)
	frame.SetIcon(favicon)
	
	# Set the app to loop indefinitely for user input
	app.MainLoop()
	
