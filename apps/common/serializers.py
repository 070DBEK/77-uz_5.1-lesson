from rest_framework import serializers
from .models import Region, District, StaticPage, Setting


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class RegionWithDistrictsSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'districts']


class StaticPageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ['slug', 'title']


class StaticPageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ['slug', 'title', 'content', 'created_at', 'updated_at']


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['phone', 'support_email', 'working_hours', 'app_version', 'maintenance_mode']
