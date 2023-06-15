from django.shortcuts import get_object_or_404, redirect, render
from Blog.forms import CommentForm
from Blog.models import BlogPost,Comments
from User.models import CustomUser
import os
from dotenv import load_dotenv
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import ListView,CreateView,DeleteView,UpdateView

# from django.contrib.auth.mixins import LoginRequiredMixin

load_dotenv()



class ListPostView(ListView):
    model=BlogPost
    template_name= "blog/index.html"
    context_object_name="all_post"
    ordering=['-date']
    paginate_by = 5



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



class CreatePostView( CreateView):
    model=BlogPost
    fields=["title", "subtitle", "img_url", "content"]
    template_name="blog/make-post.html"
    #if get_absolute_url is not defined in the BlogPost model
    success_url="/"
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)



class PostUpdateView(UpdateView):
    model=BlogPost
    fields = ["title", "subtitle", "img_url", "content"]
    success_url="/"




class DeletePostView(DeleteView):
    model=BlogPost
    template_name='blog/post_confirm_delete.html'
    success_url= '/'


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

class ListUserPostView(ListView):
    model=BlogPost
    template_name='blog/author-posts.html'
    context_object_name="all_post"
    paginate_by = 2

    def get_queryset(self):
        author_id=get_object_or_404(CustomUser,id=self.kwargs.get('author_id'))
        return BlogPost.objects.filter(author_id=author_id)
    
