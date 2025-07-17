from django.conf import settings
from django.db import models
from django.utils import timezone


class ImprovementArea(models.Model):
    """Areas in which employees can improve."""

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ImprovementPlan(models.Model):
    """Employee improvement plan model."""

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="improvement_plans"
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="managed_improvement_plans"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.username}'s Improvement Plan: {self.title}"

    def is_active(self):
        return self.status == "active"

    def is_completed(self):
        return self.status == "completed"


class Goal(models.Model):
    """Individual goals within an improvement plan."""

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    improvement_plan = models.ForeignKey(
        ImprovementPlan, on_delete=models.CASCADE, related_name="goals"
    )
    improvement_area = models.ForeignKey(
        ImprovementArea, on_delete=models.CASCADE, related_name="goals"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    success_criteria = models.TextField(help_text="What does success look like for this goal?")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="not_started")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Progress(models.Model):
    """Progress updates for goals."""

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="progress_updates")
    update_text = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Progress Updates"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Update on {self.goal.title} by {self.created_by.username}"


class Resource(models.Model):
    """Resources to help with improvement goals."""

    TYPE_CHOICES = [
        ("article", "Article"),
        ("video", "Video"),
        ("course", "Course"),
        ("book", "Book"),
        ("mentor", "Mentor"),
        ("other", "Other"),
    ]

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
