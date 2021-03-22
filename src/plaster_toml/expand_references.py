from functools import singledispatch


@singledispatch
def expand_references(value, **kwargs):
    return value


@expand_references.register(dict)
def _expand_dict(value: dict, *, applications):
    try:
        ref = value.pop("$ref")
    except KeyError:
        return {
            key: expand_references(value, applications=applications)
            for key, value in value.items()
        }
    return applications(ref, value)


@expand_references.register(list)
def _expand_list(value: list, **kwargs):
    return [expand_references(item, **kwargs) for item in value]
