from dataclasses import dataclass
from pathlib import PurePosixPath as Path

from acidfs import AcidFS
from pyramid.security import Allow, Authenticated


@dataclass
class Note:
    acidfs: AcidFS
    path: str
    mimetype: str = "text/x-rst"

    # Having four permissions for CRUD is probably unnecessary at this time,
    # since if a user is logged in, it is assumed they are trusted (they own
    # the git repository tracking changes). But in the future I'd like to have
    # finer grained control over resources (e.g. Maybe I want to archive a note
    # or open the server up to a friend to collaborate on just one note). So,
    # including these four permissions for the future.
    __acl__ = [
        (Allow, Authenticated, "view"),
        (Allow, Authenticated, "create"),
        (Allow, Authenticated, "update"),
        (Allow, Authenticated, "delete"),
    ]

    def __json__(self, request):
        return {"path": self.path, "mimetype": self.mimetype}

    @property
    def content(self):
        with self.acidfs.open(self.path, "r") as fp:
            return fp.read()

    def __getitem__(self, key):
        """Notes cannot have children."""
        raise KeyError


@dataclass
class Notebook:
    acidfs: AcidFS
    path: str

    __acl__ = [
        (Allow, Authenticated, "create"),
        (Allow, Authenticated, "update"),
        (Allow, Authenticated, "delete"),
    ]

    def __json__(self, request):
        path = Path(self.path)
        return {
            "path": self.path,
            "entries": [
                {
                    "type": "notebook"
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
    acidfs = request.acidfs
    resource_notebook = Notebook(acidfs, "/")
    path = Path(request.GET.get("path", "/"))

    for component in path.parts[1:]:
        try:
            resource_notebook = resource_notebook[component]
        except KeyError:
            break

    return resource_notebook
