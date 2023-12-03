from dataclasses import dataclass
import tomllib


@dataclass
class Coordinates:
    """Configures a set of coordinates"""

    x: int
    y: int


@dataclass
class Size:
    """Configures the size of the floating window"""

    width: int
    height: int


@dataclass
class Config:
    """i3uw configuration"""

    handled_workspaces: list[str]
    size: Size
    position: Coordinates


def load_config():
    """Load the configuration for i3uw"""

    with open("config.toml", "rb") as f:
        parsed_config = tomllib.load(f)

        return Config(
            handled_workspaces=parsed_config["handled_workspaces"],
            size=Size(**parsed_config["window"]["size"]),
            position=Coordinates(**parsed_config["window"]["position"]),
        )


config = load_config()
