from enum import Enum

from tortoise import fields

from .base import Base


class Teams(Base):
    id = fields.BigIntField(primary_key=True)
    name = fields.TextField(max_length=1000)
    llm_model = fields.CharField(null=True, max_length=1000)

    class Meta:
        table = "teams"

    class Columns(Enum):
        id = ("id",)
        name = ("name",)
        llm_model = ("llm_model",)
        created_at = ("created_at",)
        updated_at = ("updated_at",)
