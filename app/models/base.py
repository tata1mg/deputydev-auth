from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    """
    Base model class for all database models.

    This class provides common functionality and fields that should
    be available in all models throughout the application.

    Attributes:
        id: Primary key field
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
        is_active: Soft delete flag
    """

    id = fields.IntField(pk=True, description="Primary key")
    created_at = fields.DatetimeField(auto_now_add=True, description="Record creation timestamp")
    updated_at = fields.DatetimeField(auto_now=True, description="Record last update timestamp")

    class Meta:
        abstract = True
