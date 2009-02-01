'''
Python bindings for the HDAPS interface
'''

# Copyright: 2008-2009 Evgeni Golov <sargentd@die-welt.net>
# License: GPL-2

import struct
import os.path

__SYSFS_HDAPS='/sys/devices/platform/hdaps'
__SYSFS_HDAPS_CALIBRATION='%s/calibrate' % __SYSFS_HDAPS
__SYSFS_HDAPS_POSITION='%s/position' % __SYSFS_HDAPS
__SYSFS_HDAPS_KEYBOARD_ACTIVITY='%s/keyboard_activity' % __SYSFS_HDAPS
__SYSFS_HDAPS_MOUSE_ACTIVITY='%s/mouse_activity' % __SYSFS_HDAPS
__INPUT_HDAPS_EVENT='/dev/input/hdaps/accelerometer-event'

def readPosition(calibrate=False):
	if calibrate:
		filename = __SYSFS_HDAPS_CALIBRATION
	else:
		filename = __SYSFS_HDAPS_POSITION
	line = __readSysfs(filename).strip(')(')
	posX,posY = line.split(',')
	return (int(posX), int(posY))

def readKeyboardActivity():
	return int(__readSysfs(__SYSFS_HDAPS_KEYBOARD_ACTIVITY))

def readMouseActivity():
	return int(__readSysfs(__SYSFS_HDAPS_MOUSE_ACTIVITY))

def __readSysfs(filename):
	try:
		fd = file(filename, 'r')
		line = fd.readline().strip()
		fd.close()
	except IOError:
		raise IOError, '%s could not be read, is the "hdaps" module loaded?' % filename
	return line

def hasInputInterface():
	return os.path.exists(__INPUT_HDAPS_EVENT)

def readInputPosition(callback):
	if not hasInputInterface():
		raise IOError, 'You don\'t have %s. Is the "hdaps" module from tp_smapi loaded?' % __INPUT_HDAPS_EVENT
	x = 0
	y = 0
	input = open(__INPUT_HDAPS_EVENT,"rb")
	event = input.read(16)
	while event:
		(tv_sec, tv_usec, type, code, value) = struct.unpack('iihhi',event)
		if type == 3:
			if code == 0:
				x = value
			if code == 1:
				y = value
		if type == 0 and code == 0:
			callback(x, y)
		event = input.read(16)
	input.close()
