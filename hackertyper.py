import sys
from pynput.keyboard import Listener, KeyCode
from colorama import Fore


speed = 4  # characters per button press
progress = 0


try:
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        code = file.read()
except IndexError:
    print(Fore.RED + 'Usage: python hackertyper.py <filename>' + Fore.RESET)
    sys.exit()
except FileNotFoundError:
    print(Fore.RED+'File \'{}\' does not exist!'.format(filename)+Fore.RESET)
    sys.exit()


def on_press(key):
    global code, progress, speed
    if key == KeyCode.from_char('q'):
        return False  # Stops the listener thread
    print(Fore.GREEN+code[progress:progress+speed], end='', flush=True)
    progress += speed


if __name__ == '__main__':
    listener = Listener(on_press=on_press, suppress=True)  # threading.Thread instance
    listener.start()
    listener.join()
    print(Fore.RESET)

# THE END
