from django import template
from ..models import Article, Category
from django.db.models import Count, Q
from datetime import datetime, timedelta 

register = template.Library()


@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    return {
        "category": Category.objects.filter(status=True)
    }




@register.inclusion_tag("registration/partials/link.html")
def link(request, link_name, content, classes):
    return {
        "request":request,
        "link_name":link_name,
        "link":"account:{}".format(link_name),
        "content":content,
        "classes":classes,
    }