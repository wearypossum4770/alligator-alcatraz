from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    Model,
    TextChoices,
    TextField,
)
from django.utils import timezone


StatusChoice = {
    "approved": "Approved",
    "archived": "Archived",
    "cancelled": "Cancelled",
    "completed": "Completed",
    "deleted": "Deleted",
    "draft": "Draft",
    "published": "Published",
    "rejected": "Rejected",
    "submitted": "Submitted",
}


class ImprovementPlan(Model):
    """
    Employee Improvement Plan
    """

    employee = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="subject")
    manager = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="planner")
    title = CharField(max_length=200)
    description = TextField()
    start_date = DateField(default=timezone.now)
    end_date = DateField(null=True, blank=True)
    status = CharField(max_length=20, choices=StatusChoice, default=StatusChoice["draft"])
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.username}'s Improvement Plan: {self.title}"

    def archive(self):
        match self.status:
            case (
                StatusChoice.get("deleted")
                | StatusChoice.get("cancelled")
                | StatusChoice.get("completed")
                | StatusChoice.get("approved") | StatusChoice.get('archived')
            ):
                pass

    def publish_draft(self):
        match self.status:
            case StatusChoice.get("draft"):
                self.status = StatusChoice.get("published")
            case _:
                pass
