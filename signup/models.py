from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    statut = models.CharField(max_length=10, default='normal')  # 'normal' par défaut, peut être 'admin' si besoin
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10)  # Add the 'role' field back without a default

    def __str__(self):
        return self.email
