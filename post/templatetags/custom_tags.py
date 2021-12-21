from django import template
register = template.Library()

@register.filter
def shorten_naturaltime(naturaltime):
    naturaltime = naturaltime.replace('minutes','m').replace('hours','h').replace('days','d')
    naturaltime = naturaltime.replace('months','mon').replace('weeks','w').replace('week','w')
    return naturaltime