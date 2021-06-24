from django.contrib.syndication.views import Feed
from django.urls import reverse
from edl_management.models import Equipment

class LatestEntriesFeed(Feed):
    title = "E-Library"
    link = "/feed/"
    description = "Following are latest equipment avialable."

    def items(self):
        return Equipment.objects.order_by('-id')[:2]

    def item_title(self, item):
        return item.use.title

    def item_summary(self, item):
        return item.summary

    # link to url of news book.
    def item_link(self, item):
        return item.get_absolute_url()
