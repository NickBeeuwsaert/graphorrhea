from collections.abc import Mapping
from functools import singledispatch


@singledispatch
def interpolate(value, **kwargs):
    return value


@interpolate.register
def _interpolate_string(value: str, **kwargs):
    return value.format(**kwargs)


@interpolate.register
def _interpolate_mapping(mapping: Mapping, **kwargs):
    return {key: interpolate(value, **kwargs) for key, value in mapping.items()}


@interpolate.register
def _interpolate_list(items: list, **kwargs):
    return [interpolate(item, **kwargs) for item in items]


@interpolate.register
def _interpolate_tuple(items: tuple, **kwargs):
    return tuple(interpolate(item, **kwargs) for item in items)
