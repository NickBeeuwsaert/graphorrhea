from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError

__version__ = "0.1.0"


def main(global_settings, **settings):
    """
    Create the primary WSGI app.

    This app just routes requests to the frontend or API routes.
    """
    composite_routes = settings.get("composite_routes", None)

    if not composite_routes:
        raise ConfigurationError("No composite routes in composite_routes")

    def app(environ, start_response):
        path_info = environ["PATH_INFO"]

        for route in composite_routes:
            if path_info.startswith(route["prefix"]):
                return route["app"](environ, start_response)

        # If there was no matched prefix, then just use the last route
        return route["app"](environ, start_response)

    return app


def api(global_config, **settings):
    """Create the WSGI app for the V1 API."""
    settings.setdefault("tm.manager_hook", "pyramid_tm.explicit_manager")
    config = Configurator(settings=settings)

    with config:
        config.include("pyramid_tm")
        config.include("pyramid_retry")
        config.include(".openapi")
        config.include(".models")

    return config.make_wsgi_app()


def frontend(global_config, **settings):
    """Create WSGI app for the frontend"""
    settings.setdefault("tm.manager_hook", "pyramid_tm.explicit_manager")
    config = Configurator(settings=settings)

    with config:
        config.include("pyramid_jinja2")
        config.include("pyramid_tm")
        config.include("pyramid_retry")
        config.include(".routes")
        config.include(".models")

        config.scan(".views")

    return config.make_wsgi_app()
