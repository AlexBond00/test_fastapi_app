from tortoise import Model, fields


class LegacyMessageModel(Model):
    """Legacy telegram message model."""
    id = fields.BigIntField(pk=True)
    message = fields.ForeignKeyField(
        "plutus.MessageModel", on_delete=fields.CASCADE
    )
    json = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return str(self.message.message_id)

    class Meta:
        table = "legacy_message"
        ordering = ['-created_at']
