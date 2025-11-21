from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import SinglePasswordUserCreationForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = SinglePasswordUserCreationForm

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form
            form = super().get_form(request, obj, **kwargs)
        
            class FormWithRequest(form):
                def __init__(self_inner, *args, **inner_kwargs):
                    inner_kwargs['request'] = request
                    super().__init__(*args, **inner_kwargs)
                    if request.user.role == 2 and 'role' in self_inner.fields:
                        self_inner.fields['role'].choices = [
                            choice for choice in self_inner.fields['role'].choices if choice[0] != 1
                        ]
            return FormWithRequest
        else:
            form = super().get_form(request, obj, **kwargs)

            class WrappedForm(form):
                def __init__(self_inner, *args, **inner_kwargs):
                    super().__init__(*args, **inner_kwargs)
                    if request.user.role == 3:
                        if 'role' in self_inner.fields:
                            self_inner.fields['role'].disabled = True
                        if 'subject' in self_inner.fields:
                            self_inner.fields['subject'].disabled = True
                        if 'department' in self_inner.fields:
                            self_inner.fields['department'].disabled = True
                    if request.user.role == 2 and 'role' in self_inner.fields:
                        self_inner.fields['role'].choices = [
                            choice for choice in self_inner.fields['role'].choices if choice[0] != 1
                        ]
            return WrappedForm

    base_fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'department', 'subject', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name',
                'email',
                'role',
                'is_staff',
                'password',
                'department',
                'subject'
            ),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'role', 'department', 'subject')
    list_select_related = ('department', 'subject')
    search_fields = ('email',)
    ordering = ('-created_at',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(self.base_fieldsets)

        if not request.user.is_superuser and request.user.is_staff:
            if request.user.role == 2:
                for i, (title, fieldset) in enumerate(fieldsets):
                    if title == _('Permissions'):
                        fields = list(fieldset['fields'])
                        fields = [f for f in fields if f == 'is_staff']
                        if fields:
                            fieldsets[i] = (title, {'fields': tuple(fields)})
                        else:
                            fieldsets.pop(i)
                        break
            else:
                fieldsets = [fs for fs in fieldsets if fs[0] != _('Permissions')]
        return fieldsets
    
    def has_delete_permission(self, request, obj=None):
        if request.user.role in [2, 3]:
            return False
        return super().has_delete_permission(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.is_staff:
            if request.user.groups.filter(id=1).exists():
                qs = User.objects.get_users_by_department(request.user.department)
            else:
                qs = User.objects.get_users_by_department_and_subject(request.user.department, request.user.subject)
        return qs
