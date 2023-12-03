from dataclasses import dataclass
import tomllib
from os import path


@dataclass
class Coordinates:
    """Configures a set of coordinates"""

    x: int
    y: int


@dataclass
class Config:
    """i3uw configuration"""

    handled_workspaces: list[str]
    size: Coordinates
    position: Coordinates


def load_config():
    """Load the configuration for i3uw"""

    curr_path = path.dirname(path.realpath(__file__))
    config_path = path.join(curr_path, "../config.toml")

    with open(config_path, "rb") as f:
        parsed_config = tomllib.load(f)

        return Config(
            handled_workspaces=parsed_config["main"]["handled_workspaces"],
            size=Coordinates(**parsed_config["window"]["size"]),
            position=Coordinates(**parsed_config["window"]["position"]),
        )


config = load_config()
