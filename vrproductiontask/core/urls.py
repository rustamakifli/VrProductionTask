from django.urls import path
from . import views as template_views

urlpatterns = [
   path('blogs/',template_views.BlogListView.as_view(), name="blogs"),  
   path('blogs/<slug:slug>/',template_views.BlogDetailView.as_view(), name="blog_detail"),  
   path('blog-create/',template_views.BlogCreateView.as_view(), name="blog_create"),
   path('about/',template_views.AboutView.as_view(), name="about"),
   path('like/<int:blog_id>/', template_views.like_blog, name='like_blog'),

]