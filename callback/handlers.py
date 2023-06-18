import logging
import os
from time import sleep
from datetime import datetime, timedelta

from pynput.mouse import Listener, Button
from PIL import ImageGrab

from src.config import ConfigAccessor
from src.event_handler import MouseEventHandler
from .screen_analysis import _screen_analysis

logger = logging.getLogger(__name__)


class ScreenAnalysis:
    def __init__(self, cfg_proxy: ConfigAccessor):
        self.cfg_proxy = cfg_proxy

    def __call__(self):
        cfg = self.cfg_proxy.cfg
        _screen_analysis(
            cfg.diff_threshold_percentage, cfg.image_folder, cfg.screen_shot_area
        )


class PeriodicScreenAnalysis:
    def __init__(self, cfg_proxy: ConfigAccessor):
        self.cfg_proxy = cfg_proxy

    def __call__(self):
        cfg = self.cfg_proxy.cfg
        end_time = datetime.now() + timedelta(minutes=cfg.analysis_minutes)
        logger.info(f"{end_time = }")
        print(f"Job will end at {end_time}")
        while datetime.now() < end_time:
            _screen_analysis(
                cfg.diff_threshold_percentage, cfg.image_folder, cfg.screen_shot_area
            )
            sleep(cfg.time_interval_sec)


class SettingConfig:
    def __init__(self, cfg_proxy: ConfigAccessor, mouse_handler: MouseEventHandler):
        self.cfg_proxy = cfg_proxy
        self.mouse_handler = mouse_handler

    def __call__(self):
        cfg = self.cfg_proxy.cfg
        time_interval_sec = input(
            (
                "\rPlease enter the screenshot interval in seconds,"
                " or press Enter to use the previous setting: "
            )
        )
        logger.info(f"{time_interval_sec = }")
        try:
            cfg.time_interval_sec = float(time_interval_sec)
        except ValueError:
            pass

        analysis_minutes = input(
            (
                "\rPlease enter the analysis time in minutes,"
                " or press Enter to use the previous setting: "
            )
        )
        logger.info(f"{analysis_minutes = }")
        try:
            cfg.analysis_minutes = int(analysis_minutes)
        except ValueError:
            pass

        print(
            "\rPlease use left mouse button to drag and select the screenshot area, "
            "or right-click use the previous setting."
        )
        with Listener(on_click=self.on_click) as listener:
            listener.join()
        box = self.mouse_handler.get_box()
        if box:
            cfg.screen_shot_area = self.mouse_handler.get_box()
            img = ImageGrab.grab(bbox=box).convert("RGB")
            os.makedirs(cfg.image_folder, exist_ok=True)
            img.save(os.path.join(cfg.image_folder, "demo.jpeg"))

        self.cfg_proxy.save()

    def on_click(self, x: float, y: float, button: Button, pressed: bool):
        if button == Button.right:
            return False
        print(f"{'Pressed' if pressed else 'Released'} at {(x, y)}")
        self.mouse_handler.handle((x, y), pressed)
