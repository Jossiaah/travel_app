from django.db import models

# Create your models here.
from django.db import models

import bcrypt
from datetime import datetime
import re

# Create your models here.


from django.db import models

import bcrypt
from datetime import datetime
import re

# Create your models here.


class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}

        # validate name data
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters.'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'last Name must be at least 2 characters.'

        # validate email
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid email adress!'
        else:
            user_list = User.objects.filter(email=post_data['email'])
            if len(user_list) > 0:
                errors['email'] = "Email adress is already in use!"

        # validate password
        if len(post_data['password']) < 8:
            errors['passowrd'] = 'Password must be at least 8 characters.'
        if post_data['password'] != post_data['confirm']:
            errors['confirm'] = "Passowrd does not match."

        return errors

    def login_validator(self, post_data):
        errors = {}

        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) > 0:
            user = user_list[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid Email or Password"
        else:
            errors['email'] = "Invalid Email or Password"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_pw = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updtaed_at = models.DateField(auto_now=True)
    objects = UserManager()


class TripManager(models.Manager):

    def new_trip_validator(self, post_data):
        errors = {}

        # validate trip data
        if len(post_data['destination']) < 3:
            errors['destination'] = 'Must enter a destination.'
        if len(post_data['start_date']) < 1:
            errors['start_date'] = 'Must enter a start date.'
        if len(post_data['end_date']) < 1:
            errors['end_date'] = 'Must enter an end date.'
        if len(post_data['plan']) < 3:
            errors['plan'] = 'Must be more than 3 character.'

        return errors


class Trip(models.Model):
    user = models.ForeignKey(
        User, related_name="trips", on_delete=models.CASCADE)
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField(default="trip plan")
    created_at = models.DateTimeField(auto_now_add=True)
    updtaed_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
