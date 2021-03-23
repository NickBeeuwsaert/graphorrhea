from .autowired_view import AutowiredView


class ViewMapper:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, view):
        return AutowiredView(view, self.kwargs.get("attr"))
