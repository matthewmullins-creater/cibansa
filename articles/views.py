from django.shortcuts import render
from articles.models import CbArticle
from django.shortcuts import get_object_or_404,redirect,redirect
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.conf import settings
# Create your views here.


def view_article(request,id):
    article = get_object_or_404(CbArticle,pk=id)
    similar_articles = CbArticle.objects.filter(~Q(id=id),category=article.category).order_by("-created_at")[:3]
    context = {
        "article": article,
        "more_article":similar_articles
    }
    return render(request,"article/view.html",context)


def list_article(request):
    articles = CbArticle.objects.filter(is_visible=True).order_by("-created_at")
    page = request.GET.get("page", 1)
    paginator = Paginator(articles, settings.REST_FRAMEWORK.get("PAGE_SIZE"))

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {
        "articles": articles
    }
    return render(request,"article/list.html",context)


def search_article(request):
    result = CbArticle.objects.filter(title__icontain=request.GET.get("q"))
    context = {
        "result": result
    }
    return render(request,"article/list.html",result)
