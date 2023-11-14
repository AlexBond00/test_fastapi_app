from tortoise import Model, fields


class LegacyMessageModel(Model):
    """Legacy telegram message model."""
    id = fields.BigIntField(pk=True)
    bot_id = fields.BigIntField()
    chat_id = fields.BigIntField()
    message_id = fields.BigIntField()
    json = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Legacy message (bot{self.bot_id} chat{self.chat_id} "
            f"message{self.message_id})"
        )

    class Meta:
        table = "legacy_message"
        ordering = ['created_at']
