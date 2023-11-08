from tortoise import Model, fields


class BotModel(Model):
    id = fields.BigIntField(pk=True)
    token = fields.CharField(max_length=50)
    tg_bot_id = fields.BigIntField()

    class Meta:
        table = "bot"
