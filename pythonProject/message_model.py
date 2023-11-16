from tortoise import Model, fields


class MessageModel(Model):
    """Telegram message model."""
    id = fields.BigIntField(pk=True)
    bot_id = fields.BigIntField()
    chat_id = fields.BigIntField()
    message_id = fields.BigIntField()
    json = fields.JSONField()
    is_edited = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Actual message (bot{self.bot_id} chat{self.chat_id} "
            f"message{self.message_id})"
        )

    class Meta:
        table = "message"
        ordering = ['-created_at']
