from django.shortcuts import render

def index_page(request):
    return render(request,"blog/index.html")

def about_page(request):
    return render(request,"blog/about.html")

def contact_page(request):
    return render(request,"blog/contact.html")