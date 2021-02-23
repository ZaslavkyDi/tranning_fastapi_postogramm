from typing import Any

from sqlalchemy.ext.declarative.api import as_declarative, declared_attr


@as_declarative()
class Base(object):
    id: Any

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
