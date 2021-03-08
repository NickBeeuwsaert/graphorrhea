import logging

from pyramid.view import view_config

logger = logging.getLogger(__name__)


@view_config(route_name="index", renderer="string")
def index(request):
    logger.info("Hello!")
    return "Hello, world!"
