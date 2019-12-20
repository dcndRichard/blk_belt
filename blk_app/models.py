from django.db import models
import re # regex

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')


# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}

        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="invalid email address."

        if len(postData['first_name']) < 3:
            errors['first_name']="First Name must be more than 2 characters."

        if len(postData['last_name']) < 3:
            errors['last_name']="Last Name must be more than 2 characters."

        if len(postData['password']) < 3:
            errors['password']="Password must be more than 8 characters."

        if postData["password"] != postData["confirm_password"]:
            errors['password']="Passwords must match."

        for user in User.objects.all():
            if postData['email'] == user.email:
                errors['email'] = 'Email is already in our database'
                break
        return errors


    def acct_edit_validator(self, postData):
        errors={}

        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="invalid email address."

        if len(postData['first_name']) < 3:
            errors['first_name']="First Name must be more than 2 characters."

        if len(postData['last_name']) < 3:
            errors['last_name']="Last Name must be more than 2 characters."

        logged_in_user = User.objects.get(id=postData['user_id'])
        old_email= logged_in_user.email
        for user in User.objects.all():
            if postData['email'] != old_email and postData['email'] == user.email:
                errors['email'] = 'Email is already in our database'
                break 
     
        return errors






class User(models.Model):
    first_name=models.CharField(max_length=60)
    last_name=models.CharField(max_length=60)
    first_name=models.CharField(max_length=60)
    email=models.CharField(max_length=60)
    password=models.CharField(max_length=60)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # post
    # likes
    objects= UserManager()



class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors={}

        if len(postData['author']) < 3:
            errors['author']="Author must be more than 3 characters."

        if len(postData['quote']) < 11:
            errors['quote']="Quote must be more than 10 characters."

        return errors



class Quote(models.Model):
    author=models.CharField(max_length=60)
    quote=models.TextField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # relationships
    users_who_posted=models.ForeignKey('User',related_name='post',on_delete=models.CASCADE)
    users_who_liked=models.ManyToManyField('User',related_name='likes')
    
    objects= QuoteManager()



