from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Photo
from .forms import PhotoForm


def home(request):
    context = {
        'current_user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'home.html', context)


@user_passes_test(lambda u: u.is_superuser)
def add_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'base/add_photo.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def photo_list(request):
    photos = Photo.objects.all().order_by('order')
    return render(request, 'base/photo_list.html', {'photos': photos})


def slider(request):
    photos = Photo.objects.all()
    return render(request, 'base/slider.html', {'photos': photos})
