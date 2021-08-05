from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config, view_defaults

from graphorrhea.resources import Note, Notebook


@view_defaults(
    route_name="openapi.note",
    accept="application/json",
    renderer="json",
)
class NoteEndpoint:
    def __init__(self, request):
        self.request = request

    def _write_note(self, path, content):
        acidfs = self.request.acidfs
        try:
            fp = acidfs.open(path, "w")
            fp.write(content)
        except FileNotFoundError as e:
            raise HTTPBadRequest from e
        finally:
            fp.close()

    @view_config(
        request_method="POST",
        context=Notebook,
    )
    def post(self):
        path = self.request.GET["path"]
        acidfs = self.request.acidfs

        if acidfs.exists(path):
            raise HTTPBadRequest("Note already exists")

        return dict(
            status="created",
        )

    @view_config(request_method="PUT", context=Note)
    def put(self):
        path = self.request.GET["path"]
        acidfs = self.request.acidfs

        if not acidfs.exists(path):
            raise HTTPNotFound("Note doesn't exist")

        self._write_note(path, self.request.json["content"])

        return dict(
            status="updated",
        )

    @view_config(
        request_method="GET",
        # permission="view",
        context=Note,
    )
    def get(self):
        return self.request.context
