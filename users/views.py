from django.contrib.auth import login, logout
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import redirect
#from django_ratelimit.decorators import ratelimit
from .assistants import Sanitizer, generate_token, is_space_only
from .backends import ClientAuthBackend
from .models import Client


#@ratelimit(key='ip', rate='10/m')
def register(request: HttpRequest):
    """
    A view for regsitering a user.
    """

    sanitizer = Sanitizer()
    backend = ClientAuthBackend()

    has_te = 'Transfer-Encoding' in request.headers
    has_cl = 'Content-Length' in request.headers
    if has_te and has_cl:
        raise PermissionDenied
    
    if request.method == 'POST':
        names = request.POST.get('names')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        childs_class = request.POST.get('childs_class')
        check_data = [
            names and not is_space_only(names),
            phone_number and sanitizer.valid(phone_number, r'[^0-9+]'),
            address and not is_space_only(address),
            childs_class and not is_space_only(childs_class),
        ]
        if False not in check_data:
            phone_numbers = [str(client.phone_number) for client in Client.objects.all()]
            if phone_number not in phone_numbers:
                client = backend.authenticate(
                    request, 
                    names=names, 
                    username=phone_number,
                    password=generate_token(),
                    address=address,
                    childs_class=childs_class,
                )
                if client:
                    login(request, client, 'users.backends.ClientAuthBackend')
                    return redirect('lp:index')
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def signin(request: HttpRequest):
    """
    A view for signing the user in.
    """

    sanitizer = Sanitizer()
    backend = ClientAuthBackend()

    has_te = 'Transfer-Encoding' in request.headers
    has_cl = 'Content-Length' in request.headers
    if has_te and has_cl:
        raise PermissionDenied
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        check_data = [
            phone_number and not is_space_only(phone_number) and sanitizer.valid(phone_number, r'[^0-9+]'),
            password and not is_space_only(password) and sanitizer.valid(password, r'[^a-zA-Z0-9]'),
        ]
        if False not in check_data:
            client = backend.authenticate(request, username=phone_number, password=password)
            if client:
                login(request, client, 'users.backends.ClientAuthBackend')
                return JsonResponse({'status': 'signedin'})
            else:
                raise Http404
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def signout(request: HttpRequest):
    """
    A view for signing the user out.
    """

    has_te = 'Transfer-Encoding' in request.headers
    has_cl = 'Content-Length' in request.headers
    if has_te and has_cl:
        raise PermissionDenied
    
    if request.user.is_authenticated:
        request.user.is_active = False
        request.user.save()
        logout(request)
        return redirect('lp:index')


#@ratelimit(key='ip', rate='10/m')
def get_phone_numbers(request: HttpRequest):
    """
    A view for retrieving phone_numbers from the database.
    """

    has_te = 'Transfer-Encoding' in request.headers
    has_cl = 'Content-Length' in request.headers
    if has_te and has_cl:
        raise PermissionDenied
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'GET':
        phone_numbers = [str(client.phone_number) for client in Client.objects.all()]
        return JsonResponse({'phone_numbers': phone_numbers})
    raise PermissionDenied
