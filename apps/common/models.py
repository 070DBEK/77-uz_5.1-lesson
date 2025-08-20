from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'regions'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        ordering = ['name']

    def __str__(self):
        return self.name


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'districts'
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        ordering = ['name']

    def __str__(self):
        return f"{self.region.name} - {self.name}"


class StaticPage(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'static_pages'
        verbose_name = 'Static Page'
        verbose_name_plural = 'Static Pages'
        ordering = ['title']

    def __str__(self):
        return self.title or self.slug


class Setting(models.Model):
    phone = models.CharField(max_length=15, blank=True, null=True)
    support_email = models.EmailField(blank=True, null=True)
    working_hours = models.CharField(max_length=255, blank=True, null=True)
    app_version = models.CharField(max_length=20, blank=True, null=True)
    maintenance_mode = models.BooleanField(default=False)

    class Meta:
        db_table = 'settings'
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return "Application Settings"
