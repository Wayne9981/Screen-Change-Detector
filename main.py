import logging
import sys
from typing import Union

from pynput.keyboard import KeyCode, Key, Listener
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

    def handle(self, key: KeyCode):
        print("\r", end="")
        logging.info(f"On press key: {key}")
        handler = self.handler.get(key.char.lower())
        if handler:
            handler()


keyboard_handler = KeyboardEventHandler()


def on_press(key: Union[KeyCode, Key, None]):
    if isinstance(key, KeyCode):
        keyboard_handler.handle(key)
    if key == Key.esc:
        return False


if __name__ == "__main__":
    # Collect events until released
    with Listener(on_press=on_press) as listener:  # type: ignore
        listener.join()
