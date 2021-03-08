from pathlib import Path


def includeme(config):
    config.include("pyramid_openapi3")

    openapi_spec = Path(__file__).parent / "openapi.yaml"
    config.pyramid_openapi3_spec(str(openapi_spec), route="/api/v1/openapi.yaml")
    config.pyramid_openapi3_add_explorer(route="/api/v1/")

    config.scan(".views")

    with config.route_prefix_context("/api/v1/"):
        config.add_route("openapi.users", "/users")
        config.add_route("openapi.user", "/users/{id}")
        config.add_route("openapi.me", "/me")
        config.add_route("openapi.directory", "/directory")
        config.add_route("openapi.note", "/note")
