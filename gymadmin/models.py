from django.contrib.auth import models as auth_models
from django.db import models

class UserManager(auth_models.BaseUserManager):
    def create_user(self, first_name: str, last_name: str, email:str, birth_date:str, password: str = None, is_staff=False, is_superuser=False ) -> "User":
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.birth_date = birth_date
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(self, first_name: str, last_name: str, email:str, birth_date: str, password: str)->"User":
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            birth_date=birth_date,
            is_staff=True,
            is_superuser=True
        )

        user.save()

        return user


class User(auth_models.AbstractUser):
    first_name = models.CharField(verbose_name="First Name", max_length=250, db_index=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=250, db_index=True)
    email = models.EmailField(verbose_name="Email", max_length=200, unique=True, db_index=True)
    birth_date = models.DateField()
    password = models.CharField(max_length=255)
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


class SubscriptionType(models.Model):
    title = models.CharField(max_length=250, db_index=True)
    def __str__(self):
        return self.title


class Subscription(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField()

    def __str__(self):
        return f"Subscription : {self.type}, {self.user}, start: {self.start_date}, end: {self.end_date}, price: {self.price}"


class Visit(models.Model):

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, db_index=True)
    date = models.DateField(db_index=True)
    enter_time = models.TimeField()
    exit_time = models.TimeField(null=True, blank=True)


    def __str__(self):
        return f"Visit : {self.date}, from {self.enter_time}, to: {self.exit_time}"



