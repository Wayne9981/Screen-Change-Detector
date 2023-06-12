import logging
import sys

from pynput import keyboard

from callback import screen_analysis, periodic_screen_analysis


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(name)s:%(message)s",
)


class KeyboardEventHandler:
    handler = {
        "z": screen_analysis,
        "y": periodic_screen_analysis,
    }

    def handle(self, key):
        print("\r", end="")
        logging.info(f"On press key: {key}")
        handler = self.handler.get(key.char.lower())
        if handler:
            handler()


keyboard_handler = KeyboardEventHandler()


def on_press(key):
    if isinstance(key, keyboard.KeyCode):
        keyboard_handler.handle(key)
    if key == keyboard.Key.esc:
        return False


if __name__ == "__main__":
    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
