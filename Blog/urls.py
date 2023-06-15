from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListPostView.as_view(), name="home-page"),
    path("about/", views.about_page, name="about-page"),
    path("contact-me/", views.contact_page, name="contact-page"),
    path("create-post/", views.CreatePostView.as_view(), name="create-post-page"),
    path("delete-post/<pk>/", views.DeletePostView.as_view(), name="delete-post-page"),
    path("view-post/<post_id>/", views.view_post, name="view-post-page"),
    path("author-posts/<author_id>/", views.ListUserPostView.as_view(), name="author-posts-page"),
    path("edit-post/<pk>", views.PostUpdateView.as_view(template_name="blog/make-post.html"), name="edit-post-page"),
]
