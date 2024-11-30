from django.db import models
from PIL import Image
from users.models import CustomUser

# Create your models here.


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        max_size = (800, 800)

        img.thumbnail(max_size, Image.LANCZOS)
        img.save(self.image.path)

    def __str__(self):
        return self.title


class Slider(models.Model):
    name = models.CharField(max_length=100)
    photos = models.ManyToManyField(Photo, through='SliderPhoto')

    def __str__(self):
        return self.name


class SliderPhoto(models.Model):
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_value = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=50)
    primary_color = models.ForeignKey(Color, related_name='primary_themes', on_delete=models.CASCADE)
    secondary_color = models.ForeignKey(Color, related_name='secondary_themes', on_delete=models.CASCADE)
    tertiary_color = models.ForeignKey(Color, related_name='tertiary_themes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    selected_theme = models.ForeignKey(Theme, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username
