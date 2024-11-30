from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Photo
from .forms import AddPhotoToSliderForm, CreateSliderForm, UploadPhotoForm


def home(request):
    context = {
        'current_user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'home.html', context)


def upload_photo(request):
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('slider')
    else:
        form = UploadPhotoForm()
    return render(request, 'base/upload_photo.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def add_photo_to_slider(request):
    if request.method == 'POST':
        form = AddPhotoToSliderForm(request.POST)
        if form.is_valid():
            slider = form.cleaned_data['slider']
            photo = form.cleaned_data['photo']
            slider.photos.add(photo)
            return redirect('slider')
    else:
        form = AddPhotoToSliderForm()
    return render(request, 'base/add_photo_to_slider.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def create_slider(request):
    if request.method == 'POST':
        form = CreateSliderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('slider')
    else:
        form = CreateSliderForm()
    return render(request, 'base/create_slider.html', {'form': form})


def slider(request):
    photos = Photo.objects.all().order_by('order')
    return render(request, 'base/slider.html', {'photos': photos})
