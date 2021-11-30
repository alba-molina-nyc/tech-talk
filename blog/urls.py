from django.urls import path
from . import views

app_name = 'blog_urls'
urlpatterns = [
path("", views.home, name = "home"),
path("about/", views.about, name = "about"),
path("blogs/", views.BlogIndex.as_view(), name = "index"),
path("blogs/create", views.BlogCreate.as_view(), name = "blog_create"),
path("blogs/<int:pk>/", views.blogs_detail, name = "detail"),
path("blogs/<int:pk>/update/", views.BlogUpdate.as_view(), name = "blog_update"),
path("blogs/<int:pk>/delete/", views.BlogDelete.as_view(), name = "blog_delete"),
path("blogs/<int:pk>/add_comment/", views.add_comment, name = "add_comment"),
path("blogs/<int:pk>/edit_comment/", views.EditComment.as_view(),  name = "edit_comment"),
path("blogs/<int:blog_id>/delete_comment/<int:pk>", views.DeleteComment.as_view(),  name = "delete_comment"),
path("blogs/explore", views.Explore.as_view(), name= "explore"),
]