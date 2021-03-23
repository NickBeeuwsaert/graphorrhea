from functools import partial
from inspect import Parameter, isclass, signature
from typing import Annotated, get_args, get_origin

from zope.interface import Interface
from zope.interface.interfaces import ComponentLookupError


def _get_parameters(parameters, kind):
    return (parameter for parameter in parameters.values() if parameter.kind is kind)


def _get_annotation_args(annotation):
    if get_origin(annotation) is Annotated:
        return get_args(annotation)
    return (annotation,)


def _find_parameter_interface(parameter):
    annotation = parameter.annotation

    for annotation in _get_annotation_args(annotation):
        if issubclass(annotation, Interface):
            return annotation
    raise ValueError(f"{parameter.name!r} doesn't have a zope Interface!")


def _find_utility(registry, iface, name):
    try:
        utility = registry.getUtility(iface, name)
    except ComponentLookupError:
        utility = registry.getUtility(iface)
    return utility


def _find_adapter(registry, iface, request, name):
    try:
        adapter = registry.getAdapter(request, iface, name)
    except ComponentLookupError:
        adapter = registry.getAdapter(request, iface)
    return adapter


def _map_dependencies(parameters, registry, request):
    for parameter in parameters:
        iface = _find_parameter_interface(parameter)

        try:
            dependency = _find_utility(registry, iface, parameter.name)
        except ComponentLookupError:
            dependency = _find_adapter(registry, iface, request, parameter.name)

        yield dependency


def _map_matchdict(fn, matchdict):
    fn_signature = signature(fn)

    for name, parameter in fn_signature.parameters.items():
        try:
            value = matchdict[name]
        except KeyError:
            continue
        yield (name, value)


class ViewMapper:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, view):
        view_signature = signature(view)

        # The number of positional-only arguments should be less than or equal to 2
        # to map to the usual pyramid (context, request, /) or (request, /) parameters
        count_positional_only = len(
            list(_get_parameters(view_signature.parameters, Parameter.POSITIONAL_ONLY))
        )
        # Use the keyword-or-positional arguments for dependency injection
        dependency_parameters = list(
            _get_parameters(view_signature.parameters, Parameter.POSITIONAL_OR_KEYWORD)
        )

        dependency_mapper = partial(_map_dependencies, dependency_parameters)

        if count_positional_only > 2:
            raise ValueError(
                f"View {view.__name__!r} should accept 1 or 2 positional-only "
                "arguments."
            )

        def wrapper(context, request):
            dependencies = dependency_mapper(request.registry, request)

            mapped_view = view

            if count_positional_only == 1:
                mapped_view = partial(mapped_view, request)
            if count_positional_only == 2:
                mapped_view = partial(mapped_view, context, request)

            if isclass(view):
                mapped_view = mapped_view(*dependencies)
                mapped_view = getattr(mapped_view, self.kwargs["attr"])
            else:
                mapped_view = partial(mapped_view, *dependencies)

            kwargs = dict(_map_matchdict(mapped_view, request.matchdict))

            return mapped_view(**kwargs)

        return wrapper
