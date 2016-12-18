from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^pokes$', views.pokes),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^pokeuser$', views.pokeuser),
    url(r'^logout$', views.logout)
]
