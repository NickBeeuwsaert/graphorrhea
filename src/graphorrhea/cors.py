from pyramid.events import NewResponse
from pyramid.security import NO_PERMISSION_REQUIRED


class CORSPreflightPredicate:
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return f"cors_preflight = {bool(self.val)!r}"

    phash = text

    def __call__(self, context, request):
        return all(
            [
                self.val,
                request.method == "OPTIONS",
                "Origin" in request.headers,
                "Access-Control-Request-Method" in request.headers,
            ]
        )


def cors_options_view(request):
    response = request.response
    if "Access-Control-Request-Headers" in request.headers:
        response.status = 204
        response.headers["Access-Control-Allow-Methods"] = ", ".join(
            ["POST", "PUT", "GET", "OPTIONS", "HEAD", "DELETE"]
        )
        response.headers["Access-Control-Allow-Headers"] = ", ".join(
            ["Content-Type", "Accept", "Authorization", "X-TEST"]
        )

        return response
    return response


def add_cors_preflight_handler(config):
    config.add_view(
        cors_options_view,
        route_name="cors-options-preflight",
        permission=NO_PERMISSION_REQUIRED,
    )
    config.add_route(
        "cors-options-preflight",
        "/{catch_all:.*}",
        cors_preflight=True,
    )


def add_cors_to_response(event):
    request = event.request
    response = event.response

    if "Origin" not in request.headers:
        return
    response.headers["Access-Control-Allow-Methods"] = ", ".join(
        ["POST", "PUT", "GET", "OPTIONS", "HEAD", "DELETE"]
    )
    response.headers["Access-Control-Expose-Headers"] = ", ".join(
        ["Content-Type", "Accept", "Content-Length", "Authorization", "X-TEST"]
    )
    response.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]


def includeme(config):
    config.add_directive(
        "add_cors_preflight_handler",
        add_cors_preflight_handler,
    )
    config.add_route_predicate("cors_preflight", CORSPreflightPredicate)
    config.add_subscriber(add_cors_to_response, NewResponse)
