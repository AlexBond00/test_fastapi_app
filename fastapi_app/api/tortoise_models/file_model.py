from tortoise import Model, fields


class FileModel(Model):
    """File model."""
    id: int = fields.BigIntField(pk=True)
    path: str = fields.CharField(max_length=250)
    message_id: int = fields.BigIntField()

    class Meta:
        table = "file"
