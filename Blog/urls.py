from django.urls import path
from . import views
urlpatterns=[
    path('', views.index_page,name="home-page"),
    path('about/',views.about_page,name='about-page'),
    path('contact-me/',views.contact_page,name='contact-page'),

]