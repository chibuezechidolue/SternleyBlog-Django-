from turtle import title
from django.shortcuts import redirect, render
from Blog.forms import CreateBlogPost,CommentForm
from Blog.models import BlogPost, Comments
import smtplib
import os
from dotenv import load_dotenv
from django.contrib import messages


load_dotenv()





def index_page(request):
    all_posts=BlogPost.objects.all()
    return render(request,"blog/index.html",{'all_posts':all_posts})

def about_page(request):
    return render(request,"blog/about.html")

def contact_page(request):
    if request.method=="POST":
        content=request.POST
        email=content.get('email')
        name=content.get('name')
        message=content.get('message')
        phone=content.get('phone')
        messages.add_message(request, messages.SUCCESS, "Your message was sent successfully")

        with smtplib.SMTP_SSL('smtp.gmail.com') as connection:
            connection.login(user=os.environ.get('SENDING_EMAIL'), password=os.environ.get('SENDING_EMAIL_PASSWORD'))
            connection.sendmail(from_addr=os.environ.get('SENDING_EMAIL'),
                                to_addrs = os.environ.get('RECEIVING_EMAIL'),
                                msg = f'Subject:Message from portfolio website'f'\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}')
        
    return render(request,"blog/contact.html")

def create_post(request):
    form=CreateBlogPost()
    if request.method=="POST":
        form=CreateBlogPost(request.POST)
        if form.is_valid():
            print('is valid')
            new_post=BlogPost(title=form.cleaned_data["title"],subtitle=form.cleaned_data["subtitle"],
                          img_url=form.cleaned_data["img_url"],content=form.cleaned_data["content"],
                          author=request.user
                          )
        new_post.save()
        return redirect('home-page')

    return render(request, "blog/make-post.html", {"form":form})

def view_post(request,post_id):
    post=BlogPost.objects.get(id=post_id)
    form=CommentForm()
    all_comments=Comments.objects.filter(post_id=post_id).all()
    # avatar_url=gravatar_url(email=post.author.email,size=40)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=Comments(comment=form.cleaned_data['comment'],author=request.user,post=post)
            comment.save()
        return redirect('view-post-page',post_id=post.id)
    return render(request,'blog/post.html',{"post":post,"form":form,"all_comments":all_comments})

def author_posts(request,author_id):
    posts=BlogPost.objects.filter(author_id=author_id).all()
    print(posts)

    return render(request,'blog/author-posts.html', {"posts":posts})