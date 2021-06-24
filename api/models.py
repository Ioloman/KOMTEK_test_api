from typing import Optional

from django.db import models
from datetime import date


class Catalog(models.Model):
    id = models.AutoField(primary_key=True)

    identifier = models.CharField(max_length=50, verbose_name="идентификатор")

    # необходимость этого отношение здесь спорно, так как зависят элементы от глобального идентификатора
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

    @classmethod
    def get_by_version(cls, identifier: str, version: Optional[str] = None):
        try:
            if version is None:
                return cls.objects.filter(identifier=identifier, date__lte=date.today()).latest('date')
            else:
                return cls.objects.get(identifier=identifier, version=version)
        except cls.DoesNotExist:
            return None

    def save(self, *args, **kwargs) -> None:
        """
        Перегрузка метода сохранения.
        При создании нового справочника, если существует предыдущая версия,
        то она находится методом get_by_version и все элементы справочника копируются в только что созданный.
        Если предыдущей версии нет, то ищутся элементы справочника с
        родительским идентификатором, соответствующим данному справочнику.
        При сохранении из админки, изменения полей ManyToMany, произведенные в методах, аннулируются,
        так что приходится перегрузить еще один метод в файле admin.py
        """
        # если объект еще не сохранен в бд (то есть происходит создание)
        if not self.id:
            # текущий справочник, либо None
            latest = self.get_by_version(self.identifier)
            # сначала нужно сохранить
            super().save(*args, **kwargs)
            # добавляем элементы
            if latest is None:
                self.items.add(*CatalogItem.objects.filter(parent_identifier=self.identifier))
            else:
                self.items.add(*latest.items.all())
        else:
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        get_latest_by = 'date'

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

    def save(self, *args, **kwargs) -> None:
        """
        Перегрузка метода сохранения для того,
        чтобы созданные элементы соединялись с текущим справочником.
        """
        # если объект еще не сохранен в бд (то есть происходит создание)
        if not self.id:
            # находим текущий справочник либо None
            latest_catalog = Catalog.get_by_version(identifier=self.parent_identifier)
            super().save(*args, kwargs)
            # добавляем к справочнику
            if latest_catalog is not None:
                latest_catalog.items.add(self)
        else:
            super().save(*args, kwargs)

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочников"





