from tortoise import Model, fields


class FileModel(Model):
    """File model."""
    id: int = fields.BigIntField(pk=True)
    bot_id: int = fields.BigIntField()
    chat_id: int = fields.BigIntField()
    message_id: int = fields.BigIntField()
    path: str = fields.CharField(max_length=250)
    content_type: str = fields.CharField(max_length=50)

    def __str__(self):
        return self.path

    class Meta:
        table = "file"
