import re
from pathlib import PurePosixPath

from .exceptions import InvalidPathException
from .typing import IFilesystem

_root_path = PurePosixPath("/")
# A valid filename is alphanumeric, underscores, hyphens, spaces and a periods.
# I could allow more characters, but I dont want to make this too
# lenient, and allow files that are completely unreadable.
_filename_re = re.compile(r"[a-z0-9_\- .]+", flags=re.IGNORECASE)
_reserved_names = (
    # Windows reserved names
    {"CON", "NUL", "PRN", "AUX"}
    | {f"LPT{n}" for n in range(10)}
    | {f"COM{n}" for n in range(10)}
)


def _path_parts(path):
    absolute_path = _root_path / path

    for part in absolute_path.relative_to(_root_path).parts:
        if part[:1] == ".":
            # Disallow dot-files in the repository.
            # I *think* technically we could store `.` and `..`, but then when
            # the files are moved into the index, or pushed to a remote
            # there would inevitably be errors.
            # Also, I might need to store directory metadata in the future, and would
            # probably use dot-files for that.
            raise InvalidPathException("dot-files", "dot-files are forbidden.")
        if not _filename_re.fullmatch(part):
            raise InvalidPathException(
                "invalid-character", "filename contains invalid character"
            )
        if part in _reserved_names:
            raise InvalidPathException("reserved-name", "filename is reserved")

        yield part


class FileMixin:
    def open(self: IFilesystem, path, flags):
        return tuple(_path_parts(path))

    def rm(self: IFilesystem, path):
        pass


class DirectoryMixin:
    def listdir(self: IFilesystem, path):
        pass

    def rmdir(self: IFilesystem, path):
        pass

    def rmtree(self: IFilesystem, path):
        pass

    def mkdir(self: IFilesystem, path):
        pass

    def mkdirs(self: IFilesystem, path) -> None:
        pass

    def makedirs(self: IFilesystem, path) -> None:
        return self.makedirs(path)
