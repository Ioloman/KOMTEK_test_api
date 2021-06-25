from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, filters
from rest_framework.views import APIView

from api.filters import RelevantDateFilterBackend, ExactCatalogFilterBackend
from api.models import Catalog, CatalogItem
from api.serializers import CatalogSerializer, CatalogItemSerializer


def redirect_view(request):
    """
    Заглушка для переадресации с пустого url на url API
    """
    return redirect('api:root')


@api_view(['GET'])
def api_root(request, format=None):
    """
    Добро пожаловать в API. Здесь предоставлены ссылки для навигации по API.\n
    Эндпоинты со списком справочников и списом элементов справочников поддерживают постраничный вывод по 10 объектов.\n
    Результат представляет собой объект JSON с полями:\n
    count: кол-во объектов в ответе\n
    next: ссылка на следующую страницу или null\n
    previous: ссылка на предыдущую страницу или null\n
    results: списко с результатами\n
    Навигация может осуществляться вручную путем добавления параметра page:\n
    GET /api/catalogs/?page=2
    """
    # Главная страница с навигацией
    return Response({
        'Главная': reverse('api:root', request=request, format=format),
        'Список справочников': reverse('api:catalog-list', request=request, format=format),
        'Список элементов': reverse('api:catalog-item-list', request=request, format=format),
        'Валидация элементов': reverse('api:catalog-item-validation', request=request, format=format),
    })


class CatalogList(generics.ListAPIView):
    """
    Список справочников. Read-Only.\n
    Возможна сортировка по полям date, identifier, version. Например:\n
    GET /api/catalogs/?ordering=identifier - в алфавитном порядке\n
    GET /api/catalogs/?ordering=-date - по дате, начиная с последней.\n
    Для получения списка справочников, актуальных на указанную дату используется параметр date:\n
    GET /api/catalogs/?date=2021-06-24 - дата представлена в ISO формате YYYY-MM-DD.
    """
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    # свой фильтр для получения списка справочников, актуальных на указанную дату
    filter_backends = [RelevantDateFilterBackend, filters.OrderingFilter]
    ordering_fields = ['date', 'identifier', 'version']
    ordering = ['-date']


class CatalogDetail(generics.RetrieveAPIView):
    """
    Конкретный справочник. Read-Only.
    """
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class CatalogItemList(generics.ListAPIView):
    """
    Список элементов справочников. Read-Only.\n
    Возможна сортировка по полю parent_identifier. Например:\n
    GET /api/catalog-items/?ordering=-parent_identifier - в  обратном алфавитном порядке.\n
    Для получения элементов заданного справочника текущей или указанной версии:\n
    GET /api/catalog-items/?catalog_identifier=1222 - выдаст элементы актуального на сегодня справочника с идентификатором 1222,\n
    GET /api/catalog-items/?catalog_identifier=1222&catalog_version=1.3 - выдаст элементы справочника с идентификатором 1222 версии 1.3.\n
    """
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    # свой фильтр для получения элементов заданного справочника текущей или указанной версии
    filter_backends = [ExactCatalogFilterBackend, filters.OrderingFilter]
    ordering_fields = ['parent_identifier']
    ordering = ['parent_identifier']


class CatalogItemDetail(generics.RetrieveAPIView):
    """
    Конкретный элемент справочника. Read-Only.
    """
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer


class CatalogItemsValidation(APIView):
    """
    Валидация элементов справочника. Выбор справочника и версии справочника, относительно которого
    требуется валидация производится также, как и на странице <a href="/api/catalogs/">со списком справочников</a>.\n
    То есть комбинацией параметров catalog_identifier и catalog_version.\n
    Для валидации необходимо совершить POST запрос как минимум с параметром catalog_identifier:\n
    POST /api/catalog-items/validation/?catalog_identifier=1222\n
    И в теле запроса должен содержаться JSON список с объектами, которые подлежат валидации.\n
    При некорректных данных запроса в ответ будет состоять из JSON объекта с полем "error" и описание проблемы.\n
    При корректном запросе в ответе будет JSON объект с полем "short_results", в котором будет список булевых значений
    true или false на месте, соответствующему объекту в запросе.\n
    Вторым полем будет "results". Это список из пар: объект, подаваемый на валидацию и булево значение, соответствующее ему.\n
    Если в параметрах будет указан несуществующий справочник, то все объекты будут оценены, как не прошедшие валидацию, то есть значением false.
    """
    def post(self, request, format=None):
        # проверяем наличие обязательного параметра
        identifier = request.query_params.get('catalog_identifier', None)
        if not identifier:
            return Response({'error': 'parameter "catalog_identifier" is required'})
        # с помощью уже написанного фильтра получаем элементы указанного в параметрах справочника
        queryset = CatalogItem.objects.all()
        filter = ExactCatalogFilterBackend()
        catalogs_items = filter.filter_queryset(request, queryset, None)
        # сериализуем полученные элементы и сохраняем в виде словарей
        serialized_catalogs_items = [CatalogItemSerializer(item).data for item in catalogs_items]
        # убираем из элементов поле "id"
        for item in serialized_catalogs_items:
            if item.get('id', False):
                del item['id']
        # если в теле запроса не список, то явно некорректные данные
        if not isinstance(request.data, list):
            return Response({'error': 'invalid data'})
        # сериализуем полученные в запросе объекты
        serialized_input_items = []
        for item in request.data:
            serialized_item = CatalogItemSerializer(data=item)
            if serialized_item.is_valid():
                serialized_input_items.append(dict(serialized_item.validated_data))
            else:
                serialized_input_items.append(None)
        # заполняем список с результатами
        validation_short_data = []
        for item in serialized_input_items:
            # если словарь из запроса совпадаем со словарем из выбранного справочника,
            # то добавляем на это место True
            if item in serialized_catalogs_items:
                validation_short_data.append(True)
            else:
                validation_short_data.append(False)
        return Response({
            'short_results': validation_short_data,
            # для полных результатов склеиваем данные запроса со списком результатов
            'results': zip(request.data, validation_short_data)
        })




