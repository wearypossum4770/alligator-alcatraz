from django import forms

from .models import Goal, ImprovementArea, ImprovementPlan, Progress, Resource


class ImprovementPlanForm(forms.ModelForm):
    class Meta:
        model = ImprovementPlan
        fields = ["employee", "title", "description", "start_date", "end_date", "status"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = [
            "improvement_area",
            "title",
            "description",
            "success_criteria",
            "priority",
            "status",
            "due_date",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
            "success_criteria": forms.Textarea(attrs={"rows": 3}),
        }


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ["update_text"]
        widgets = {
            "update_text": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Describe the progress made..."}
            ),
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "description", "url", "resource_type"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class ImprovementAreaForm(forms.ModelForm):
    class Meta:
        model = ImprovementArea
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
