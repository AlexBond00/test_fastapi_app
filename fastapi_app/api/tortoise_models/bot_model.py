from tortoise import Model, fields


class BotModel(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=64)
    uid = fields.BigIntField(null=False)
    token = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        table = "bot"
