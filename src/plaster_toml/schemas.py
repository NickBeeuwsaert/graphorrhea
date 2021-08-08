import colander

__all__ = ("WSGIServerSchema", "WSGIAppSchema", "WSGIFilterSchema")


class WSGIServerSchema(colander.Schema):
    use = colander.SchemaNode(colander.GlobalObject(None))

    def schema_type(self):
        return colander.Mapping(unknown="preserve")


class WSGIAppSchema(colander.Schema):
    use = colander.SchemaNode(colander.GlobalObject(None))

    def schema_type(self):
        return colander.Mapping(unknown="preserve")


class WSGIFilterSchema(colander.Schema):
    use = colander.SchemaNode(colander.GlobalObject(None))

    def schema_type(self):
        return colander.Mapping(unknown="preserve")
