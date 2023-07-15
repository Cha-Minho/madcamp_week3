from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AnonymousUser

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, email):
        if not username:
            raise ValueError("사용자명은 필수 입력 항목입니다.")
        if not email:
            raise ValueError("이메일은 필수 입력 항목입니다.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email):
        user = self.create_user(
            username=username,
            password=password,
            email=email,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable = False)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
    @property
    def is_anonymous(self):
        return False

    class Meta:
        db_table = 'users'

class CustomAnonymousUser(AnonymousUser):
    pass

AnonymousUser = CustomAnonymousUser
