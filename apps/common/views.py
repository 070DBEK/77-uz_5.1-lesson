from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Region, StaticPage, Setting
from .serializers import RegionWithDistrictsSerializer, StaticPageListSerializer, StaticPageDetailSerializer, \
    SettingSerializer


class RegionWithDistrictsView(generics.ListAPIView):
    queryset = Region.objects.all().prefetch_related('districts')
    serializer_class = RegionWithDistrictsSerializer
    permission_classes = [AllowAny]


class StaticPageListView(generics.ListAPIView):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageListSerializer
    permission_classes = [AllowAny]


class StaticPageDetailView(generics.RetrieveAPIView):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class SettingView(generics.RetrieveAPIView):
    serializer_class = SettingSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        setting, created = Setting.objects.get_or_create(id=1)
        return setting
