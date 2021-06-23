from django.db import models
from datetime import date


class Catalog(models.Model):
    id = models.AutoField(primary_key=True)

    identifier = models.CharField(max_length=50, verbose_name="идентификатор")

    # необходимость этого отношение здесь спорно, так как зависят элементы от глобального идентификатора
    # заполняться будет в сериализаторе
    items = models.ManyToManyField('CatalogItem', blank=True)

    name = models.CharField(max_length=150, blank=True, verbose_name="наименование")
    short_name = models.CharField(max_length=50, blank=True, verbose_name="короткое наименование")
    description = models.TextField(blank=True, verbose_name="описание")
    version = models.CharField(max_length=20, verbose_name="версия")

    # решил использовать default вместо auto_now_add,
    # потому что не знаю как будет выбираться дата начала действия
    date = models.DateField(
        default=date.today,
        verbose_name="дата начала действия справочника этой версии"
    )

    def __str__(self):
        return f'{self.identifier} - {self.short_name}'

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

        # как я понял, справочники могут обновляться, а идентификатор остается тем же,
        # таким образом версия будет уникальна в пределах справочника
        constraints = [
            models.UniqueConstraint(fields=['identifier', 'version'], name='unique_version'),
        ]


class CatalogItem(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="идентификатор")

    identifier = models.CharField(max_length=50, verbose_name="идентификатор")
    parent_identifier = models.CharField(max_length=50, verbose_name="родительский идентификатор")

    code = models.CharField(max_length=50, blank=False, verbose_name="код элемента")
    value = models.CharField(max_length=200, blank=False, verbose_name="значение элемента")

    def __str__(self):
        return f'{self.identifier} - {self.parent_identifier}'

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочников"





