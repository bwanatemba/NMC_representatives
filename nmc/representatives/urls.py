from django.urls import path
from . import views
from .views import add_representative, get_wards, manage_counties, manage_wards
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_representative, name='add_representative'),
    path('list/', views.representative_list, name='representative_list'),
    path('table/', views.representative_table, name='representative_table'),
    path('export/', views.export_representatives_csv, name='export_representatives_csv'),
    path('edit_positions/', views.edit_positions, name='edit_positions'),
    path('wards/<int:county_id>/', get_wards, name='get_wards'),
    path('manage-counties/', manage_counties, name='manage_counties'),
    path('manage-wards/<int:county_id>/', manage_wards, name='manage_wards'),
    path('noveu/', views.noveu, name='noveu'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
