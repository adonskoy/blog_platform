from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        if not password:
            raise ValueError('Password must be provided')

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, **extra_fields):
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = ['full_name']
    USERNAME_FIELD = 'nickname'

    objects = UserAccountManager()

    nickname = models.CharField('nickname', unique=True, blank=False, null=False, max_length=200)

    full_name = models.CharField('full name', blank=False, null=True, max_length=400)
    image = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_superuser = models.BooleanField('superuser status', default=False)
    is_active = models.BooleanField('active', default=True)
    subscriptions = models.ManyToManyField("self", symmetrical=False, blank=True)

    def get_short_name(self):
        return self.nickname

    @property
    def display_name(self):
        if not self.full_name:
            return self.nickname
        else:
            return self.full_name

    def __unicode__(self):
        return self.nickname


from django.contrib.auth.backends import ModelBackend


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        kwargs = {'nickname': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
            else:
                raise ValidationError("wrong password")
        except User.DoesNotExist:
            raise User.DoesNotExist
        except Exception as e:
            print(e)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
