from importlib.resources import path

from graphorrhea.resources import resource_factory


def includeme(config):
    config.include("graphorrhea.views")
    config.scan("graphorrhea.views")

    with path("graphorrhea", "openapi.yaml") as openapi_spec:
        config.pyramid_openapi3_spec(
            str(openapi_spec),
            route="/api/v1/openapi.yaml",
        )

    with config.route_prefix_context("/api/v1"):
        config.add_route("openapi.note", "/note", factory=resource_factory)
        config.add_route(
            "openapi.notebooks",
            "/notebook",
            factory=resource_factory,
        )

        config.add_route("auth.register", "/auth/register")
        config.add_route("auth.login", "/auth/login")
        config.add_route("auth.renew", "/auth/renew")
