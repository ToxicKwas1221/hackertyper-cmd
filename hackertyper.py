import os
import random
from platform import platform
from argparse import ArgumentParser
from pynput.keyboard import Listener, KeyCode
from colorama import Fore, Style

if platform().lower().startswith('windows'):
    from colorama import init
    init()

parser = ArgumentParser()
parser.add_argument('-f', '--file', help='pick a specific file from the directory')

speed = 4  # characters per button press
progress = 0


def on_press(key):
    global code, progress, speed
    if key == KeyCode.from_char('q'):
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
    if args.file:
        try:
            with open(args.file, 'r') as file:
                code = file.read()
        except FileNotFoundError:
            print(Fore.RED+f'File {args.file} is not found!'+Fore.RESET)
            exit()
    else:
        os.chdir('pwn3r-scripts')
        file = random.choice(os.listdir(path='.'))
        while file == '.DS_Store':  # MacOSX compatibility
            file = random.choice(os.listdir(path='.'))
        with open(file, 'r') as file:
            code = file.read()

    print(Fore.GREEN, Style.BRIGHT)
    listener = Listener(on_press=on_press, suppress=True)  # threading.Thread instance
    listener.start()
    listener.join()
    print(Fore.RESET, Style.RESET_ALL)

# THE END
