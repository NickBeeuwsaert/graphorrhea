import pytest

from acidfs import AcidFS, InvalidPathException


@pytest.fixture
def acid_fs():
    return AcidFS("some_repo")


def test_file_open(acid_fs):
    assert acid_fs.open("a/b/c", None) == ("a", "b", "c")


@pytest.mark.parametrize(
    ("path", "reason"),
    [
        # Anything with dot-files
        ("../", "dot-files"),
        ("another/path/..", "dot-files"),
        ("/the/dot-file/is/../in/the/middle", "dot-files"),
        # Not testing with '.' since pathlib strips that out for us.
        (".git", "dot-files"),
        # invalid characters
        ("hello?", "invalid-character"),
        ("it's me", "invalid-character"),
        ("I was wondering \\ if after all", "invalid-character"),
        ("these years you'd like to meet?", "invalid-character"),
        # Reserved filenames
        ("CON", "reserved-name"),
        ("NUL", "reserved-name"),
    ],
)
def test_dot_files_forbidden(acid_fs, path, reason):
    with pytest.raises(InvalidPathException) as exc_info:
        acid_fs.open(path, None)
    assert exc_info.value.reason == reason
