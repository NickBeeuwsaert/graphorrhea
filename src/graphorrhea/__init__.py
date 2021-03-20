from pyramid.config import Configurator

__version__ = "0.1.0"


def main(global_config, **settings):
    """Create" the primary WSGI app."""
    settings.setdefault("tm.manager_hook", "pyramid_tm.explicit_manager")
    config = Configurator(settings=settings)

    with config:
        config.include("pyramid_jinja2")
        config.include("pyramid_tm")
        config.include("pyramid_retry")
        config.include(".routes")
        config.include(".openapi")
        config.include(".models")

        config.scan(".views")

    return config.make_wsgi_app()
