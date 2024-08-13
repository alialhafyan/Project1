from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Myuser(AbstractUser):
    username = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        null=False,
        help_text="Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.",
        verbose_name="Username"
    ) 
    email=models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="Email address",
        help_text="Required Enter a valid email address")
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    is_manager=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"



class PasswordResetToken(models.Model):
    user = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()