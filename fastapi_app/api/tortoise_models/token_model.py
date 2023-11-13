import datetime
import uuid

from tortoise import Model, fields


class Token(Model):
    """Token model."""
    id = fields.BigIntField(pk=True)
    token = fields.UUIDField(index=True, default=uuid.uuid4())
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "token"

    def is_expired(self):
        """Check if token expired."""
        timedelta_days = (datetime.datetime.now() - self.updated_at).day
        return timedelta_days >= 7
