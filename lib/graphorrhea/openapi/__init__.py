from pathlib import Path

import jwt
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

from graphorrhea.models.note import Note
from graphorrhea.security import InvalidAuthorizationError, jwt_exception_view


def note_factory(request):
    try:
        path = request.GET["path"]
    except KeyError:
        raise HTTPBadRequest
    try:
        return Note(request.acidfs.open(path, "r").read())
    except FileNotFoundError:
        raise HTTPNotFound


def includeme(config):
    config.include("pyramid_openapi3")

    openapi_spec = Path(__file__).parent / "openapi.yaml"
    config.pyramid_openapi3_spec(
        str(openapi_spec),
        route="/api/v1/openapi.yaml",
    )
    config.pyramid_openapi3_add_explorer(route="/api/v1/")

    config.scan(".views")

    with config.route_prefix_context("/api/v1/"):
        config.add_route(
            "openapi.view_note",
            "/note",
            request_method="GET",
            factory=note_factory,
        )
        config.add_route("openapi.create_note", "/note", request_method="POST")
        config.add_route("openapi.notebook", "/notebook")

        config.add_route("auth.register", "/auth/register")
        config.add_route("auth.login", "/auth/login")
        config.add_route("auth.renew", "/auth/renew")

        config.add_exception_view(
            jwt_exception_view,
            jwt.InvalidTokenError,
            renderer="json",
        )
        config.add_exception_view(
            jwt_exception_view,
            InvalidAuthorizationError,
            renderer="json",
        )
    # config.add_route("openapi.users", "/users")
    # config.add_route("openapi.user", "/users/{id}")
    # config.add_route("openapi.me", "/me")
    # config.add_route("openapi.directory", "/directory")
    # config.add_route("openapi.note", "/note")
