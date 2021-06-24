from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from api.models import Catalog, CatalogItem
from api.serializers import CatalogSerializer, CatalogItemSerializer
# TODO:
#  протестировать привязку по связи мэни ту мэни в модели при создании,
#  сделать документацию,
#  добавить комменты,
#  сделать фильтры,
#  узнать про валидацию, сделать валидацию


def redirect_view(request):
    """
    Заглушка для переадресации с пустого url на url API
    """
    return redirect('api:root')


@api_view(['GET'])
def api_root(request, format=None):
    """Добро пожаловать в API.
    Ниже предоставлены ссылки."""
    return Response({
        'Главная': reverse('api:root', request=request, format=format),
        'Каталоги': reverse('api:catalog-list', request=request, format=format),
        'Элементы': reverse('api:catalog-item-list', request=request, format=format),
    })


class CatalogList(generics.ListAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class CatalogDetail(generics.RetrieveAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class CatalogItemList(generics.ListAPIView):
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer


class CatalogItemDetail(generics.RetrieveAPIView):
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
