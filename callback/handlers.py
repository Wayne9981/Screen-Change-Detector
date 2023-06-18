import logging
from time import sleep
from datetime import datetime, timedelta

from src.config import ConfigAccessor
from .screen_analysis import _screen_analysis

logger = logging.getLogger(__name__)


class ScreenAnalysis:
    def __init__(self, cfg_proxy: ConfigAccessor):
        self.cfg_proxy = cfg_proxy

    def __call__(self):
        cfg = self.cfg_proxy.cfg
        _screen_analysis(cfg.diff_threshold_percentage, cfg.image_folder)


class PeriodicScreenAnalysis:
    def __init__(self, cfg_proxy: ConfigAccessor):
        self.cfg_proxy = cfg_proxy

    def __call__(self):
        cfg = self.cfg_proxy.cfg
        end_time = datetime.now() + timedelta(minutes=cfg.analysis_minutes)
        logger.info(f"{end_time = }")
        print(f"Job will end at {end_time}")
        while datetime.now() < end_time:
            _screen_analysis(cfg.diff_threshold_percentage, cfg.image_folder)
            sleep(cfg.time_interval_sec)


class SettingConfig:
    def __init__(self, cfg_proxy: ConfigAccessor):
        self.cfg_proxy = cfg_proxy

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

        self.cfg_proxy.save()
