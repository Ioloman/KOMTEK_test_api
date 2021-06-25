from django.contrib import admin
from api.models import Catalog, CatalogItem


class CatalogAdmin(admin.ModelAdmin):
    """
    Класс, перегружающий поведение админки при действиях с моделью Catalog
    """
    def save_related(self, request, form, formsets, change):
        """
        При сохранении через админку, если производится изменение
        поля ManyToMany в перегруженном методе save(...) модели, то эти изменения аннулируются.
        Данный метод перегружен, чтобы избежать этого.
        """
        # добавляем сохраненные в методе save(...) объекты в форму, которая пришла с админки
        form.cleaned_data['items'] = form.cleaned_data['items'].union(form.instance.items.all())
        # сохраняем
        form.save_m2m()
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(CatalogItem)
