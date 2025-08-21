from django.urls import path, include, re_path
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
    path('api/v1/',include(category.urls)),
    path('api/v1/',include(topics.urls)),
    path('api/v1/',include(questions.urls)),
    path('api/v1/',include(answer_like.urls)),
    path('api/v1/',include(answer_reply_like.urls)),
    path('topic-by-category',views.get_topic_by_category,name="topic-by-category"),
    path('tag-auto-complete',views.tag_search,name="tag-auto-complete"),
    path('tag-auto-complete',views.tag_search,name="tag-auto-complete"),
    path('question-auto-complete',views.question_auto_complete,name="question-auto-complete"),
    path('contact-thank-you',views.contact_thank_you,name="contact-thank-you"),

    # path('category/(?P<slug>[\w|\W\-]+)/list-topic/',views.list_topic,name="list-topic"),
    # path('',views.index,name="home-page"),
]