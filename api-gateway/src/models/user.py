from tortoise import fields, models


class Users(models.Model):
    """
    Users model
    """
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=64, unique=True)
    name = fields.CharField(max_length=128, unique=True)
    password_hash = fields.CharField(max_length=60, null=True)


class OAuthClient(models.Model):
    """
    User's OAuth  athentications
    """
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.Users")
    service = fields.CharField(max_length=64)


