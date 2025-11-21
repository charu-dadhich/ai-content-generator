from django.core.exceptions import ValidationError
from django import forms
from question_ai.exception import ApiException
from utils import Validator
from .models import User


class SinglePasswordUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, help_text="Must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            if self.request.user.role == 3:
                self.fields['subject'].initial = self.request.user.subject
                self.fields['subject'].disabled = True
                self.fields['role'].initial = 4
                self.fields['role'].disabled = True

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'role', 'is_staff',
            'department', 'subject',
            'is_active', 'is_superuser', 'groups', 'user_permissions'
        )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            Validator.validate_password(password)
        except ApiException as e:
            raise ValidationError("Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one digit, and one special character.")

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        if self.request:
            user.created_by_user = self.request.user
            if self.request.user.role == 3:
                user.subject = self.request.user.subject
        if commit:
            user.save()
        return user
