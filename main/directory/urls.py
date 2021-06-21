from django.urls import path
from .views import *

urlpatterns = [
    path('api/directory/all/', directory_list),
    path('api/directory/date/', directory_date),
    path('api/directory/version/', elements_of_directory),
    path('api/directory/validate/', elements_current_directory),
    path('api/directory/element/validate/', validate_element),
    path('api/directory/current/validate/', validate_current_element),
]
