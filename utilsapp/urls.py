from django.urls import path

from utilsapp.views import IndexView


app_name = 'utilsapp'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]