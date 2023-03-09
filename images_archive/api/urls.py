from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImageList.as_view(), name='images-list'),
    path('images/<str:image_name>',
         views.media_access, name='media'),
    path('<int:id>', views.ImageExpiringLink.as_view(), name='expiring-link'),
]
