from tortoise import fields, models


class AbstractBaseModel(models.Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class User(TimestampMixin, AbstractBaseModel):
    vk_id = fields.CharField(max_length=50, unique=True, index=True, null=True)
    ya_id = fields.CharField(max_length=50, unique=True, index=True, null=True)

    username = fields.CharField(max_length=50)
    password_hash = fields.CharField(max_length=128, null=True)

    is_verify = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)

    emails: fields.ReverseRelation["Email"]

    def __str__(self):
        return f'<User id={self.id} username={self.username}>'


class Email(AbstractBaseModel):
    email = fields.CharField(max_length=50, unique=True, index=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User', related_name='emails')
    is_prime = fields.BooleanField(default=False)

    def __str__(self):
        return f'<Email id={self.id} email={self.email} user={self.user}>'

