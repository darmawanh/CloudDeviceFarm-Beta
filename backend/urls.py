from django.conf.urls import url
from backend import views

from django.conf.urls.static import static
from django.conf import settings

from django.urls import path
urlpatterns=[
    # url(r'^trend/$', views.get_trend),
    url(r'^startdeviceandroid/$', views.start_device_android),
    url(r'^startappiumserver/$', views.create_appium_hub),
    url(r'^killdeviceandroid/$', views.kill_device_android),
    url(r'^startdeviceios/$', views.start_device_ios),
    url(r'^killdeviceios/$', views.kill_device_ios),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)