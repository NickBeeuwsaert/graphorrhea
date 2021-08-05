from pyramid.view import view_config, view_defaults

from graphorrhea.resources import Notebook


@view_defaults(
    route_name="openapi.notebooks", accept="application/json", renderer="json"
)
class NotebookEndpoint:
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET", renderer="json", context=Notebook)
    def get(self):
        return self.request.context
