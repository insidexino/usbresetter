#!/usr/bin/env python3

from os import system,getuid
import curses
import subprocess
import fcntl

def resetusb(device):
	system('clear')
	print()
	with open ('/dev/bus/usb/{}/{}'.format(device[0],device[1]),'w') as f:
		try:
			fcntl.ioctl(f,0x5514)
		except:
			print('Resetting failed!')
		else:
			print('Successfully reset!')

	print()
	input("Press enter key to continue...")


if (getuid() != 0):
	exe = subprocess.Popen(['sudo', __file__])
	exe.wait()
	exit(1)

while True:
	output = subprocess.Popen('lsusb', stdout=subprocess.PIPE, universal_newlines=True ).communicate()[0]

	screen = curses.initscr()
	screen.clear()
	screen.border(0)

	pos=4
	cmd_list = {}
	cmdno=ord('a')
	screen.addstr(2, 2, "Select a USB port to reset...")
	for line in output.split('\n'):
		content = line.split()
		if (len(content)==0):
			continue;
		cmd_list[chr(cmdno)] =  [content[1], content[3].replace(':','')]

		screen.addstr(pos, 4, chr(cmdno) + ' - ' + line)

		pos+=1
		cmdno+=1

	screen.addstr(pos, 4, chr(cmdno) + ' - Quit')
	screen.addstr(pos+2, 2, '>')

	x = screen.getch()

	if (x == cmdno):
		curses.endwin()
		break;

	if (x < cmdno and x >= ord('a')):
		curses.endwin()
		resetusb(cmd_list[chr(x)])
