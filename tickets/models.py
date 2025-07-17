from django.db.model import (
    Model, CharField, SmallAutoField, JSONField
)


class Ticket(Model):
    title = CharField(max_length=200, null=False,  blank=False)
    prefix = CharField(max_length=20, null=False,  blank=False)
    number = SmallAutoField()
    description = CharField(max_length=200, null=False, blank=False)
    status = CharField(max_length=20, null=False, blank=False)
    tags = JSONField(null=False, blank=False, default=list)

