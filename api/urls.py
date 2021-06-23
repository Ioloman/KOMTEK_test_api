from django.urls import path
from api import views


app_name = 'api'

urlpatterns = [
    path('', views.api_root, name='root'),
    path('catalogs/', views.CatalogList.as_view(), name='catalog-list'),
    path('catalogs/<int:pk>/', views.CatalogDetail.as_view(), name='catalog-detail'),
    path('catalog-items/', views.CatalogItemList.as_view(), name='catalog-item-list'),
    path('catalog-items/<int:pk>/', views.CatalogItemDetail.as_view(), name='catalog-item-detail'),
]