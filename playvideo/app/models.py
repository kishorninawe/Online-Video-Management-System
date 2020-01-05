from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
        )

        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class VideoCategoryModel(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ('category',)


class VideoDetailModel(models.Model):
    video_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    tags = models.CharField(max_length=1000)
    categories = models.ForeignKey(VideoCategoryModel, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='images/thumbnail/')
    video = models.FileField(upload_to='video/')
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='u')
    date_uploaded = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def __int__(self):
        return self.categories
