from django.contrib import admin
from .models import Prompt, GradeSpecificPrompt, SubjectSpecificPrompt, PromptDetail


admin.site.register(Prompt)
admin.site.register(GradeSpecificPrompt)
admin.site.register(SubjectSpecificPrompt)
admin.site.register(PromptDetail)