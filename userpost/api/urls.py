from django.urls import path
from .views import api_post_img_view

app_name = 'userpost'

urlpatterns = [
    path('post/', api_post_img_view, name='post_image'),
]