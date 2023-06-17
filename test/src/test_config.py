import json
from dataclasses import asdict

import pytest

from src.config import Config, Hotkeys


@pytest.fixture
def config_text():
    return """
{
  "image_folder": "images",
  "diff_threshold_percentage": 30,
  "time_interval_sec": 5,
  "screen_shot_area": [[0,0], [50, 50]],
  "hotkeys": {
    "screen_analysis": "z",
    "periodic_screen_analysis": "y"
  }
}
"""


def test_config(config_text):
    config_dict = json.loads(config_text)
    config = Config.from_dict(config_dict)
    assert config.hotkeys == Hotkeys(**config_dict["hotkeys"])

    assert asdict(config) == config_dict
