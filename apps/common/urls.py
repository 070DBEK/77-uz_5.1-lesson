from django.urls import path
from . import views


urlpatterns = [
    path('regions-with-districts/', views.RegionWithDistrictsView.as_view(), name='regions-with-districts'),
    path('pages/', views.StaticPageListView.as_view(), name='static-pages-list'),
    path('pages/<slug:slug>/', views.StaticPageDetailView.as_view(), name='static-page-detail'),
    path('setting/', views.SettingView.as_view(), name='setting'),
]
