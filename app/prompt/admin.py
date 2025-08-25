from django.contrib import admin
from .models import Prompt, GradeSpecificPrompt, SubjectSpecificPrompt


admin.site.register(Prompt)
admin.site.register(GradeSpecificPrompt)
admin.site.register(SubjectSpecificPrompt)