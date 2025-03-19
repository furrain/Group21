from django import template
from HighlandWanderer.models import Category

register = template.Library()

@register.inclusion_tag('HighlandWanderer/top_categories.html')
def show_top_categories():
    # retrieve Top 5 category
    top_categories = Category.objects.order_by('-views')[:5]
    return {'top_categories': top_categories}