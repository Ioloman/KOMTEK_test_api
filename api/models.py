from django.db import models
from datetime import date


class Catalog(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="идентификатор")

    # в задании написано, что некоторые подробности не указаны,
    # так что я сделал наименование обязательным (не может быть пустым),
    # а короткое наименование необязательным
    name = models.CharField(max_length=150, verbose_name="наименование")

    short_name = models.CharField(max_length=50, blank=True, verbose_name="короткое наименование")
    description = models.TextField(blank=True, verbose_name="описание")
    version = models.CharField(max_length=20, verbose_name="версия")

    # решил использовать default вместо auto_now_add,
    # потому что не знаю как будет выбираться дата начала действия
    date = models.DateField(
        default=date.today,
        verbose_name="дата начала действия справочника этой версии"
    )

    class Meta:
        verbose_name = "Справочник"

        # как я понял, справочники могут обновляться, а наименование остается тем же,
        # таким образом версия будет уникальна в пределах справочника
        constraints = [
            models.UniqueConstraint(fields=['name', 'version'], name='unique_version'),
        ]


class CatalogItem(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="идентификатор")

    # сделал CASCADE, если нельзя удалять эти документы, нужно сделать SET_NULL
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name="родительский идентификатор")

    code = models.CharField(max_length=50, blank=False, verbose_name="код элемента")
    value = models.CharField(max_length=200, blank=False, verbose_name="значение элемента")

    class Meta:
        verbose_name = "Элемент справочника"





