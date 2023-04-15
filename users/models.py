from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import time


class ClientManager(BaseUserManager):
    """
    A class for managing client data.
    """

    def create_user(self, names, phone_number, password, address, childs_class):
        """
        A method for creating a new client.
        """

        attrs = {
            'names': names,
            'phone_number': phone_number,
            'password': password,
            'address': address,
            'childs_class': childs_class,
        }
        for key, value in attrs.items():
            if not value:
                raise ValueError(f"{key.title().replace('_', ' ')} has not been provided!")
        
        client = self.model(
            names=names,
            phone_number=phone_number,
            address=address,
            childs_class=childs_class,
        )

        client.set_password(password)
        client.is_active = True
        client.last_login = time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime())
        client.date_joined = time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime())
        client.save(using=self._db)
        return client

    
    def create_superuser(self, names, phone_number, password, address, childs_class):
        """
        A method for creating a superuser.
        """

        attrs = {
            'names': names,
            'phone_number': phone_number,
            'password': password,
            'address': address,
            'childs_class': childs_class,
        }
        for key, value in attrs.items():
            if not value:
                raise ValueError(f"{key.title().replace('_', ' ')} has not been provided!")
        
        superuser = self.create_user(
            names=names,
            phone_number=phone_number,
            password=password,
            address=address,
            childs_class=childs_class,
        )

        superuser.is_active = True
        superuser.is_admin = True
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.last_login = time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime())
        superuser.date_joined = time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime())
        superuser.save(using=self._db)
        return superuser


class Client(AbstractBaseUser):
    """
    A new user with some different attributes.
    """

    names = models.CharField(max_length=180)
    phone_number = models.CharField(max_length=13, unique=True, primary_key=True)
    password = models.CharField(max_length=128)
    address = models.CharField(max_length=250)
    childs_class = models.CharField(max_length=20)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=False)
    date_joined = models.DateTimeField(auto_now_add=False)

    objects = ClientManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['names', 'address', 'childs_class']
    PERMISSIONS = []

    def __str__(self) -> str:
        
        return self.names
    

    def has_perm(self, perm, obj=None):
        """
        A method for checking if the user has the given permission.
        """

        return True
    

    def has_module_perms(self, app_label):
        """
        A method for checking if the user has a permission for a module with the given app label.
        """

        return True
    
