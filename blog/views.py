from django.db import models
from django.db.models import fields
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from .models import BlogEntry, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

#Blog Views:
class BlogIndex(ListView):
    model = BlogEntry
    template_name = "blogs/index.html"

    def get_queryset(self):
        queryset = BlogEntry.objects.filter()
        return queryset
      
class BlogCreate(CreateView):
    model = BlogEntry
    fields = ('title', 'blog_text', 'image_url')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def blogs_detail(request, pk):
    blog = BlogEntry.objects.get(id = pk)
    comment_form = CommentForm()

    return render(
      request,
      "blogs/detail.html", {
          "blog": blog,
          "comment_form": comment_form
           

      }
    )

class BlogUpdate(UpdateView):
    model = BlogEntry
    fields = ("title","blog_text", "image_url", "likes",  )

class BlogDelete(DeleteView):
    model = BlogEntry
    fields = ("title","blog_text", "date_posted", "image_url", "likes",  )
    success_url = '/blogs/'

def add_comment(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit = False)
        new_comment.blog_entry_id = pk
        new_comment.user = request.user
        new_comment.save()


    return redirect("blog_urls:detail", pk = pk)

class EditComment(UpdateView):
    model = Comment
    fields = ("comment_text",)

class DeleteComment(DeleteView):
    model = Comment
    def get_success_url(self):
        blog_id = self.kwargs.get('blog_id')
        return f'/blogs/{blog_id}'

    
    