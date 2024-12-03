from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
def validate_min_length(value):
    if len(value) < 6:
        raise ValidationError('This field must be at least 6 characters long.')

class User(models.Model):
    username = models.CharField(max_length=100, unique=True, validators=[validate_min_length])
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, validators=[validate_min_length])

    def __str__(self):
        return self.username