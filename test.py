import os
import json
from setenv import create_json


def test_structure():
    if not os.path.exists("config.json"):
        create_json()

    with open("config.json", "r") as file:
        cfg = json.load(file)

    assert "Name" in cfg
    assert "Levels" in cfg
    assert "Normal" in cfg["Levels"]

    for level in cfg["Levels"]:
        assert isinstance(level, str)

        x, y = cfg["Levels"][level]
        assert isinstance(x, int)
        assert isinstance(y, int)


def run_tests():
    test_structure()



