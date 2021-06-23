from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


def redirect_view(request):
    return redirect('api:root')


@api_view(['GET'])
def api_root(request, format=None):
    """Добро пожаловать в API.
    Ниже предоставлены ссылки."""
    return Response({
        'Главная': reverse('api:root', request=request, format=format),
    })
