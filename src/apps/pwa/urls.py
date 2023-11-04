from django.urls import path
from .views import offline, serviceworker, manifest

app_name = 'pwa'
urlpatterns = [
    path("offline", offline, name="offline"),
    path('serviceworker.js', serviceworker, name='serviceworker'),
    path('manifest.json', manifest, name='manifest'),
]

