from django.db import models
from datetime import date
from common.models import AbstractBaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email,  password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have a valid email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """Custom User model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField(default=date.today())
    phone_number = models.CharField(max_length=15)
    heading = models.CharField(max_length=255, default="")
    desc = models.TextField(default="")
    image = models.ImageField(null=True, upload_to='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """Str representation of the object"""
        return str(self.email)


class VerifyTokenGen(AbstractBaseModel):
    """Generates a token for a user to verify acccount and reset password"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="token_user")
    token = models.CharField(max_length=8)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Str representation of the object"""
        return str(self.user.email)


class Location(AbstractBaseModel):
    """Store Locations, independent model. Can be removed when the app uses navigation API"""
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    lat = models.IntegerField()
    log = models.IntegerField()

    def __str__(self):
        """Str representation of the object"""
        return str(f"{self.city}, {self.state}")


class UserLocation(AbstractBaseModel):
    """User Location showed on the profile"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="location_user")
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    lat = models.IntegerField()
    log = models.IntegerField()

    def __str__(self):
        """Str representation of the object"""
        return str(f"{self.user.email} - {self.city}, {self.state}")


class CategoryService(AbstractBaseModel):
    """Category for provided jobs and freelancing"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """Str representation of the object"""
        return str(self.name)


class Freelancing(AbstractBaseModel):
    """Users freelancing services"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="freelancing_user")
    date_posted = models.DateField()

    def __str__(self):
        """Str representation of the object"""
        return str(f"{self.user.email} - {self.date_posted}")


class FreelancingService(AbstractBaseModel):
    """Each freelancing posts can have several different services"""
    HOUR = "HOUR"
    ONCE = "ONCE"
    PAYMENT_CHOICES = (
        (HOUR, "Hour"),
        (ONCE, "Once"),
    )

    freelancing = models.ForeignKey(Freelancing, on_delete=models.CASCADE, related_name="service_freelancing")
    service_name = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Str representation of the object"""
        return str(f"{self.freelancing.user.email} - {self.service_name}")


class Job(AbstractBaseModel):
    """Users can post temp jobs"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_user")
    title = models.CharField(max_length=255)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_range_availability = models.DateField()
    end_range_availability = models.DateField()

    def __str__(self):
        """Str representation of the object"""
        return str(f"{self.user.email} - {self.title}")
