from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, filters

from api.filters import RelevantDateFilterBackend
from api.models import Catalog, CatalogItem
from api.serializers import CatalogSerializer, CatalogItemSerializer
# TODO:
#  метод get_by_version обезопасить
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
        'Список справочников': reverse('api:catalog-list', request=request, format=format),
        'Список элементов': reverse('api:catalog-item-list', request=request, format=format),
    })


class CatalogList(generics.ListAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    # свой фильтр для получения списка справочников, актуальных на указанную дату.
    filter_backends = [RelevantDateFilterBackend, filters.OrderingFilter]
    ordering_fields = ['date', 'identifier', 'version']
    ordering = ['-date']


class CatalogDetail(generics.RetrieveAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class CatalogItemList(generics.ListAPIView):
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer


class CatalogItemDetail(generics.RetrieveAPIView):
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
