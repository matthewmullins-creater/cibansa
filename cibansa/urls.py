"""cibansa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import path, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.contrib import admin
import main.views as mv
from filebrowser.sites import site
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500



urlpatterns = [

    path('accounts/', include("accounts.urls")),
    # path('/api/v1/',include(category,namespace="category-api")),
    # path('admin/filebrowser/', include(site.urls)),  # Temporarily commented out for Django 5 compatibility
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    re_path(r'^category/(?P<slug>[\w|\W\-]+)/list-topic/',mv.list_topic,name="list-topic"),
    re_path(r'^topic/(?P<slug>[\w|\W\-]+)/questions/',mv.list_topic_question,name="list-topic-questions"),
    path('topic/search',mv.topic_search,name="topic-search"),
    path('category/',mv.list_categories,name="list-categories"),
    path('search/category/',mv.category_search,name="category-search"),
    path('questions/post-new-question/',mv.post_question,name="post-new-question"),
    re_path(r'^questions/edit/(?P<question>[0-9]+)/',mv.edit_question,name="edit-question"),
    re_path(r'^questions/tagged/(?P<slug>[\w|\W\-]+)/',mv.question_by_tag,name="question-by-tag"),
    re_path(r'^questions/(?P<id>[0-9]+)/',mv.view_question,name="view-question"),
    path('questions/search/',mv.question_search,name="question-search"),
    path('',mv.index,name="home-page"),

    path('main/',include("main.urls")),
    path('selectable/', include('selectable.urls')),
    path('blog/',include("articles.urls")),
    path('courses/',include("courses.urls")),
    path('tinymce/', include('tinymce.urls')),
    # path('djangojs/', include('djangojs.urls')),  # Commented out - may not be needed for Django 5
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler400 = 'main.views.bad_request'
handler403 = 'main.views.permission_denied'
handler404 = 'main.views.page_not_found'
handler500 = 'main.views.server_error'
