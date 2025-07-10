from urllib import request
from django.shortcuts import get_object_or_404, render,redirect
from .forms import ImageDetailForm,ContactForm,SubscribeForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponseNotFound
from itertools import zip_longest



# Create your views here.

from django.views.generic import ListView,DetailView
from .models import  Image,Contact,Gallery,Video




def home(request):
    images = Image.objects.all().order_by('title')
    return render (request, 'index.html',{'images': images})





def image_detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
   

    return render(request, 'image_detail.html', {'image': image})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save the form data to the database
            contact_instance = Contact.objects.create(
                name=name, email=email, phone=phone, subject=subject, message=message
            )

            # Send email to yourself
            send_mail(
                f'Florance Rest House: {subject}',
                f'Name: {name}\n\nEmail: {email}\n\nPhone Number: {phone}\n\nMessage:\n{message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            # Send confirmation email to the user
            client_message = render_to_string('email/client_message.txt', {'name': name})
            send_mail(
                'Thank you for contacting us!',
                strip_tags(client_message),
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=client_message,
                fail_silently=False,
            )

            # Send email to the specified email address from the .env file
            if settings.SPECIFIED_EMAIL:
                send_mail(
                    f'Kirimara Coffee Estate: {subject}',
                    f'Name: {name}\n\nEmail: {email}\n\nPhone Number: {phone}\n\nSubject: {subject}\n\nMessage:\n{message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.SPECIFIED_EMAIL],
                    fail_silently=False,
                )

            return redirect('success_page')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def success( request):
    return render (request, 'success_page.html')


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            # Add any additional logic here, such as sending a confirmation email
            return redirect('success_page')  # Redirect to a success page
    else:
        form = SubscribeForm()

    return render(request, 'footer.html', {'form': form})


def about(request):
    return render(request, 'about.html')


def gallery(request):
    images = Gallery.objects.all().order_by('-created_at')
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'gallery.html', {'images': images, 'videos': videos})


def services(request):
    images = Image.objects.all()
    return render (request, 'service.html',{'images': images})
   


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)