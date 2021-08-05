from pyramid.config import Configurator

__version__ = "0.1.0"


def main(global_settings, **settings):
    with Configurator(settings=settings) as config:
        # Enable transaction support (Failed operations will be rolled
        # back, in AcidFS and in the database)
        config.include("pyramid_tm")
        # Enable retrying requests on error
        config.include("pyramid_retry")
        config.include("pyramid_openapi3")

        config.include("graphorrhea.security")
        config.include("graphorrhea.models")
        config.include("graphorrhea.routes")

        return config.make_wsgi_app()
