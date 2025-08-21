from django.urls import path, include, re_path
from articles import views
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
    path('api/v1/article/',include(article.urls)),
    path('api/v1/article-likes/', include(article_like.urls)),
    path('api/v1/article-comment-likes/', include(article_comment_like.urls)),
    path('api/v1/article-cr-likes/', include(a_com_reply.urls)),
    re_path(r'^view/(?P<id>[0-9]+)',views.view_article,name="view-article"),
    path('list/',views.list_article,name="list-article"),
    path('search/',views.search_article,name="search-article"),
    re_path(r'^category/(?P<slug>[\w|\W\-]+)/',views.by_category,name="article-by-category")
]