from .schemas import WSGIAppSchema, WSGIFilterSchema, WSGIServerSchema


class WSGIMixin:
    def _get_section(self, section):
        config = self._config
        try:
            return config[section]
        except KeyError:
            raise ValueError(f"No {section!r} section!")

    def _maybe_get_name(self, name):
        if not name:
            name = self.uri.fragment

        if not name:
            name = "main"

        return name

    def _get_app_definition(self, name):
        name = self._maybe_get_name(name)
        schema = WSGIAppSchema()
        apps = self._get_section("applications")

        try:
            app = apps[name]
        except KeyError:
            raise ValueError(f"App {name!r} not found!")

        return schema.deserialize(app)

    def get_wsgi_app(self, name=None, defaults=None):
        settings = self._get_app_definition(name)
        app_factory = settings.pop("use")

        app = app_factory(defaults or {}, **settings)

        return app

    def get_wsgi_app_settings(self, name=None, defaults=None):
        settings = self._get_app_definition(name)

        settings.pop("use")

        return settings

    def get_wsgi_filter(self, name=None, defaults=None):
        schema = WSGIFilterSchema()
        name = self._maybe_get_name(name)
        filters = self._get_section("filters")

        try:
            filter_ = filters[name]
        except KeyError:
            raise ValueError(f"Filter {name!r} not found!")

        filter_settings = schema.deserialize(filter_)
        filter_ = filter_settings.pop("use")

        return filter_

    def get_wsgi_server(self, name=None, defaults=None):
        schema = WSGIServerSchema()
        name = self._maybe_get_name(name)
        servers = self._get_section("servers")

        try:
            server = servers[name]
        except KeyError:
            raise ValueError(f"Server {name!r} not found!")

        server_settings = schema.deserialize(server)
        server = server_settings.pop("use")

        def serve(app):
            return server(app, **server_settings)

        return serve
