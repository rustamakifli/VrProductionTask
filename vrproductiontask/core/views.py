from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView
from django.db.models import Count

from core.forms import BlogCommentForm,BlogForm
from core.models import BlogCategory,Blog,BlogComment,Tag,About,Like
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Team
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class BlogDetailView(DetailView, CreateView):
    template_name = 'blog/blog_details.html'
    model = Blog
    context_object_name = 'blog'
    form_class = BlogCommentForm
    # login_url = 'login'

    def form_valid(self, form):
        form.instance.slug = self.kwargs['slug']
        form.instance.blog = Blog.objects.get(slug=self.kwargs['slug'])
        form.instance.author = self.request.user
        try:
            parent_comment_id = int(self.request.POST.get('parent_id'))
            form.instance.parent_comment = BlogComment.objects.get(id=parent_comment_id)
        except:
            form.instance.parent_comment = None
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog=self.get_object()
        context['categories'] = BlogCategory.objects.annotate(num_blogs=Count('category_blogs')).order_by('-num_blogs')
        context['blogs'] = Blog.objects.all()
        context['recents'] = Blog.objects.order_by("-created_at")
        # cat_id = Blog.objects.get(slug=self.kwargs.get('slug'))
        # print(cat_id)
        # context['related_blogs'] = Blog.objects.filter(category__id=cat_id)
        context['comments'] = BlogComment.objects.filter(
            blog__slug=self.kwargs.get('slug')).all()
        context['comments_count'] = BlogComment.objects.filter(
            blog__slug=self.kwargs.get('slug')).all().count()
        context['comment_form'] = BlogCommentForm(
            data=self.request.POST)
        context['tags']=Tag.objects.all()
        context['blog_tags'] = Tag.objects.filter(
            blog__id=blog.id
        )
        return context


    def get_object(self):
        return Blog.objects.filter(slug=self.kwargs['slug']).first()

    def get_success_url(self):
        blog_slug = self.kwargs['slug']
        return reverse_lazy('blog_detail', kwargs = {'slug':blog_slug})


class BlogListView(ListView):
    template_name = 'blog/blog.html'
    model = Blog
    context_object_name = 'blogs'
    ordering = ('-created_at', )
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category_id') 
        tag_id = self.request.GET.get('tag_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        queryset = queryset.annotate(comment_count=Count('blog_comments'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.annotate(num_blogs=Count('category_blogs')).order_by('-num_blogs')
        context['recents'] = Blog.objects.order_by("-created_at")
        context['tags']=Tag.objects.all()
        
        return context
    
class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/add_blog.html'
    success_url = reverse_lazy('blogs')  

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class AboutView(ListView):
    template_name = 'home/about.html'
    model = About
    context_object_name = 'about'
    ordering = ('-created_at', )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about"] = About.objects.all().first()
        context['team'] = Team.objects.all()[:3]
        return context
    
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    session_key = request.session.session_key
    liked = False
    
    if request.user.is_authenticated:
        like, created = Like.objects.get_or_create(blog=blog, user=request.user)
    else:
        if session_key:
            like, created = Like.objects.get_or_create(blog=blog, session_key=session_key)
        else:
            request.session.create()
            like, created = Like.objects.get_or_create(blog=blog, session_key=request.session.session_key)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'likes_count': blog.likes.count()})