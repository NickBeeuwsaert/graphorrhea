from pathlib import PurePosixPath as Path

import transaction
from pyramid.view import view_config, view_defaults
from webob.exc import HTTPBadRequest

from graphorrhea.resources import Note, Notebook


@view_defaults(
    route_name="openapi.files",
    renderer="json",
    openapi=True,
)
class FilesAPI:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(
        request_method="GET",
        context=Note,
        permission="view",
    )
    def get_note(self):
        return self.context

    @view_config(
        request_method="GET",
        context=Notebook,
        permission="view",
    )
    def get_notebook(self):
        return self.context

    @view_config(
        request_method="POST",
        context=Notebook,
        permission="write",
    )
    def create_entry(self):
        acidfs = self.request.acidfs
        payload = self.request.json
        content = payload.get("content", None)

        try:
            entry_type = payload["type"]
            name = payload["name"]
        except KeyError:
            raise HTTPBadRequest

        # Because of the way git works, we can't commit an empty directory
        # So, when we create the directory, we are actually just creating
        # an empty file in that directory
        if entry_type == "directory":
            content = ""
            name = Path(name) / "empty"

        path = Path(self.context.path) / name
        acidfs.mkdirs(str(path.parent))

        with acidfs.open(str(path), "w") as fp:
            fp.write(content)
        return dict(success=True)

    @view_config(
        request_method="PUT",
        context=Note,
        permission="write",
    )
    def update_note(self):
        acidfs = self.request.acidfs
        payload = self.request.json
        try:
            content = payload["content"]
        except KeyError:
            raise HTTPBadRequest

        with acidfs.open(self.context.path, "w") as fp:
            fp.write(content)
        return dict(success=True)
