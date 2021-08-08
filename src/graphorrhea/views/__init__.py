import jwt

from graphorrhea.security import jwt_exception_view


def includeme(config):
    config.add_exception_view(jwt_exception_view, jwt.DecodeError)
    config.pyramid_openapi3_add_explorer(route="/api/v1")
