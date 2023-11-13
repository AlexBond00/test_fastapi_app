from tortoise import Model, fields


class LegacyMessageModel(Model):
    id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField()
    bot_id = fields.BigIntField()
    message_id = fields.BigIntField()
    json = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "legacy_message"
        ordering = ['created_at']
