#MIDI Unbound

**AUTHOR:** Eric Dauenhauer

**VERSION:** 1.0

**COPYRIGHT:** Copyright 2014 Eric Dauenhauer

**LICENSE:** GNU GPL License (see gpl.txt in main directory)



## OVERVIEW
This software provides the ability to bind desktop events to MIDI Control Changes. At this time it has only been tested on and packaged for Linux. Windows will come soon, I hope.

In this case, I used the phrase 'desktop events' to mean any of the following:

+ Keyboard combinations (e.g. Shift+Alt+L)
+ Inserting characters
+ Any other computer commands, not limited to traditional MIDI software

The purpose of this software is to expand the use of MIDI controllers beyond digital music production. The program allows MIDI events to be bound to external desktop events. This can be particularly useful for repetetive tasks. A few simple examples of use include:

+ Creating a super clipboard for copy/paste events. You can bind a different MIDI note to different strings of text and insert them when the MIDI note is triggered
+ Running custom commands or launching applications with the touch of a button
+ Binding keyboard shortcuts to a single button press. This can be particularly useful given that the keyboard shortcuts can be arbitrarily large and complex. Even if it isn't easy to replicate on a traditional keyboard, the shortcut can be bound to a MIDI event and triggered every time the note is triggered.


## INSTALLATION	

+ If you are using Linux, simply launch the executable included in the root directory.

+ If you are launching from the Python script (not recommended), the script requires three third party modules:
    + wxPython: The GUI toolkit. Go to 
            http://wiki.wxpython.org/How%20to%20install%20wxPython 
            for how to install this on your system
    + Mido: Handles MIDI input. To install with pip, simply run: 
            pip install mido 
            Otherwise, source downloads are available here: 
            https://pypi.python.org/pypi/mido/1.1.6#downloads 
            or here:
            https://github.com/olemb/mido/
    + Autopy: Performs keyboard emulation. To install on Windows, go to:
            https://pypi.python.org/pypi/autopy/.
            For other OS, simply run: 
            easy_install autopy



## HOW TO USE	

+ The purpose of this software is to expand the use of MIDI controllers beyond digital music production.  The program allows MIDI events to be bound to external desktop events.  This can be particularly useful for repetetive tasks.  A few simple examples of use include:
    + Creating a super clipboard for copy/paste events.  You can bind a different MIDI note to different strings of text and insert them when the MIDI note is triggered
    + Running custom commands or launching applications with the touch of a button
    + Binding keyboard shortcuts to a single button press.  This can be particularly useful given that the keyboard shortcuts can be arbitrarily large and complex.  Even if it isn't easy to replicate on a traditional keyboard, the shortcut can be bound to a MIDI event and triggered every time the note is triggered.

+ The design of this software should be quite self evident.  Each row represents a new MIDI event binding.  The functions of each widget within the rows are listed below:
    + Lock: This checkbox locks the row so that changes are not accidentally made to the event binding.
    + MIDI Note: Selects the MIDI event to which the desktop event will be bound.  This can be selected manually, or you can use the MIDI Learn button.  Clicking the MIDI Learn button will save the next triggered MIDI event as the MIDI Note or Control Change number.  MIDI Unlearn simply resets this value to 0.
    + Event Selection: Select the type of event you want to execute when the MIDI event is triggered.  Possible options are 'Keyboard Binding' which will emulate a keyboard shortcut; 'Insert Text' which will insert any string of text; and 'Command' which allows you to run a custom command.
    + Event Binding: User entry for the bound event.  For example, type in the command that should be executed upon MIDI event triggering (e.g. gedit)
    + Reset: Resets the values of the row.

+ This program allows for the saving of settings files.  Simply name the file and then load it the next time you want to use those settings.

**! NOTE: The settings file is fairly primitive and may not behave correctly if edited.**


## KNOWN BUGS	

+ Keyboard binding has limited support, and occassionally malfunctions with modifier keys.  One known example is that using the <CONTROL> modifier key produces the same effect as <CONTROL>+<SHIFT>.  I believe this is due to an error in the module used for keyboard emulation (autopy), but regretfully the module has not had many updated in the past several years so bug fixes are unlikely.  I will be searching for a better way to implement this in the future.
+ MIDI CC (Control Change) not yet supported.  Confusingly, I have built in support to capture these event, but not implemented support to bind them properly



#FUTURE PLANS	

+ Add tabs to accomodate more MIDI event bindings in a more user friendly interface
+ Add system controls (e.g. Volume, Mute, etc) as event binding options
+ Fix keyboard binding issues

		
	
#CONTACT			
For any questions, concerns, or bug reports, please contact:
Eric Dauenhauer
eric_yd@yahoo.com
