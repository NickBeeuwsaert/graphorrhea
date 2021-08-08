from functools import cached_property
from logging.config import dictConfig
from pathlib import Path

import toml
from plaster import ILoader
from plaster.protocols import IWSGIProtocol
from plaster.uri import PlasterURL

from .interpolate import interpolate
from .mixins import WSGIMixin

__all__ = "Loader"


class Loader(WSGIMixin, IWSGIProtocol, ILoader):
    uri: PlasterURL

    def __init__(self, uri: PlasterURL):
        self.uri = uri

    @cached_property
    def _config(self):
        return toml.load(self.uri.path)

    def get_sections(self):
        return list(self._config.keys())

    def get_settings(self, section=None, defaults=None):
        settings = self._config.get(section, {})

        return interpolate(settings, here=Path(self.uri.path).parent.resolve())

    def setup_logging(self, defaults=None):
        dictConfig(self._config["logging"])
