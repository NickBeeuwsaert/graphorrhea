from zope.interface import Interface


class IDatabaseSession(Interface):
    """Marker class for SQLAlchemy database sessions."""
