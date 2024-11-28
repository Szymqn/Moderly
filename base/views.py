from django.shortcuts import render


def home(request):
    context = {
        'current_user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'base.html', context)
