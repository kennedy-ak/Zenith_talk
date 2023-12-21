from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()
# simple_tag = processes the data and returns a string
@register.simple_tag

def total_posts():
    return Post.published.count()


# inclusion tag = processes the data and returns a rendered templates
@register.inclusion_tag('blog/post/lastest_posts.html')

def show_latest_posts(count=5):
    lastest_posts = Post.published.order_by('-publish')[:count]

    return {'lastest_posts':lastest_posts}

@register.simple_tag

def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments = Count('comments')
    ).order_by('-total_comments')[:count]