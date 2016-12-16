from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^quotes$', views.quotes),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^addquote$', views.addquote),
    url(r'^favorite$', views.addtofavorites),
    url(r'^remove$', views.removefavorite),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^logout$', views.logout),
    url(r'^user$', views.user)
]
