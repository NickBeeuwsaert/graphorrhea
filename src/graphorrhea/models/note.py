from dataclasses import asdict, dataclass

from pyramid.security import Allow, Authenticated, Deny, Everyone


@dataclass
class Note:
    content: str
    mimetype: str = "text/x-rst"

    # Having four permissions for CRUD is probably unnecessary at this time,
    # since if a user is logged in, it is assumed they are trusted (they own
    # the git repository tracking changes). But in the future I'd like to have
    # finer grained control over resources (e.g. Maybe I want to archive a note,
    # or open the server up to a friend to collaborate on just one note). So,
    # including these four permissions for the future.
    __acl__ = [
        (Allow, Authenticated, "view"),
        (Allow, Authenticated, "create"),
        (Allow, Authenticated, "update"),
        (Allow, Authenticated, "delete"),
    ]

    def __json__(self, request):
        return asdict(self)
