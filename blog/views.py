from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from .models import BlogEntry, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'tech-talk-123456'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

#Blog Views:
class BlogIndex(ListView):
    model = BlogEntry
    template_name = "blogs/index.html"

    def get_queryset(self):
        queryset = BlogEntry.objects.filter(user = self.request.user)
        return queryset
      
class BlogCreate(CreateView):
    model = BlogEntry
    fields = ('title', 'blog_text')
    def form_valid(self, form):
        # Current user added as the blog user
        form.instance.user = self.request.user
        # Handle photo uploaed
        photo_file = self.request.FILES.get('photo-file')
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            form.instance.image_url = url
        except Exception as error:
            print(f'an error occured uploading to AWS S3 ')
            print(error)
        return super().form_valid(form)



def blogs_detail(request, pk):
    blog = BlogEntry.objects.get(id = pk)
    comment_form = CommentForm()
    return render(
      request,
      "blogs/detail.html", {
          "blog": blog,
          "comment_form": comment_form,
          "user_id": request.user.id,
          "author_id": blog.user.id,
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

    
class Explore (ListView):
    model = BlogEntry
    template_name = 'blogs/explore.html'
    def get_queryset(self):
        queryset = BlogEntry.objects.exclude(user = self.request.user)
        return queryset
