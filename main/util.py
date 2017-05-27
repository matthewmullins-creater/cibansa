from main.models import CbCategory
from django.db.models import Count
from operator import itemgetter


def get_top_category():
    # c = CbCategory.objects.annotate().order_by("-topic_count")[:4]
    cat = CbCategory.objects.annotate(topic_count=Count("category_topics")).order_by("-topic_count")[:4]
    a = []
    for c in cat:
        question = c.category_questions.count()
        discussion = 0
        for q in c.category_questions.all():

            discussion += q.question_answers.count()
            for k in q.question_answers.all():
                discussion += k.answer_replies.count()

        d = {"topic_count": c.topic_count,"question_count":question,"category_name":c.name,"slug":c.slug,
             "discussion":discussion,"url": c.image.url}
        a.append(d)

    a.sort(key=itemgetter("question_count","topic_count"), reverse=True)
    return a


