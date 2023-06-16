from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListPostView.as_view(), name="home-page"),
    path("about/", views.AboutPage.as_view(), name="about-page"),
    path("contact-me/", views.ContactPage.as_view(), name="contact-page"),
    path("create-post/", views.CreatePostView.as_view(), name="create-post-page"),
    path("delete-post/<pk>/", views.DeletePostView.as_view(), name="delete-post-page"),
    path("view-post/<post_id>/", views.ViewPost.as_view(), name="view-post-page"),
    path("author-posts/<author_id>/", views.ListUserPostView.as_view(), name="author-posts-page"),
    path("edit-post/<pk>", views.PostUpdateView.as_view(template_name="blog/make-post.html"), name="edit-post-page"),
]
