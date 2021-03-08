import enum
import typing
from pathlib import PurePosixPath

Path = typing.Union[PurePosixPath, str]


class FileFlags(enum.Flag):
    READ = enum.auto()
    WRITE = enum.auto()
    TRUNCATE = enum.auto()
    APPEND = enum.auto()


class IFilesystem(typing.Protocol):
    def open(self, path: Path, flags: FileFlags):
        """
        Open a file.

        *flags* is meant to mimic the *mode* parameter of
        :func:`os.open <https://docs.python.org/3/library/os.html#os.open>` because the
        *mode* parameter of
        :func:`open <https://docs.python.org/3/library/functions.html#open>` has never
        made sense to me.
        """
        ...

    def mkdir(self, path: Path) -> None:
        """Create directory."""
        ...

    def mkdirs(self, path: Path) -> None:
        """Create directories recursively."""
        ...

    def makedirs(self, path: Path) -> None:
        """
        Create directories recursively.

        This function is identical to mkdirs. It exists to match
        :func:`os.makedirs <https://docs.python.org/3/library/os.html#os.makedirs>`
        """
        ...

    def listdir(self, path: Path) -> typing.List:
        ...

    def rm(self, path: Path) -> None:
        """Remove a file."""
        ...

    def rmtree(self, path: Path) -> None:
        """Remove a directory and all files and directories under it."""
        ...

    def rmdir(self, path: Path) -> None:
        """Remove an empty directory."""
        ...
