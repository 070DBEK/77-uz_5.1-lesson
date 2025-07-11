from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Ad, AdPhoto, FavouriteProduct, MySearch, PopularSearchTerm

User = get_user_model()


class CategoryListSerializer(serializers.ModelSerializer):
    product_count = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'product_count']


class CategoryWithChildrenSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'children']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategoryListSerializer(children, many=True).data


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'profile_photo']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AdListSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    photo = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    updated_time = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'name', 'slug', 'price', 'photo', 'published_at', 'address', 'seller', 'is_liked',
                  'updated_time']

    def get_photo(self, obj):
        return obj.main_photo

    def get_address(self, obj):
        # Get seller's default address
        address = obj.seller.addresses.filter(is_default=True).first()
        return address.name if address else ""

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favourites.filter(user=request.user).exists()
        return False


class AdDetailSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    photos = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    updated_time = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'name', 'slug', 'description', 'price', 'photos', 'published_at', 'address', 'seller',
                  'category', 'is_liked', 'view_count', 'updated_time']

    def get_photos(self, obj):
        return [photo.image.url for photo in obj.photos.all()]

    def get_address(self, obj):
        address = obj.seller.addresses.filter(is_default=True).first()
        return address.name if address else ""

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favourites.filter(user=request.user).exists()
        return False


class AdCreateSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.URLField(), write_only=True)

    class Meta:
        model = Ad
        fields = ['name_uz', 'name_ru', 'category', 'description_uz', 'description_ru', 'price', 'photos']

    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])
        validated_data['seller'] = self.context['request'].user
        ad = super().create(validated_data)

        # Create photo objects
        for i, photo_url in enumerate(photos_data):
            AdPhoto.objects.create(
                ad=ad,
                image=photo_url,
                is_main=(i == 0)
            )

        return ad


class MyAdSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    updated_time = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'name', 'slug', 'price', 'photo', 'published_at', 'address', 'status', 'view_count', 'is_liked',
                  'updated_time']

    def get_photo(self, obj):
        return obj.main_photo

    def get_address(self, obj):
        address = obj.seller.addresses.filter(is_default=True).first()
        return address.name if address else ""

    def get_is_liked(self, obj):
        return False  # For my ads, this is always false


class MyAdDetailSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    updated_time = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'name', 'slug', 'description', 'category', 'price', 'photos', 'published_at', 'status',
                  'view_count', 'updated_time']

    def get_photos(self, obj):
        return [photo.image.url for photo in obj.photos.all()]


class AdUpdateSerializer(serializers.ModelSerializer):
    new_photos = serializers.ListField(child=serializers.URLField(), write_only=True, required=False)

    class Meta:
        model = Ad
        fields = ['name', 'category', 'description', 'price', 'new_photos']

    def update(self, instance, validated_data):
        new_photos = validated_data.pop('new_photos', [])

        # Update ad fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Add new photos if provided
        if new_photos:
            for photo_url in new_photos:
                AdPhoto.objects.create(
                    ad=instance,
                    image=photo_url,
                    is_main=False
                )

        return instance


class FavouriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteProduct
        fields = ['product']


class FavouriteProductByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteProduct
        fields = ['device_id', 'product']


class FavouriteProductResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteProduct
        fields = ['id', 'product', 'device_id', 'created_at']


class MyFavouriteProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name')
    slug = serializers.CharField()
    description = serializers.CharField(source='description')
    photo = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    updated_time = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'name', 'slug', 'description', 'price', 'published_at', 'address', 'seller', 'photo',
                  'is_liked', 'updated_time']

    def get_photo(self, obj):
        return obj.main_photo

    def get_address(self, obj):
        address = obj.seller.addresses.filter(is_default=True).first()
        return address.name if address else ""

    def get_seller(self, obj):
        return obj.seller.full_name

    def get_is_liked(self, obj):
        return True


class MySearchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MySearch
        fields = ['category', 'search_query', 'price_min', 'price_max', 'region_id']


class MySearchResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MySearch
        fields = ['id', 'category', 'search_query', 'price_min', 'price_max', 'region_id', 'created_at']


class MySearchDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)

    class Meta:
        model = MySearch
        fields = ['id', 'category', 'search_query', 'price_min', 'price_max', 'region_id', 'created_at']


class ProductImageCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = AdPhoto
        fields = ['id', 'image', 'is_main', 'product_id', 'created_at']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        try:
            ad = Ad.objects.get(id=product_id)
            validated_data['ad'] = ad
            return super().create(validated_data)
        except Ad.DoesNotExist:
            raise serializers.ValidationError("Product not found")


class SearchResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    icon = serializers.URLField(required=False)


class SearchCompleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.URLField(required=False)


class PopularSearchTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularSearchTerm
        fields = ['id', 'name', 'icon', 'search_count']


class PopularSearchIncreaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularSearchTerm
        fields = ['id', 'category', 'search_count', 'updated_at']
