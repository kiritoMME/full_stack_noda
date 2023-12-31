from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class City(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def _create_user(self, password, first_name, last_name, mobile, **extra_fields):
        if not mobile:
            raise ValueError("mobile must be provided")
        if not password:
            raise ValueError("Password is not provided")
        
        user = self.model(
            # email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            mobile = mobile,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(password, first_name, last_name, mobile, **extra_fields)
    
    def create_superuser(self, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(password, first_name, last_name, mobile, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile = models.CharField(unique=True, max_length=50)
    address = models.CharField(max_length=100000)
    # city = models.CharField(max_length=1000)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    products_in_cart = models.IntegerField(default=0)
    price_in_cart = models.FloatField(default=0)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f' {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
