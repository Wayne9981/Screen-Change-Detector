import logging
from typing import Callable

from pynput.keyboard import KeyCode

logger = logging.getLogger(__name__)


class KeyboardEventHandler:
    def __init__(self, handlers: dict[str, Callable]):
        self.handlers = handlers

    def handle(self, key: KeyCode):
        print(f"\rOn press key: {key}")
        logger.info(f"On press key: {key}")
        handler = self.handlers.get(key.char.lower())
        if handler:
            print(f"{type(handler).__name__} started")
            handler()
            print(f"{type(handler).__name__} finished")
