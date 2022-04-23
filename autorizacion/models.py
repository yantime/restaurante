from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .authManager import UserManager


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField( unique=True, null=False)
    password = models.TextField(null=False)
    nombre = models.CharField(max_length=45, null=False)
    rol = models.CharField(choices= (['admin', 'admin'], ['mozo', 'mozo']), max_length=40)

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = UserManager()

    USERNAME_FIELD = 'correo'

    REQUIRED_FIELDS = ['nombre', 'rol']

    class Meta:
        db_table = 'usuarios'
