import uuid

from pyramid.view import view_config, view_defaults


@view_defaults(route_name="openapi.users", openapi=True, renderer="json")
class UsersEndpoint:
    def __init__(self, request):
        self.request = request

    @view_config(request_method="POST", accept="application/json")
    def create(self):
        return {"id": str(uuid.uuid4())}

    @view_config(request_method="GET")
    def list(self):
        return [{"username": "asdf"}]
