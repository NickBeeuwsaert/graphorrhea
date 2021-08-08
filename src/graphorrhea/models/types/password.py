from functools import cached_property
from typing import Protocol, Union

from passlib.context import LazyCryptContext
from sqlalchemy import Text, TypeDecorator, event
from sqlalchemy.orm import mapper


class IPassword(Protocol):
    hash: str

    def __init__(self, hash: str):
        pass

    def __eq__(self, rhs) -> bool:
        pass


class PasswordType(TypeDecorator):
    impl = Text

    def __init__(self, **kwargs):
        super().__init__()
        self.context = LazyCryptContext(**kwargs)

    @cached_property
    def _password_type(self) -> type[IPassword]:
        context = self.context

        class Password(IPassword):
            def __init__(self, password_hash):
                self.hash = password_hash

            def __eq__(self, rhs):
                return context.verify(rhs, self.hash)

        return Password

    def process_bind_param(self, value, dialect) -> str:
        return self.coerce(value).hash

    def process_result_value(self, value, dialect) -> IPassword:
        return self._password_type(value)

    def coerce(self, value: Union[IPassword, str]) -> IPassword:
        if isinstance(value, self._password_type):
            return value

        return self._password_type(self.context.hash(value))


@event.listens_for(mapper, "mapper_configured")
def mapper_configured(mapper, cls):
    if mapper.non_primary:
        return

    for prop in mapper.column_attrs:
        column = getattr(cls, prop.key)

        if not isinstance(column.type, PasswordType):
            continue

        def set(target, value, oldvalue, initiator):
            return column.type.coerce(value)

        event.listen(column, "set", set, retval=True)
