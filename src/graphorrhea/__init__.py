from pyramid.config import Configurator

__version__ = "0.1.0"


def main(global_config, **settings):
    """Create" the primary WSGI app."""
    config = Configurator(settings=settings)

    with config:
        config.include("pyramid_jinja2")
        config.include(".routes")
        config.include(".openapi")

        config.scan(".views")

    return config.make_wsgi_app()
