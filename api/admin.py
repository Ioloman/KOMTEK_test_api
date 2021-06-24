from django.contrib import admin
from api.models import Catalog, CatalogItem


class CatalogAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        form.cleaned_data['items'] = form.cleaned_data['items'].union(form.instance.items.all())
        form.save_m2m()
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(CatalogItem)
