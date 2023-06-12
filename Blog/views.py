from django.http import HttpResponse
from django.shortcuts import redirect, render
from Blog.forms import CreateBlogPost, CommentForm, EditBlogPost
from Blog.models import BlogPost, Comments
import smtplib
import os
from dotenv import load_dotenv
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail


load_dotenv()


def index_page(request):
    all_posts = BlogPost.objects.all()
    return render(request, "blog/index.html", {"all_posts": all_posts})


def about_page(request):
    return render(request, "blog/about.html")


def contact_page(request):
    if request.method == "POST":
        if request.POST:
            content = request.POST
            email = content.get("email")
            name = content.get("name")
            message = content.get("message")
            phone = content.get("phone")
            messages.add_message(
                request, messages.SUCCESS, "Your message was sent successfully"
            )

            # with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
            #     connection.login(
            #         user=os.environ.get("SENDING_EMAIL"),
            #         password=os.environ.get("SENDING_EMAIL_PASSWORD"),
            #     )
            # send_mail(
            #     from_addr=os.environ.get("SENDING_EMAIL"),
            #     to_addrs=os.environ.get("RECEIVING_EMAIL"),
            #     msg=f"Subject:Message from portfolio website"
            #     f"\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}",
            #     )
            send_mail(
                subject='Message from SternleyBlog',
                message=f"\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}",
                from_email=None,
                recipient_list=[os.environ.get("RECEIVING_EMAIL"),],
                

            )

    return render(request, "blog/contact.html")


@login_required
def create_post(request):
    form = CreateBlogPost()
    if request.method == "POST":
        form = CreateBlogPost(request.POST)
        if form.is_valid():
            print("is valid")
            form.save()
            #     new_post=BlogPost(title=form.cleaned_data["title"],subtitle=form.cleaned_data["subtitle"],
            #                   img_url=form.cleaned_data["img_url"],content=form.cleaned_data["content"],
            #                   author=request.user
            #                   )
            # new_post.save()
            return redirect("home-page")

    return render(request, "blog/make-post.html", {"form": form})


@login_required
def edit_post(request, post_id):
    # restrict non author
    post = BlogPost.objects.get(id=post_id)
    if not request.user.id == post.author.id:
        return HttpResponse(status=403)
    form = EditBlogPost(instance=post)
    if request.method == "POST":
        form = EditBlogPost(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return redirect("home-page")
    return render(request, "blog/make-post.html", {"is_edit": True, "form": form})


@login_required
def delete_post(request, post_id):
    # restrict non author
    post = BlogPost.objects.get(id=post_id)
    if not request.user.id == post.author.id:
        return HttpResponse(status=403)
    if request.method == "POST":
        post = BlogPost.objects.get(id=post_id)
        post.delete()
        messages.add_message(request, messages.SUCCESS, "The post has been deleted")
        return redirect("home-page")
    return render(request, "blog/post_confirm_delete.html", {"post_id": post_id})


def view_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    form = CommentForm()
    all_comments = Comments.objects.filter(post_id=post_id).all()
    # avatar_url=gravatar_url(email=post.author.email,size=40)
    if request.method == "POST":
        print("request.method")
        form = CommentForm(request.POST)
        if form.is_valid():
            print("form.is_valid")
            try:
                comment = Comments(
                    comment=form.cleaned_data["comment"], author=request.user, post=post
                )
                comment.save()
            except ValueError:
                messages.add_message(
                    request, messages.WARNING, "You have to log in first"
                )
                return redirect("login")
        return redirect("view-post-page", post_id=post.id)
    return render(
        request,
        "blog/post.html",
        {"post": post, "form": form, "all_comments": all_comments},
    )


def author_posts(request, author_id):
    posts = BlogPost.objects.filter(author_id=author_id).all()
    print(posts)

    return render(request, "blog/author-posts.html", {"posts": posts})
