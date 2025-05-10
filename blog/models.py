from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/')  # Ensure this is correct
    tags = models.CharField(max_length=255, blank=True)



    def __str__(self):
        return self.title
 
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/' , default='profile_pics/default.png')

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save , sender=User)
def save_user_profile(instance , sender , **kwargs):
    instance.profile.save()

