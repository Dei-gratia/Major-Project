from django.shortcuts import render
from main.models import Home, About

# Create your views here.


def home(request):
    site = Home.objects.latest('updated')
    about = About.objects.latest('updated')

    print(about.addresses.first().address)

    context = {
        'site': site,
        'about': about,
    }

    return render(request, 'front/index.html', context)
