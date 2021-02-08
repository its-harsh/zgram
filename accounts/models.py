from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


def image_upload_path(instance, filename):
    return f'{instance}/profile_image/{filename}'


class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password=None, **extra_fields):
        if not username and not email:
            raise ValueError(
                'Every account must have an email address and username')
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.model(
            username=username, email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='Username', max_length=15, unique=True, primary_key=True, validators=[])
    email = models.EmailField(verbose_name='Email',
                              max_length=254, unique=True, validators=[])
    full_name = models.CharField(
        verbose_name='Full Name', max_length=60, blank=True, null=True)
    image = models.ImageField(verbose_name='Image',
                              upload_to=image_upload_path, blank=True, null=True)
    bio = models.TextField(
        verbose_name='Bio', max_length=500, blank=True, null=True)
    website = models.URLField(verbose_name='Website',
                              max_length=200, blank=True, null=True)
    gender = models.CharField(verbose_name='Gender', max_length=1, choices=(
        ('m', 'Male'), ('f', 'Female'), ('o', 'Other')
    ), default='m')
    is_active = models.BooleanField(
        verbose_name='Account Enabled', default=False)
    is_private = models.BooleanField(
        verbose_name='Private Account', default=False)
    creator_account = models.BooleanField(
        verbose_name='Creator\'s Account', default=False)

    is_staff = models.BooleanField(verbose_name='Staff User', default=False)
    is_superuser = models.BooleanField(verbose_name='Superuser', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email', )

    last_login = None

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class FFRelation(models.Model):
    user = models.ForeignKey(
        verbose_name='Account who is following', to=User, on_delete=models.CASCADE, related_name='account')
    f_account = models.ForeignKey(verbose_name='Account to be followed',
                                  to=User, on_delete=models.CASCADE, related_name='followed')

    def __str__(self):
        return f'{self.user} -> {self.f_account}'

    class Meta:
        verbose_name = 'User Relation'
        verbose_name_plural = 'Users Relations'
