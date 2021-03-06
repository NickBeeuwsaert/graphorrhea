from pyramid.view import view_config


@view_config(route_name="index", renderer="string")
def index(request):
    return "Hello, world!"
