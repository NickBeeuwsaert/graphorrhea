from functools import cached_property
from logging.config import dictConfig

import toml
from plaster import ILoader
from plaster.protocols import IWSGIProtocol
from plaster.uri import PlasterURL

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
        return self._config.get(section, {})

    def setup_logging(self, defaults=None):
        dictConfig(self._config["logging"])
