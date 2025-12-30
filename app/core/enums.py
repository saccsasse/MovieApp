from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class AuditAction(str, Enum):
    CREATE_USER = "CREATE_USER"
    DELETE_USER = "DELETE_USER"
    PROMOTE_USER = "PROMOTE_USER"
    BAN_USER = "BAN_USER"