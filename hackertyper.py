import os
import random
from argparse import ArgumentParser
from pynput.keyboard import Listener, KeyCode, Key
from colorama import Fore, Style, init

init()  # initialize colorama

parser = ArgumentParser()
parser.add_argument('-f', '--file', help='pick a specific file from the directory')
parser.add_argument('-c', '--color', help='choose the output color. Options:\
					black, red, green, yellow, blue, magenta, cyan, white. (Not case sensitive)'
					, default='green')
parser.add_argument('-s', '--speed', help='set the speed of the output(default is 4)', default=4, type=int)
parser.add_argument('--bright', help='make the output bright', action='store_true')

_progress = 0


def on_press(key):
	global code, _progress, speed
	if key == Key.esc:
		return False  # Stops the listener thread
	if '\n' in code[_progress:_progress+speed]:
		print(code[_progress:_progress + speed], end='', flush=True)
		_progress += speed
		while code[_progress:_progress+speed] == '    ':
			print(code[_progress:_progress+speed], end='', flush=True)
			_progress += speed
	else:
		print(code[_progress:_progress+speed], end='', flush=True)
		_progress += speed


if __name__ == '__main__':
	args = parser.parse_args()
	speed = args.speed
	color = args.color.upper()

	if args.bright:
		print(Style.BRIGHT, end='')
		
	if args.file:
		try:
			with open(args.file, 'r') as file:
				code = file.read()
		except FileNotFoundError:
			print(Fore.RED+f'File {args.file} is not found!'+Style.RESET_ALL)
			exit()
	else:
		os.chdir('pwn3r-scripts')
		file = random.choice(os.listdir(path='.'))
		with open(file, 'r') as file:
			code = file.read()

	try:
		exec(f'print(Fore.{color}, end="")')
	except (AttributeError, SyntaxError):
		parser.print_help()
		exit()

	listener = Listener(on_press=on_press, suppress=True)  # threading.Thread instance
	listener.start()
	listener.join()
	print(Style.RESET_ALL)

# THE END
