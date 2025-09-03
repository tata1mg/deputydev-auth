from enum import Enum

from tortoise import fields

from .base import Base


class Users(Base):
    id = fields.IntField(primary_key=True)
    email = fields.TextField(max_length=1000)
    name = fields.TextField(max_length=1000)
    org_name = fields.TextField(max_length=1000)

    class Meta:
        table = "users"
        unique = (("email",),)

    class Columns(Enum):
        id = ("id",)
        email = ("email",)
        name = ("name",)
        org_name = ("org_name",)
        created_at = ("created_at",)
        updated_at = ("updated_at",)
