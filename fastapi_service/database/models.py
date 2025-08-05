import datetime
import typing

import sqlalchemy
import sqlalchemy.orm

intpk = typing.Annotated[int, sqlalchemy.orm.mapped_column(primary_key=True)]
created_at = typing.Annotated[
    datetime.datetime,
    sqlalchemy.orm.mapped_column(
        server_default=sqlalchemy.text("TIMEZONE('utc', now())")
    ),
]
updated_at = typing.Annotated[
    datetime.datetime,
    sqlalchemy.orm.mapped_column(
        server_default=sqlalchemy.text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
]


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


class RequestLog(Base):
    __tablename__ = "request_logs"

    id: sqlalchemy.orm.Mapped[intpk]

    path = sqlalchemy.Column(sqlalchemy.String(255))
    ip_address = sqlalchemy.Column(sqlalchemy.String(45))
    user_agent = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    accept_language = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    status_code = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    response_time_ms = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]
