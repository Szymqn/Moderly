from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Photo, Slider
from products.models import Comment
from .forms import AddPhotoToSliderForm, CreateSliderForm, UploadPhotoForm, ChooseSliderForm


def home(request):
    user_events = Comment.objects.all()

    return render(request, 'base/home.html', {
        'current_user': request.user if request.user.is_authenticated else None,
        'user_events': user_events,
    })


@user_passes_test(lambda u: u.is_superuser)
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
    selected_slider_id = request.session.get('selected_slider_id')
    if selected_slider_id:
        selected_slider = Slider.objects.get(id=selected_slider_id)
        photos = selected_slider.photos.all().order_by('sliderphoto__order')
    else:
        photos = Photo.objects.all()
    return render(request, 'base/slider.html', {'photos': photos})


@user_passes_test(lambda u: u.is_superuser)
def choose_slider(request):
    if request.method == 'POST':
        form = ChooseSliderForm(request.POST)
        if form.is_valid():
            selected_slider = form.cleaned_data['slider']
            request.session['selected_slider_id'] = selected_slider.id
            return redirect('slider')
    else:
        form = ChooseSliderForm()
    return render(request, 'base/choose_slider.html', {'form': form})
