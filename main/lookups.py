from __future__ import unicode_literals

from selectable.base import ModelLookup
from selectable.registry import registry

from main.models import CbTag,CbCategory,CbTopic


class TagLookup(ModelLookup):
    model = CbTag
    search_fields = ('name__icontains', )


class TopicLookup(ModelLookup):
    model = CbTopic
    search_fields = ('title__icontains', )

    def get_query(self, request, term):
        results = super(TopicLookup, self).get_query(request, term)
        category = request.GET.get('category', '')
        print(category,1234)
        if category:
            results = results.filter(category=category)
        return results

    def get_item_label(self, item):
        return "{title} - {category}".format(title=item.title,category=item.category)

    def get_item_value(self,item):
        return "%s" % item.title


registry.register(TopicLookup)

registry.register(TagLookup)