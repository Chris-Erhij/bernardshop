from django.db import models
from django.db.models import (
    Model, CharField, SlugField, ForeignKey, ImageField, TextField, DecimalField, BooleanField,
    DateTimeField,
    )
from django.urls import reverse

class Category(Model):
    name: CharField = models.CharField(max_length=200)
    slug: SlugField = models.SlugField(max_length=200, unique=True)

    # Meta class for model, for ordering and indexing.
    class Meta:
        ordering = ['name']
        indexes =  [
            models.Index(fields=['name'])
        ]
        verbose_name: str = 'category'
        verbose_name_plural: str = 'categories'

    def __str__(self) -> str | CharField:
        return self.name
    
    def get_absolute_url(self) -> reverse:
        return reverse('eshop:product_list_by_category', args=(self.slug,))


class Product(Model):
    category: ForeignKey = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name: CharField = models.CharField(max_length=200)
    slug: SlugField = models.SlugField(max_length=200)
    Image: ImageField = models.ImageField(upload_to='products/%y/%m/%d', blank=True)
    description: TextField = models.TextField(blank=True)
    price: DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    available: BooleanField = models.BooleanField(default=True)
    created: DateTimeField = models.DateTimeField(auto_now_add=True)
    updated: DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self) -> str | CharField:
        return self.name

    def get_absolute_url(self) -> reverse:
        return reverse('eshop:product_detail', args=(self.id, self.slug,))
    