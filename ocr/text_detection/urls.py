from django.urls import path
from .views import process_image, home, download_result, result


urlpatterns = [
    path('', home, name='home'),
    path('process_image', process_image, name='process_image'),
    path('result', result, name='result'),
    path('download', download_result, name='download'),

]
