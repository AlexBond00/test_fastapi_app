from tortoise import Model, fields


class DialogueModel(Model):
    """Dialogue model."""
    id = fields.BigIntField(pk=True)
    bot_id = fields.BigIntField()
    chat_id = fields.BigIntField()
    updated_at = fields.DatetimeField()

    def __str__(self):
        return f"Dialogue (bot {self.bot_id} chat{self.chat_id})"

    class Meta:
        table = "dialogue"
        ordering = ['-updated_at']
