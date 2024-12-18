from enum import Enum


class Role(Enum):
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"


class Status(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class tasksType(Enum):
    TEXT = "TEXT"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"


class MessageCode(Enum):
    SUCCESS = "S20000"
    CREATED = "S20201"
    ACCEPTED = "S20202"
    NO_DATA = "S20204"
    ERROR = "S20404"
    UNAUTHORIZED = "S20401"
    FORBIDDEN = "S20403"
    NOT_FOUND = "S20404"
