from django.db import models
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    moderator = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    reported_by = models.ManyToManyField(CustomUser, related_name='reported_products', blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    reply = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.user} on {self.product}'


class Discussion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='discussions')
    moderator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='moderator_discussions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discussions')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Discussion between {self.user} and {self.moderator} on {self.product}'


class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Event for {self.user}'
