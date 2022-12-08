from django.db import models
import re
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be 2 or more charactors"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be 2 or more charactors"

        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"

        current_user = User.objects.filter(email = postData['email'])
        if len(current_user) > 0:
            errors['duplicate'] = "Email already registered"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 charactors"
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Passwords do not match"

        return errors

    def login_validator(self, postData):
        errors = {}
        existing_users = User.objects.filter(email = postData['email'])

        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        
        elif len(existing_users) == 0:
            errors['email'] = "Please enter a valid email and password"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be entered and at least 8 charactors"

        elif bcrypt.checkpw(postData['password'].encode(), existing_users[0].password.encode()) != True:
            errors['password'] = "Password and email do not match"

        return errors




class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return f"Name : {self.first_name}, email : {self.email}"
    # my_wishes


class WishManager(models.Manager):
    def wish_validater(self, postReq):
        errors = {}

        if len(postReq['wish']) < 4:
            errors['wish'] = "Wish must be at least 3 charactors"

        if len(postReq['description']) < 4:
            errors['description'] = "Description must be at least 3 charactors"

        return errors
    

class Wish(models.Model):
    wish = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    wish_maker = models.ForeignKey(User, related_name = 'my_wishes', on_delete = models.CASCADE)
    granted_wish = models.CharField(max_length=55, default = 'no')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()