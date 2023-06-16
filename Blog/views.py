from django.http import HttpRequest, HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from Blog.forms import CommentForm, ContactForm
from Blog.models import BlogPost,Comments
from User.models import CustomUser
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView,CreateView,DeleteView,UpdateView,TemplateView,FormView

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin




class ListPostView(ListView):
    model=BlogPost
    template_name= "blog/index.html"
    context_object_name="all_post"
    ordering=['-date']
    paginate_by = 5



class AboutPage(TemplateView):
    template_name="blog/about.html"


class ContactPage(SuccessMessageMixin,FormView):
    template_name="blog/contact.html"
    form_class=ContactForm
    success_url="/contact-me/"
    success_message="Your message was sent successfully"

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)




class CreatePostView( LoginRequiredMixin, CreateView):
    model=BlogPost
    fields=["title", "subtitle", "img_url", "content"]
    template_name="blog/make-post.html"
    #if get_absolute_url is not defined in the BlogPost model, use:
    # success_url="/"
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=BlogPost
    fields = ["title", "subtitle", "img_url", "content"]
    #if get_absolute_url is not defined in the BlogPost model, use:
    # success_url="/view-post/<post_id>/"

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else:
            return False




class DeletePostView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=BlogPost
    template_name='blog/post_confirm_delete.html'
    success_url= '/'

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else:
            return False


class ViewPost(CreateView):
    model=Comments
    # fields=['comment']
    template_name="blog/post.html"
    form_class=CommentForm

    
    def get_context_data(self, **kwargs):
        context= super(ViewPost,self).get_context_data(**kwargs)
        context['comments']=Comments.objects.filter(post_id=self.kwargs.get('post_id'))
        context['post']=BlogPost.objects.get(id=self.kwargs.get('post_id'))
        return context
    
    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            post=BlogPost.objects.get(id=self.kwargs.get('post_id'))
            try:
                comment=Comments(comment=form.cleaned_data.get('comment'),author=self.request.user, post=post)
                comment.save()
                return redirect('view-post-page',post_id=post.id)
            except ValueError:
                messages.add_message(
                    request, messages.WARNING, "You have to log in first"
                )
                return redirect("login")

        else:
            return self.render_to_response(
              self.get_context_data(form=form))
        

    def get_success_url(self):
        return reverse('view-post-page')
    

    


class ListUserPostView(ListView):
    model=BlogPost
    template_name='blog/author-posts.html'
    context_object_name="all_post"
    paginate_by = 2

    def get_queryset(self):
        author_id=get_object_or_404(CustomUser,id=self.kwargs.get('author_id'))
        return BlogPost.objects.filter(author_id=author_id)
    
