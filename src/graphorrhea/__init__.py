from pyramid.config import Configurator
from pyramid.decorator import reify

__version__ = "0.1.0"


class main:
    def __init__(self, global_settings, **settings):
        self.global_settings = global_settings
        self.settings = settings

    @property
    def _config(self):
        config = Configurator(
            settings={
                "tm.manager_hook": "pyramid_tm.explicit_manager",
                **self.settings,
            }
        )
        with config:
            config.include("pyramid_tm")
            config.include("pyramid_retry")
            config.include(".models")
        return config

    @reify
    def app(self):
        """Handle frontend requests."""
        config = self._config
        with config:
            config.include("pyramid_jinja2")
            config.include(".routes")

            config.scan(".views")

        return config.make_wsgi_app()

    @reify
    def api_app(self):
        """Handle v1 API requests."""
        config = self._config
        with config:
            config.include(".openapi")

        return config.make_wsgi_app()

    def __call__(self, environ, start_response):
        """Route requests to the API or the frontend."""
        path_info = environ["PATH_INFO"]
        app = self.app

        if path_info.startswith("/api"):
            app = self.api_app

        return app(environ, start_response)
