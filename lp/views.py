from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
#from django_ratelimit.decorators import ratelimit
from .models import Book, FAQ, IndexInfo, Place


#@ratelimit(key='ip', rate='10/m')
def index(request: HttpRequest):
    """
    The home page.
    """
    
    information = None
    place = None
    faq = FAQ.objects.all()
    try:
        information = IndexInfo.objects.latest('date_added')
        place = Place.objects.latest('id')
    except (IndexInfo.DoesNotExist, Place.DoesNotExist):
        pass

    context = {
        'information': information,
        'place': place,
        'faq': faq,
    }
    return render(request, 'lp/index.html', context)


#@ratelimit(key='ip', rate='10/m')
def get_main_information(request: HttpRequest):
    """
    A view for retrieving data on social media for the base html and returning it as a JsonResponse.

    Raises Http404 in case no data found.
    """

    has_te = 'Transfer-Encoding' in request.headers
    has_cl = 'Content-Length' in request.headers
    if has_te and has_cl:
        raise PermissionDenied

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'GET':
        information = None
        try:
            information = IndexInfo.objects.latest('date_added')
        except IndexInfo.DoesNotExist:
            pass
        book = None
        try:
            book = Book.objects.latest('id')
        except Book.DoesNotExist:
            pass
        brand = render_to_string(
            'lp/includes/brand.html',
            {
                'brand_image': information.brand.url if information.brand else None, 
                'height': information.brand_height if information.brand_height else None,
            }
        ) if information else None
        footer = render_to_string(
            'lp/includes/information-for-footer.html',
            {
                'information': information, 
                'media': information.media.all().order_by('name') if information else None, 
                'user': request.user,
            },
        )
        return JsonResponse({'brand': brand, 'footer': footer, 'book_link': book.file.url if book else None})
    raise PermissionDenied
