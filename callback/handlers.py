from time import sleep

from src.config import ConfigAccessor
from .screen_analysis import _screen_analysis


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
        while True:
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
        try:
            cfg.time_interval_sec = float(time_interval_sec)
        except ValueError:
            pass

        self.cfg_proxy.save()
