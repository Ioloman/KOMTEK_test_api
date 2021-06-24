import datetime

from django.db.models import QuerySet, Count
from rest_framework import filters

from api.models import Catalog


class RelevantDateFilterBackend(filters.BaseFilterBackend):
    """
    Фильтр для получения списка справочников, актуальных на указанную дату
    """
    def filter_queryset(self, request, queryset: QuerySet, view):
        # определяем есть ли нужный параметр
        date = request.query_params.get('date_filter', None)
        if date:
            # конвертируем дату
            date = datetime.date.fromisoformat(date)
            # находим список уникальных идентификаторов
            distinct_identifiers = [dictionary['identifier'] for dictionary in
                                    queryset.values('identifier').annotate(Count('identifier'))]
            # убираем из queryset справочники, которые точно не подходят (составлены позже)
            queryset = queryset.filter(date__lte=date)

            # находим актуальный справочник и убираем из queryset
            # все справочники с таким же идентификатором, кроме найденного
            for identifier in distinct_identifiers:
                relevant_catalog = queryset.filter(identifier=identifier).latest('date')
                queryset = queryset.exclude(identifier=identifier, date__lt=relevant_catalog.date)

        return queryset
