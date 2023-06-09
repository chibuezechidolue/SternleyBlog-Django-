from turtle import title
from django.shortcuts import redirect, render
from Blog.forms import CreateBlogPost
from Blog.models import BlogPost
from User.models import CustomUser

def index_page(request):
    all_posts=BlogPost.objects.all()
    return render(request,"blog/index.html",{'all_posts':all_posts})

def about_page(request):
    return render(request,"blog/about.html")

def contact_page(request):
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
    return render(request,'blog/post.html',{"post":post})