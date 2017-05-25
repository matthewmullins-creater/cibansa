from django.conf.urls import url
from articles import views
from django.conf.urls import include
from articles import api
from rest_framework import routers

article = routers.SimpleRouter()
article.register("",api.CbArticleViewset,"article")

article_like = routers.SimpleRouter()
article_like.register("",api.CbArticleLikeViewset,"a-likes")

article_comment_like = routers.SimpleRouter()
article_comment_like.register("",api.CbArticleCommentLikeViewset,"ac-likes")

a_com_reply = routers.SimpleRouter()
a_com_reply.register("",api.CbArticleCommentReplyLikeViewset,"a-com-rep-likes")


urlpatterns = [
    url(r'^api/v1/article/',include(article.urls,namespace="article-api")),
    url(r'^api/v1/article-likes/', include(article_like.urls,namespace="article-likes-api")),
    url(r'^api/v1/article-comment-likes/', include(article_comment_like.urls,namespace="article-cl-api")),
    url(r'^api/v1/article-cr-likes/', include(a_com_reply.urls,namespace="article-crl-api")),
    url(r'^view/(?P<id>[0-9]+)',views.view_article,name="view-article")
]