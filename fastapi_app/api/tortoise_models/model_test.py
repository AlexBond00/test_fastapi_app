from tortoise import Model, fields


class ModelTest(Model):
    id = fields.BigIntField(pk=True)

    class Meta:
        table = "table_test"
