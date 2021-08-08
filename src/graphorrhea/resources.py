from dataclasses import dataclass
from pathlib import PurePosixPath as Path

from acidfs import AcidFS
from pyramid.security import Allow, Authenticated
from zope.interface import implementer

from graphorrhea.interfaces import IGitResource


@implementer(IGitResource)
class RootGitResourceFactory:
    def __init__(self, request):
        self.acidfs = request.acidfs


@dataclass
class Note:
    acidfs: AcidFS
    path: str
    mimetype: str = "text/x-rst"

    __acl__ = [
        (Allow, Authenticated, "view"),
        (Allow, Authenticated, "write"),
        (Allow, Authenticated, "delete"),
    ]

    def __json__(self, request):
        return {
            "type": "note",
            "path": self.path,
            "mimetype": self.mimetype,
            "content": self.content,
        }

    @property
    def content(self):
        with self.acidfs.open(self.path, "r") as fp:
            return fp.read()

    @content.setter
    def content(self, contents):
        with self.acidfs.open(self.path, "w") as fp:
            fp.write(contents)

    def __getitem__(self, key):
        """Notes cannot have children."""
        raise KeyError


@dataclass
class Notebook:
    acidfs: AcidFS
    path: str

    __acl__ = [
        (Allow, Authenticated, "view"),
        (Allow, Authenticated, "write"),
        (Allow, Authenticated, "delete"),
    ]

    def __json__(self, request):
        path = Path(self.path)
        return {
            "type": "directory",
            "path": self.path,
            "entries": [
                {
                    "type": "directory"
                    if self.acidfs.isdir(str(path / name))
                    else "note",
                    "name": name,
                }
                for name in self.acidfs.listdir(str(path))
            ],
        }

    def __getitem__(self, key):
        path = str(Path(self.path) / key)

        if not self.acidfs.exists(path):
            raise KeyError

        if self.acidfs.isdir(path):
            return Notebook(self.acidfs, path)

        return Note(self.acidfs, path)


def resource_factory(request):
    return request.acidfs


# def resource_factory(request):
#     acidfs = request.acidfs
#     resource_notebook = Notebook(acidfs, "/")
#     path = Path(request.GET.get("path", "/"))

#     for component in path.parts[1:]:
#         try:
#             resource_notebook = resource_notebook[component]
#         except KeyError:
#             break

#     return resource_notebook
