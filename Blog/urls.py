from django.urls import path
from . import views
urlpatterns=[
    path('', views.index_page,name="home-page"),
    path('about/',views.about_page,name='about-page'),
    path('contact-me/',views.contact_page,name='contact-page'),
    path('create-post/',views.create_post,name='create-post-page'),
    path('view-post/<post_id>/',views.view_post,name='view-post-page'),
]