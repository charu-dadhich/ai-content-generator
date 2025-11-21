from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
    Group
)
from app.base.models import BaseModel
from utils import (
    Choice,
    Helper
)


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 1)
        self.create_user(email, password, **extra_fields)

    def get_by_pk(self, pk):
        return self.filter(id=pk).first()

    def get_by_email(self, email):
        return self.filter(email=email).first()

    def get_users_by_department(self, department):
        return self.filter(department=department).order_by('-created_at')

    def get_users_by_department_and_subject(self, department, subject):
        return self.filter(department=department, subject=subject).order_by('-created_at')


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        (1, 'Super Admin'),
        (2, 'HOD'),
        (3, 'Team Leader'),
        (4, 'Content Creator')
    ]
 
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=4)
    department = models.ForeignKey('utils.Department', on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey('utils.Subject', on_delete=models.CASCADE, null=True, blank=True)
    created_by_user = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    profile_pic = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    generation_attempts = models.IntegerField(default=0)
    # regeneration_attempts = models.IntegerField(default=0)
    last_generation_attempt_at = models.DateTimeField(null=True, blank=True)
    # last_regeneration_attempt_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.role == 3:
            team_leader_group, _ = Group.objects.get_or_create(name='TL')
            if not self.groups.filter(name='TL').exists():
                self.groups.add(team_leader_group)

        elif self.role == 2:
            hod_group, _ = Group.objects.get_or_create(name='HOD')
            if not self.groups.filter(name='HOD').exists():
                self.groups.add(hod_group)

    def login(self):
        current_time = now()
        payload = {
            'id': self.id
        }
        access_token = Helper.encode_jwt(payload, current_time)
        user_details = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'access_token': access_token
        }
        self.last_login = current_time
        return user_details
