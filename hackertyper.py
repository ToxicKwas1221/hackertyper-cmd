import sys
from pynput.keyboard import Listener, KeyCode
from colorama import Fore, Style


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
    try:
        filename = sys.argv[1]
        with open(filename, 'r') as file:
            code = file.read()
    except IndexError:
        print(Fore.RED + 'Usage: python hackertyper.py <filename>' + Fore.RESET)
        sys.exit()
    except FileNotFoundError:
        print(Fore.RED + 'File \'{}\' does not exist!'.format(filename) + Fore.RESET)
        sys.exit()
    print(Fore.GREEN, Style.BRIGHT)
    listener = Listener(on_press=on_press, suppress=True)  # threading.Thread instance
    listener.start()
    listener.join()
    print(Fore.RESET, Style.RESET_ALL)

# THE END
