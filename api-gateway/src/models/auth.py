from tortoise import fields
from tortoise import models


class AuthTokens(models.Model):
    """
    Model for storing users token
    """
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.Users")
    token = fields.CharField(max_length=64, unique=True)
    renew_token = fields.CharField(max_length=64, unique=True)
    expiration = fields.DatetimeField()
    renew_expiration = fields.DatetimeField()
