import json
from dataclasses import asdict

import pytest

from src.config import Config, Hotkeys


@pytest.fixture
def config_text() -> str:
    with open("config.json") as f:
        text = f.read()
    return text


def test_config(config_text: str):
    config_dict = json.loads(config_text)
    config = Config.from_dict(config_dict)
    assert config.hotkeys == Hotkeys(**config_dict["hotkeys"])

    assert asdict(config) == config_dict
