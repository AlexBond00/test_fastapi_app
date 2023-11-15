from tortoise import Model, fields


class BotModel(Model):
    """Telegram bot model."""
    id = fields.BigIntField(pk=True)
    title = fields.CharField(max_length=64)
    token = fields.CharField(max_length=128)
    uid = fields.BigIntField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        table = "bot"
