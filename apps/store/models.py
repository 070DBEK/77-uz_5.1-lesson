from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return self.ads.filter(is_active=True).count()


class Ad(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads')
    name_uz = models.CharField(max_length=255, blank=True, null=True)
    name_ru = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description_uz = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)
    is_top = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ads'
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name_uz or self.name_ru or f'ad-{uuid.uuid4().hex[:8]}')
            self.slug = base_slug
            counter = 1
            while Ad.objects.filter(slug=self.slug).exists():
                self.slug = f'{base_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz or self.name_ru or f'Ad #{self.id}'

    @property
    def name(self):
        return self.name_uz or self.name_ru

    @property
    def description(self):
        return self.description_uz or self.description_ru

    @property
    def main_photo(self):
        photo = self.photos.filter(is_main=True).first()
        return photo.image.url if photo and photo.image else None


class AdPhoto(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='ads/')
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ad_photos'
        verbose_name = 'Ad Photo'
        verbose_name_plural = 'Ad Photos'

    def save(self, *args, **kwargs):
        if self.is_main:
            # Set all other photos of this ad as non-main
            AdPhoto.objects.filter(ad=self.ad, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)


class FavouriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites', null=True, blank=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='favourites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favourite_products'
        verbose_name = 'Favourite Product'
        verbose_name_plural = 'Favourite Products'
        unique_together = [['user', 'product'], ['device_id', 'product']]


class MySearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    search_query = models.CharField(max_length=255, blank=True, null=True)
    price_min = models.PositiveIntegerField(blank=True, null=True)
    price_max = models.PositiveIntegerField(blank=True, null=True)
    region_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'my_searches'
        verbose_name = 'My Search'
        verbose_name_plural = 'My Searches'


class PopularSearchTerm(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='search_icons/', blank=True, null=True)
    search_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'popular_search_terms'
        verbose_name = 'Popular Search Term'
        verbose_name_plural = 'Popular Search Terms'
        ordering = ['-search_count']

    def __str__(self):
        return self.name
