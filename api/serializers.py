from rest_framework import serializers

from api.models import Catalog, CatalogItem


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        exclude = ['items']


class CatalogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogItem
        fields = '__all__'
