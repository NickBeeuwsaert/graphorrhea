from pyramid.config import Configurator
from pyramid.decorator import reify

__version__ = "0.1.0"


def frontend(global_settings, **settings):
    settings = {
        "tm.manager_hook": "pyramid_tm.explicit_manager",
        **settings,
    }
    config = Configurator(settings=settings)
    with config:
        config.include("pyramid_jinja2")
        config.include("pyramid_tm")
        config.include("pyramid_retry")
        config.include(".models")
        config.include(".routes")

        config.scan(".views")

    return config.make_wsgi_app()


def api(global_settings, **settings):
    settings = {
        "tm.manager_hook": "pyramid_tm.explicit_manager",
        **settings,
    }
    config = Configurator(settings=settings)
    with config:
        config.include("pyramid_tm")
        config.include("pyramid_retry")
        config.include(".models")
        config.include(".routes")
        config.include(".openapi")

    return config.make_wsgi_app()


class main:
    def __init__(self, global_settings, **settings):
        self.app = frontend(global_settings, **settings)
        self.api_app = api(global_settings, **settings)

    def __call__(self, environ, start_response):
        """Route requests to the API or the frontend."""
        path_info = environ["PATH_INFO"]
        app = self.app

        if path_info.startswith("/api"):
            app = self.api_app

        return app(environ, start_response)
