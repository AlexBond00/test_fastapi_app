from tortoise import Model, fields


class MessageModel(Model):
    id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField()
    message_id = fields.BigIntField()
    json = fields.JSONField()
    is_recieved = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "message"
        orderindg = ['-id']
