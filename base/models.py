from django.db import models
from PIL import Image

# Create your models here.


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        max_size = (800, 800)

        img.thumbnail(max_size, Image.LANCZOS)
        img.save(self.image.path)


class Slider(models.Model):
    name = models.CharField(max_length=100)
    photos = models.ManyToManyField(Photo, through='SliderPhoto')


class SliderPhoto(models.Model):
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
