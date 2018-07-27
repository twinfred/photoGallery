from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    url(r'^admin$', views.admin), # admin_dash.html

    # Homepage
    url(r'^$', views.index), # index.html

    # Login/Reg
    url(r'^login$', views.login), # login.html
    url(r'^register$', views.register), # register.html
    url(r'^logout$', views.logout), # logout user

    # Images
    url(r'images$', views.images),
    url(r'images/(?P<image_id>\w+)$', views.images),
    url(r'images/like/(?P<image_id>\w+)$', views.like),

    # Catch-All
    url(r'^', views.home), # Redirect to /images
]