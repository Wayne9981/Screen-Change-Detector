import logging
from typing import Union

from pynput.keyboard import KeyCode, Key, Listener
from callback import screen_analysis, periodic_screen_analysis


logging.basicConfig(
    filename="history.log",
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(name)s:%(message)s",
)

logger = logging.getLogger(__name__)


class KeyboardEventHandler:
    handler = {
        "z": screen_analysis,
        "y": periodic_screen_analysis,
    }

    def handle(self, key: KeyCode):
        print(f"\rOn press key: {key}")
        logging.info(f"On press key: {key}")
        handler = self.handler.get(key.char.lower())
        if handler:
            print(f"{handler.__name__} started")
            handler()
            print(f"{handler.__name__} finished")


keyboard_handler = KeyboardEventHandler()


def on_press(key: Union[KeyCode, Key, None]):
    if isinstance(key, KeyCode):
        keyboard_handler.handle(key)
    if key == Key.esc:
        return False


if __name__ == "__main__":
    logger.info("Main.py started")
    print("Main.py started")
    with Listener(on_press=on_press) as listener:  # type: ignore
        listener.join()
    logger.info("Main.py finished")
    print("Main.py finished")
