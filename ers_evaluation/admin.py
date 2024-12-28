from django.contrib import admin
from .models import Evaluation, Recommendation

MAX_EVALUATIONS = 3

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("rating", "comment", "user_id")
    list_filter = ("user_id",)
    change_list_template = "admin/evaluation_changelist.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['max_evaluations'] = MAX_EVALUATIONS
        return super(EvaluationAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(Recommendation)