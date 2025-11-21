
from django.contrib import admin
from .models import (
    ServiceGrade,
    Subject,
    Department,
    Standard,
    ServiceType,
    LLMModel,
    Board
)

admin.site.register(ServiceGrade)
admin.site.register(Subject)
admin.site.register(Department)
admin.site.register(Standard)
admin.site.register(ServiceType)
admin.site.register(LLMModel)
admin.site.register(Board)


# class ServiceGradeAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         # Hide model from non-superusers
#         if not request.user.is_superuser:
#             return {}
#         return super().get_model_perms(request)

