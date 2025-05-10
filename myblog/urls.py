
from django.contrib import admin
from django.urls import path, include
from blog.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing'),
    path('home/', home, name='home'),
    path('form/' , form , name='form'),
    path('login/', login_page , name='login'),
    path('register/' , register , name='register'),
    path('logout/' , logout_page , name='logout'),
    path('update-profile-pic/',update_profile_pic, name='update_profile_pic'),
    path('my-posts/', my_posts, name='my_posts'),
    path('edit-post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
