from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
#from django_ratelimit.decorators import ratelimit
from lp.models import Book, FAQ, IndexInfo, Place
from lp.relations import SocialMedia
from users.assistants import Sanitizer, is_space_only
from users.models import Client


#@ratelimit(key='ip', rate='10/m')
def clients(request: HttpRequest):
    """
    The page for checking the existing users in the database.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404

    people = Client.objects.all().order_by("date_joined")
    people_count = Client.objects.count()

    context = {
        'people_count': people_count,
        'people': people,
    }
    return render(request, 'admin_panel/clients.html', context)


#@ratelimit(key='ip', rate='10/m')
def delete_client(request: HttpRequest, phone_number: str):
    """
    A view for deleting a specific client.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404

    sanitizer = Sanitizer()

    if request.user.is_superuser:
        if phone_number and not is_space_only(phone_number) and sanitizer.valid(phone_number, r'[^0-9+]'):
            client = get_object_or_404(Client, phone_number=phone_number)
            client.delete()
            return redirect('admin_panel:clients')
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def main_information(request: HttpRequest):
    """
    A view for checking the main information for the main page.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404

    information = IndexInfo.objects.all()
    places = Place.objects.all()
    media = SocialMedia.objects.all()
    books = Book.objects.all()
    faq = FAQ.objects.all()
    
    context = {
        'information': information,
        'places': places,
        'media': media,
        'books': books,
        'faq': faq,
    }
    return render(request, 'admin_panel/main-page.html', context)


#@ratelimit(key='ip', rate='10/m')
def add_main_information(request: HttpRequest):
    """
    A view for adding main information.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404
    
    sanitizer = Sanitizer()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        brand = request.FILES.get('brand')
        brand_height = request.POST.get('brand_height')
        title = request.POST.get('title')
        available_places = request.POST.get('available_places')
        booked_places = request.POST.get('booked_places')
        product_title = request.POST.get('product_title')
        product_info = request.POST.get('product_info')
        company_requisities = request.POST.get('company_requisities')
        footer_motto = request.POST.get('footer_motto')
        socialmedia = request.POST.getlist('socialmedia')
        check_data = [
            brand and sanitizer.filevalid(str(brand), ['.png', '.jpg', '.jpeg', '.svg', '.bmp']),
            brand_height and not \
            is_space_only(brand_height) and \
            sanitizer.valid(brand_height, r'[^0-9.]'),
            title and not \
            is_space_only(title),
            product_title and not \
            is_space_only(product_title),
            product_info and not \
            is_space_only(product_info),
            company_requisities and not \
            is_space_only(company_requisities),
            footer_motto and not \
            is_space_only(footer_motto),
        ]
        print(check_data)
        if False not in check_data:
            new_info = IndexInfo.objects.create(
                brand_height=brand_height,
                title=title,
                product_title=product_title,
                product_info=product_info,
                company_requisities=company_requisities,
                footer_motto=footer_motto,
            )
            new_info.brand = brand
            new_info.media.set([int(sm_id) for sm_id in socialmedia])
            new_info.save()
            return JsonResponse({'status': 'added'})
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def delete_main_information(request: HttpRequest):
    """
    A view for deleting specific main information.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404
    
    sanitizer = Sanitizer()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'GET' and sanitizer.valid(request.GET.get('id'), r'[^0-9]'):
        info = get_object_or_404(IndexInfo, pk=request.GET.get('id'))
        info.delete()
        return JsonResponse({'status': 'deleted'})
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def add_place(request: HttpRequest):
    """
    A view for adding places for courses.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404
    
    sanitizer = Sanitizer()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        available_places = request.POST.get('available_places')
        booked_places = request.POST.get('booked_places')
        check_data = [
            available_places and not is_space_only(available_places) and sanitizer.valid(available_places, r'[^0-9]'),
            booked_places and not is_space_only(booked_places) and sanitizer.valid(booked_places, r'[^0-9]'),
        ]
        if False not in check_data:
            new_place = Place.objects.create(available_places=available_places, booked_places=booked_places)
            new_place.save()
            return JsonResponse({'status': 'added'})
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def delete_place(request: HttpRequest):
    """
    A view for deleting specific place for a course.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404
    
    sanitizer = Sanitizer()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'GET' and sanitizer.valid(request.GET.get('id'), r'[^0-9]'):
        place = get_object_or_404(Place, pk=request.GET.get('id'))
        place.delete()
        return JsonResponse({'status': 'deleted'})
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def add_media(request: HttpRequest):
    """
    A view for adding social media for contact.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404
    
    sanitizer = Sanitizer()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        name = request.POST.get('name')
        icon = request.FILES.get('icon')
        link = request.POST.get('link')
        print(icon)
        check_data = [
            name and not is_space_only(name),
            icon and sanitizer.filevalid(str(icon), ['.png', '.jpg', '.jpeg', '.svg', '.bmp']),
            link and not is_space_only(link),
        ]
        if False not in check_data:
            new_media = SocialMedia.objects.create(
                name=name,
                link=link,
            )
            new_media.icon = icon
            new_media.save()
            return JsonResponse({'status': 'added'})
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def delete_media(request: HttpRequest):
    """
    A view for deleting specific social media.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404

    sanitizer = Sanitizer()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'GET' and sanitizer.valid(request.GET.get('id'), r'[^0-9]'):
        media = get_object_or_404(SocialMedia, pk=request.GET.get('id'))
        media.delete()
        return JsonResponse({'status': 'deleted'})
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def add_book(request: HttpRequest):
    """
    A view for adding a book.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404

    sanitizer = Sanitizer()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')
        check_data = [
            name and not is_space_only(name),
            file and sanitizer.filevalid(str(file), ['.pdf']),
        ]
        if False not in check_data:
            new_book = Book.objects.create(
                name=name,
            )
            new_book.file = file
            new_book.save()
            return JsonResponse({'status': 'added'})
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def delete_book(request: HttpRequest):
    """
    A view for deleting a specific book.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404

    sanitizer = Sanitizer()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'GET' and sanitizer.valid(request.GET.get('id'), r'[^0-9]'):
        book = get_object_or_404(Book, pk=request.GET.get('id'))
        book.delete()
        return JsonResponse({'status': 'deleted'})
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def add_faq(request: HttpRequest):
    """
    A view for adding frequently asked questions.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        check_data = [
            question and not \
            is_space_only(question),
            answer and not \
            is_space_only(answer),
        ]
        if False not in check_data:
            new_faq = FAQ.objects.create(
                question=question,
                answer=answer,
            )
            new_faq.save()
            return JsonResponse({'status': 'added'})
    raise PermissionDenied


#@ratelimit(key='ip', rate='10/m')
def delete_faq(request: HttpRequest):
    """
    A view for deleting a specific frequently asked question.
    """

    if not request.user.is_superuser or not request.user.is_admin:
        raise Http404

    sanitizer = Sanitizer()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'GET' and sanitizer.valid(request.GET.get('id'), r'[^0-9]'):
        faq = get_object_or_404(FAQ, pk=request.GET.get('id'))
        faq.delete()
        return JsonResponse({'status': 'deleted'})
    raise PermissionDenied
