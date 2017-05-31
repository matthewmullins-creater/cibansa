from django.conf.urls import url
from django.conf.urls import include
from main import api
from main import views
from rest_framework import routers

category = routers.SimpleRouter()
category.register(r'category',api.CbCategoryViewset,"category")

topics = routers.SimpleRouter()
topics.register(r'topics',api.CbTopicViewset,"topic")

questions = routers.SimpleRouter()
questions.register(r'questions',api.CbQuestionViewset,"question")

answer_like = routers.SimpleRouter()
answer_like.register(r'answer-like',api.CbAnswerLikeViewset,"answer-like")

answer_reply_like = routers.SimpleRouter()
answer_reply_like.register(r'answer-reply-like',api.CbAnswerReplyLikeViewset,"answer-reply-like")


urlpatterns = [
    url(r'^api/v1/',include(category.urls,namespace="category-api")),
    url(r'^api/v1/',include(topics.urls,namespace="topic-api")),
    url(r'^api/v1/',include(questions.urls,namespace="question-api")),
    url(r'^api/v1/',include(answer_like.urls,namespace="answer-like-api")),
    url(r'^api/v1/',include(answer_reply_like.urls,namespace="answer-reply-like-api")),
    url(r'^topic-by-category',views.get_topic_by_category,name="topic-by-category"),
    url(r'^tag-auto-complete',views.tag_search,name="tag-auto-complete"),
    url(r'^tag-auto-complete',views.tag_search,name="tag-auto-complete"),
    url(r'^question-auto-complete',views.question_auto_complete,name="question-auto-complete"),
    url(r'^contact-thank-you',views.contact_thank_you,name="contact-thank-you"),

    # url(r'^category/(?P<slug>[\w|\W\-]+)/list-topic/',views.list_topic,name="list-topic"),
    # url(r'^$',views.index,name="home-page"),
]