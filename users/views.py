from django.shortcuts import render
from main.models import Home, About, SchoolLevel, Specialisation

# Create your views here.
genders = ["Male", 'Female']


def user_profile(request):
    site = Home.objects.latest('updated')
    about = About.objects.latest('updated')
    school_levels = SchoolLevel.objects.all()
    specializations = Specialisation.objects.all()

    current_user = request.user

    context = {
        'site': site,
        'about': about,
        'user': current_user,
        'school_levels': school_levels,
        'specializations': specializations,
        'genders': genders,

    }
    return render(request, 'front/user_profile.html', context)
