from django.shortcuts import render
from main.models import Contact, Home, About
from .forms import ContactForm
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.http import JsonResponse

# Create your views here.


def home(request):
    site = Home.objects.latest('updated')
    about = About.objects.latest('updated')

    print(about.addresses.first().address)

    context = {
        'site': site,
        'about': about,
    }

    return render(request, 'front/main/index.html', context)


class AboutView(TemplateResponseMixin, View):
    template_name = 'front/main/about.html'

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        return self.render_to_response({'site': site, 'about': about})


class ContactView(TemplateResponseMixin, View):
    template_name = 'front/main/contact.html'
    model = Contact

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        form = ContactForm()
        return self.render_to_response({'site': site, 'about': about, 'form': form})

    def post(self,	request,	*args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.save()
            contact_email = form.cleaned_data['email']
            email_subject = f'Major project new contact: {form.cleaned_data["name"]}, {form.cleaned_data["email"]}'
            email_message = form.cleaned_data['message']
            print(contact_email, email_subject, email_message)

        return JsonResponse({"success": True, "message": "Thank you for getting in touch, our team will get back to you"})
