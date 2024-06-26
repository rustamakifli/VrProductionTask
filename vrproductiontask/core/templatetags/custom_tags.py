
from django.template import Library
from core.models import Blog
from core.models import  WebsiteSetting

register = Library()

@register.simple_tag
def get_blogs(offset, limit, order):
    
    if order > 0:
        return Blog.objects.all().order_by('created_at')[offset:limit]
    return Blog.objects.all().order_by('-created_at')[offset:limit]

@register.simple_tag
def related_blog_categories(offset,limit):
    print("custom tags")
    return Blog.objects.all().order_by('category')[offset:limit]


@register.simple_tag()
def get_website_settings():
    website_setting = WebsiteSetting.objects.first()
    print("ooooo",website_setting)
    return website_setting