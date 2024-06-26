from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

# Create your models here.


class AbsrtactModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):

    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change the related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Change the related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    email = models.EmailField(('email address'), blank=True, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='profile_images')
    sex = models.CharField(max_length=40, choices=SEX_CHOICES)
    phone_number = models.TextField(max_length=500, blank=True)
    birthdate = models.DateField(max_length=500, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return str(self.username)
    
class Team(AbsrtactModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team_images')
    position = models.CharField(max_length=255)
    description = models.TextField(max_length=500,blank=True,null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_user')

    def __str__(self):
        return self.name

class Contact(AbsrtactModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=500)
    is_answered = models.BooleanField(default=False)
    def __str__(self):
        return self.name