from django.conf.urls import include, url

urlpatterns = [
    url(r'^distance/', include('apps.distance.urls')),
]
