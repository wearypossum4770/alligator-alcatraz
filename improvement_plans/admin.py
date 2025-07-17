from django.contrib import admin

from .models import Goal, ImprovementArea, ImprovementPlan, Progress, Resource


@admin.register(ImprovementArea)
class ImprovementAreaAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 1
    fields = ("title", "improvement_area", "priority", "status", "due_date")


@admin.register(ImprovementPlan)
class ImprovementPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "employee", "manager", "status", "start_date", "end_date")
    list_filter = ("status", "start_date", "manager")
    search_fields = ("title", "description", "employee__username", "employee__email")
    inlines = [GoalInline]
    date_hierarchy = "start_date"


class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 1
    fields = ("update_text", "created_by", "created_at")
    readonly_fields = ("created_at",)


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1
    fields = ("title", "resource_type", "url", "added_by")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "improvement_plan",
        "improvement_area",
        "priority",
        "status",
        "due_date",
    )
    list_filter = ("status", "priority", "improvement_area", "due_date")
    search_fields = ("title", "description", "success_criteria")
    inlines = [ProgressInline, ResourceInline]
    date_hierarchy = "due_date"


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("goal", "created_by", "created_at")
    list_filter = ("created_at", "created_by")
    search_fields = ("update_text", "goal__title")
    date_hierarchy = "created_at"


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "goal", "resource_type", "added_by", "created_at")
    list_filter = ("resource_type", "created_at", "added_by")
    search_fields = ("title", "description", "goal__title")
    date_hierarchy = "created_at"
