from functools import cached_property

from pygit2 import Repository

from .exceptions import InvalidPathException
from .mixins import DirectoryMixin, FileMixin
from .typing import IFilesystem, Path

__all__ = ("AcidFS", "InvalidPathException")


class AcidFS(FileMixin, DirectoryMixin, IFilesystem):
    path: Path

    def __init__(self, path):
        self.path = path

    @cached_property
    def _repository(self):
        return Repository(self.path, bare=True)
