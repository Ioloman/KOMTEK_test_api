from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, filters
from rest_framework.views import APIView

from api.filters import RelevantDateFilterBackend, ExactCatalogFilterBackend
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
        'Валидация элементов': reverse('api:catalog-item-validation', request=request, format=format),
    })


class CatalogList(generics.ListAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    # свой фильтр для получения списка справочников, актуальных на указанную дату
    filter_backends = [RelevantDateFilterBackend, filters.OrderingFilter]
    ordering_fields = ['date', 'identifier', 'version']
    ordering = ['-date']


class CatalogDetail(generics.RetrieveAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class CatalogItemList(generics.ListAPIView):
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    # свой фильтр для получения элементов заданного справочника текущей или указанной версии
    filter_backends = [ExactCatalogFilterBackend, filters.OrderingFilter]
    ordering_fields = ['parent_identifier']
    ordering = ['parent_identifier']


class CatalogItemDetail(generics.RetrieveAPIView):
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer


class CatalogItemsValidation(APIView):
    def post(self, request, format=None):
        identifier = request.query_params.get('catalog_identifier', None)
        if not identifier:
            return Response({'error': 'parameter "catalog_identifier" is required'})
        queryset = CatalogItem.objects.all()
        filter = ExactCatalogFilterBackend()
        catalogs_items = filter.filter_queryset(request, queryset, None)
        serialized_catalogs_items = [CatalogItemSerializer(item).data for item in catalogs_items]
        for item in serialized_catalogs_items:
            del item['id']
        if not isinstance(request.data, list):
            return Response({'error': 'invalid data'})
        serialized_input_items = []
        for item in request.data:
            serialized_item = CatalogItemSerializer(data=item)
            if serialized_item.is_valid():
                serialized_input_items.append(dict(serialized_item.validated_data))
            else:
                serialized_input_items.append(None)
        validation_short_data = []
        for item in serialized_input_items:
            if item in serialized_catalogs_items:
                validation_short_data.append(True)
            else:
                validation_short_data.append(False)
        return Response({
            'short_results': validation_short_data,
            'results': zip(request.data, validation_short_data)
        })




