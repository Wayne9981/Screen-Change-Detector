import logging
from typing import Callable
import sys
import termios

from pynput.keyboard import KeyCode

import utils

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


class MouseEventHandler:
    def __init__(self):
        self.start = None
        self.end = None

    @utils.log_times
    def handle(self, point: tuple[float, float], pressed: bool):
        point = list(map(int, point))
        if pressed:
            self.start = point
        else:
            self.end = point

    @utils.log_times
    def get_box(self):
        if self.start and self.end:
            left, right = sorted((self.start[0], self.end[0]))
            up, down = sorted((self.start[1], self.end[1]))
            return [left, up, right, down]
