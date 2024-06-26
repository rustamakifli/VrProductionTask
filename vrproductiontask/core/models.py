from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from ckeditor.fields import RichTextField
from core.utils import tools


User = get_user_model()


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BlogCategory(models.Model):
    parent_cat = models.ForeignKey('self', related_name='category_sub_cat', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    title = models.CharField(max_length=100, db_index=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title

class Blog(AbstractModel):
    author = models.ForeignKey(User, related_name='author_blogs', on_delete=models.CASCADE, default=1)
    category = models.ManyToManyField(BlogCategory, related_name='category_blogs')
    title = models.CharField(max_length=250, db_index=True)
    image = models.ImageField(upload_to='blog_images')
    description = models.CharField(max_length=255)
    content = RichTextField()
    # is_quote = models.BooleanField(default=False)
    # quote = RichTextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(max_length=70, editable=False, db_index=True) 


    def get_absolute_url(self):
        return reverse_lazy('blog_detail', kwargs={
            'slug': self.slug
        })


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title


class BlogComment(AbstractModel):
    parent_comment = models.ForeignKey('self', related_name='child_comments', on_delete=models.CASCADE, null=True, blank=True, )
    blog = models.ForeignKey(Blog, related_name='blog_comments', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, related_name='user_blog_comments', on_delete=models.CASCADE, default=1)
    comment = models.TextField()

    class Meta:
        verbose_name = 'Blog comment'
        verbose_name_plural = 'Blog comments'

    def __str__(self):
        return f'{self.comment} - {self.blog} ({self.user})' 

    def children(self):
        return BlogComment.objects.filter(parent_comment=self)

    @property
    def is_parent(self):
        if self.parent_comment is not None:
            return False
        return True
    
class About(AbstractModel):
    title = models.CharField(max_length=250)
    content = RichTextField()
    image = models.ImageField(upload_to='about_images')
    top_services = RichTextField()

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'Abouts'

    def __str__(self):
        return self.title
    
class WebsiteSetting(AbstractModel):
    # logo = models.ImageField(upload_to=tools.get_logo_ref_images, null=True)
    # favicon = models.ImageField(upload_to=tools.get_logo_ref_images, null=True, blank=True)
    header_social_accounts = models.ManyToManyField(
        'SocialAccount',
        related_name = 'settings',
        blank=True,
        verbose_name="Social Accounts",
    )
    # playstore_link = models.URLField("Play Store link", null=True, blank=True)
    # appstore_link = models.URLField("App Store link", null=True, blank=True)
    contact_number = models.CharField(max_length=50, null=True, blank=True)
    contact_email = models.EmailField(
        verbose_name=('Əlaqə E-poçt'),
        null=True, blank=True
    )
    address = RichTextField(
        verbose_name=('Adres'),
        null=True, blank=True
    )
    work_hours = models.CharField(max_length=300, null=True, blank=True)

    map = models.TextField(
        verbose_name=('Map'),
        null=True, blank=True
    )
    # meta_keywords = models.TextField(null=True, blank=True)
    # meta_description = models.TextField(null=True, blank=True)
    

    
class SocialAccount(AbstractModel):
    social = models.CharField(choices=tools.SOCIAL_CHOICES,max_length=50)
    link = models.URLField()
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = ("Social Accounts")

    def __str__(self):
        return self.social
    
class Like(AbstractModel):
    blog = models.ForeignKey(Blog, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        unique_together = ('blog', 'user', 'session_key')