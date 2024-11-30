from django.contrib import admin
from .models import Category, Product, Comment, Discussion, Event

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Discussion)
admin.site.register(Event)
