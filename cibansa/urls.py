"""cibansa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import main.views as mv
from django.conf.urls import include
from filebrowser.sites import site
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    url(r'^accounts/', include("accounts.urls")),
    # url(r'^/api/v1/',include(category,namespace="category-api")),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', admin.site.urls),
    url(r'^category/(?P<slug>[\w|\W\-]+)/list-topic/',mv.list_topic,name="list-topic"),
    url(r'^topic/(?P<slug>[\w|\W\-]+)/questions/',mv.list_topic_question,name="list-topic-questions"),
    url(r'^category/',mv.list_categories,name="list-categories"),
    url(r'^questions/post-new-question/',mv.post_question,name="post-new-question"),
    url(r'^questions/edit/(?P<question>[0-9]+)/',mv.edit_question,name="edit-question"),
    url(r'^questions/tagged/(?P<slug>[\w|\W\-]+)/',mv.question_by_tag,name="question-by-tag"),
    url(r'^questions/(?P<id>[0-9]+)/',mv.view_question,name="view-question"),
    url(r'^questions/search/',mv.question_search,name="question-search"),
    url(r'^$',mv.index,name="home-page"),

    url(r'^main/',include("main.urls")),
    url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^article/',include("articles.urls")),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^djangojs/', include('djangojs.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
