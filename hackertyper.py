import os
import random
from argparse import ArgumentParser
from pynput.keyboard import Listener, KeyCode, Key
from colorama import Fore, Style, init

init()

parser = ArgumentParser()
parser.add_argument('-f', '--file', help='pick a specific file from the directory')
parser.add_argument('-c', '--color', help='choose the output color. Options:\
					black, red, green, yellow, blue, magenta, cyan, white. (Not case sensitive)'
					, default='green')

speed = 4  # characters per button press
progress = 0


def on_press(key):
	global code, progress, speed
	if key == Key.esc:
		return False  # Stops the listener thread
	if '\n' in code[progress:progress+speed]:
		print(code[progress:progress + speed], end='', flush=True)
		progress += speed
		while code[progress:progress+speed] == '    ':
			print(code[progress:progress+speed], end='', flush=True)
			progress += speed
	else:
		print(code[progress:progress+speed], end='', flush=True)
		progress += speed


if __name__ == '__main__':
	args = parser.parse_args()
	color = args.color.upper()

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
		while file == '.DS_Store':  # MacOSX compatibility
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
