import logging
from typing import Callable
import sys
import termios

from pynput.keyboard import KeyCode

logger = logging.getLogger(__name__)


class KeyboardEventHandler:
    def __init__(self, handlers: dict[str, Callable]):
        self.handlers = handlers

    def handle(self, key: KeyCode):
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        termios.tcflush(sys.stdout, termios.TCIOFLUSH)
        print(f"\rOn press key: {key}")
        logger.info(f"On press key: {key}")
        handler = self.handlers.get(key.char.lower())
        if handler:
            print(f"{type(handler).__name__} started")
            handler()
            print(f"{type(handler).__name__} finished")
