"""Parser to read text documents with frontmatter."""
import functools
import io
import operator
from functools import cached_property
from typing import IO, Iterator, Optional

import yaml

__all__ = ("loads", "load")

_read_lines: functools.partial[Iterator[str]] = functools.partial(
    map, operator.methodcaller("rstrip", "\r\n")
)


def _read_frontmatter(line_iter):
    for line in line_iter:
        # Read lines until we hit a document start marker
        # or a document end marker
        if line in ("---", "..."):
            return

        yield line


def _cons(car, cdr):
    yield car
    yield from cdr


class Document:
    """Represents a text file with additional metadata stored in it's header."""

    frontmatter: str

    def __init__(self, line_iter, frontmatter=None):
        """Initialize a new document.

        :param line_iter: An iterable of each line of the document
        :param frontmatter: The unparsed YAML frontmatter
        """
        self._line_iter = line_iter
        self.frontmatter = frontmatter

    @cached_property
    def metadata(self):
        """Parse and return the frontmatter.

        Deferred until first access so use doesnt need to parse yaml if they only
        want the content
        """
        if self.frontmatter is None:
            return {}

        return yaml.load(self.frontmatter, Loader=yaml.SafeLoader)

    @cached_property
    def content(self):
        """Actual document content.

        This is deferred to when its first accessed so we dont load a large document
        if we only need to check the frontmatter
        """
        return "".join(f"{line}\n" for line in self._line_iter)

    def __getitem__(self, key):
        """Get an item from the documents metadata."""
        return self.metadata[key]

    def __setitem__(self, key, value):
        """Write to the documents metadata."""
        self.metadata[key] = value


def load(stream: IO[str]) -> Document:
    """Load a document from a stream.

    :param stream: The text stream to load from
    """
    line_iter = _read_lines(stream)
    frontmatter = None
    first_line: Optional[str] = next(line_iter, "")

    if first_line == "---":
        frontmatter = "\n".join(_read_frontmatter(line_iter))
    else:
        line_iter = _cons(first_line, line_iter)

    return Document(line_iter, frontmatter)


def loads(s: str) -> Document:
    """Load a document from a string.

    :param s: The string to load
    """
    fp = io.StringIO(s, newline=None)

    return load(fp)
