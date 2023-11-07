from tortoise import Model, fields


class DialogueModel(Model):
    id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField()
    bot_id = fields.BigIntField()
    updated_at = fields.DatetimeField(null=True)

    class Meta:
        table = "dialogue"
        orderindg = ['-updated_at']
