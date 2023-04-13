from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from .assistants import Sanitizer, is_space_only
from .models import Client
import time


class ClientAuthBackend(BaseBackend):
    """
    A class for managing the authentication for the client.
    """

    def authenticate(self, request: HttpRequest, **credentials):
        """
        A method for authenticating the user with their phone number and password.
        """

        sanitizer = Sanitizer()

        has_te = 'Transfer-Encoding' in request.headers
        has_cl = 'Content-Length' in request.headers
        if has_te and has_cl:
            raise PermissionDenied
        
        names = credentials['names'] if 'names' in credentials else None
        phone_number = credentials['username']
        password = credentials['password']
        address = credentials['address'] if 'address' in credentials else None
        email = credentials['email'] if 'email' in credentials else None
        childs_class = credentials['childs_class'] if 'childs_class' in credentials else None
        if names and phone_number and password and address and childs_class:
            check_data = [
                names and not is_space_only(names),
                phone_number and sanitizer.valid(phone_number, r'[^0-9+]'),
                password and sanitizer.valid(password, r'[^a-zA-Z0-9]'),
                address and not is_space_only(address),
                sanitizer.valid(email, r'[^a-zA-Z0-9@.-_]'),
                childs_class and not is_space_only(childs_class),
            ]
            if False not in check_data:
                client = Client(
                    names=names,
                    phone_number=phone_number,
                    address=address,
                    email=email if email and not is_space_only(email) else None,
                    childs_class=childs_class,
                )
                client.set_password(password)
                client.is_active = True
                client.last_login = time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime())
                client.date_joined = time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime())
                client.save()
                return client
        elif not names and not address and not email and not childs_class and phone_number and password:
            check_data = [
                phone_number and sanitizer.valid(phone_number, r'[^0-9+]'),
                password and sanitizer.valid(password, r'[^a-zA-Z0-9]'),
            ]
            if False not in check_data:
                try:
                    client = Client.objects.get(phone_number=phone_number)
                except Client.DoesNotExist:
                    return None
                if client.check_password(password) is True:
                    client.is_active = True
                    client.last_login = time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime())
                    client.save()
                    return client
                return None
        raise PermissionDenied('An invalid input made!')

    def get_user(self, phone_number):
        """
        Gets the user with the corresponding phone number.
        """

        try:
            return Client.objects.get(phone_number=phone_number)
        except Client.DoesNotExist:
            return None
