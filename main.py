import logging
from typing import Union

from pynput.keyboard import KeyCode, Key, Listener

from src.config import ConfigAccessor
from src.event_handler import KeyboardEventHandler, MouseEventHandler
from callback import ScreenAnalysis, PeriodicScreenAnalysis, SettingConfig


logging.basicConfig(
    filename="history.log",
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(name)s:%(message)s",
)

logger = logging.getLogger(__name__)

cfg_accessor = ConfigAccessor()
hotkeys = cfg_accessor.cfg.hotkeys
mouse_handler = MouseEventHandler()

handlers = {
    hotkeys.screen_analysis: ScreenAnalysis(cfg_accessor),
    hotkeys.periodic_screen_analysis: PeriodicScreenAnalysis(cfg_accessor),
    hotkeys.setting_config: SettingConfig(cfg_accessor, mouse_handler),
}
keyboard_handler = KeyboardEventHandler(handlers)


def on_press(key: Union[KeyCode, Key, None]):
    if isinstance(key, KeyCode):
        keyboard_handler.handle(key)
    if key == Key.esc:
        return False


def main():
    logger.info("Main.py started")
    print("Main.py started")
    with Listener(on_press=on_press) as listener:  # type: ignore
        listener.join()
    logger.info("Main.py finished")
    print("Main.py finished")


if __name__ == "__main__":
    main()
