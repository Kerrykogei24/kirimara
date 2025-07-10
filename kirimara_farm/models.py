# properties/models.py
from django.db import models




class Image(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    
class Gallery(models.Model):  
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
    
class Video(models.Model):
    video = models.FileField(upload_to='gallery/videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video.name
   



class ImageDetail(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=100)
    detail_image = models.ImageField(upload_to='detail_images/',null=True)

    def __str__(self):
        return self.title
    

class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)