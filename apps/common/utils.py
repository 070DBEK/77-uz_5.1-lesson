from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status


def paginate_queryset(request, queryset, page_size=20):
    """Umumiy pagination utility"""
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, page_size)

    try:
        page_obj = paginator.page(page)
    except:
        page_obj = paginator.page(1)

    return page_obj


def search_queryset(queryset, search_fields, query):
    """Umumiy search utility"""
    if not query:
        return queryset

    search_q = Q()
    for field in search_fields:
        search_q |= Q(**{f"{field}__icontains": query})

    return queryset.filter(search_q)


def success_response(message, data=None, status_code=status.HTTP_200_OK):
    """Success response utility"""
    response_data = {'message': message}
    if data:
        response_data.update(data)
    return Response(response_data, status=status_code)


def error_response(error, status_code=status.HTTP_400_BAD_REQUEST):
    """Error response utility"""
    return Response({'error': error}, status=status_code)


def format_phone_number(phone):
    """Telefon raqamini formatlash"""
    if not phone.startswith('+'):
        phone = '+' + phone
    return phone


def generate_slug(text, model_class, field_name='slug'):
    """Unique slug yaratish"""
    from django.utils.text import slugify
    import uuid

    base_slug = slugify(text)
    if not base_slug:
        base_slug = f'item-{uuid.uuid4().hex[:8]}'

    slug = base_slug
    counter = 1

    while model_class.objects.filter(**{field_name: slug}).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    return slug
