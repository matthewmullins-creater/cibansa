from main.models import CbCategory
from django.db.models import Count
from operator import itemgetter


def get_top_category():
    # c = CbCategory.objects.annotate().order_by("-topic_count")[:4]
    cat = CbCategory.objects.annotate(topic_count=Count("category_topics")).order_by("-topic_count")[:4]
    a = []
    for c in cat:
        question = c.category_questions.count()
        d = {"topic_count": c.topic_count,"question_count":question,"category_name":c.name,"slug":c.slug}
        a.append(d)

    a.sort(key=itemgetter("question_count","topic_count"), reverse=True)
    return a


