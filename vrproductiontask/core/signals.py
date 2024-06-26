from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from core.models import Blog
from slugify import slugify


# @receiver(pre_save, sender=Blog)
# def story_object_creation(sender, instance, **kwargs):
#     instance.slug = f"{slugify(instance.title)}-{instance.id}"


@receiver(post_save, sender=Blog)
def story_object_creation(sender, instance, created, **kwargs):
    # print(created)
    old_slug = instance.slug
    new_slug = f"{slugify(instance.title)}-{instance.id}"
    if old_slug != new_slug:
        instance.slug = new_slug
        instance.save()
        # print('isledi')

from core.utils import soup
from core.models import WebsiteSetting

@receiver(post_save, sender=WebsiteSetting)
def update_google_maps(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # Don't process if the instance is being created
        return

    map_html = instance.map
    iframe_src = soup.extract_iframe_src(map_html)

    if iframe_src:
        instance.map = iframe_src
        instance.save()
        print(iframe_src)