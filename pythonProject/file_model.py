from tortoise import Model, fields


class FileModel(Model):
    """File model."""
    id: int = fields.BigIntField(pk=True)
    path: str = fields.CharField(max_length=250)
    message_id: int = fields.BigIntField()

    def __str__(self):
        return self.path

    class Meta:
        table = "file"
