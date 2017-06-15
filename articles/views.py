from django.shortcuts import render
from articles.models import CbArticle
from django.shortcuts import get_object_or_404,redirect,redirect
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.conf import settings
from main.models import CbCategory
# Create your views here.


def view_article(request,id):
    article = get_object_or_404(CbArticle,pk=id)
    similar_articles = CbArticle.objects.filter(~Q(id=id),category=article.category,is_visible=True).order_by("-created_at")[:3]
    context = {
        "article": article,
        "more_article":similar_articles
    }
    return render(request,"article/view.html",context)


def by_category(request,slug):
    c = get_object_or_404(CbCategory,slug=slug)
    articles = CbArticle.objects.filter(is_visible=True,category=c.id)
    page = request.GET.get("page", 1)
    paginator = Paginator(articles, settings.REST_FRAMEWORK.get("PAGE_SIZE"))
    category = CbCategory.objects.filter(is_visible=True)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {
        "articles": articles,
        "category": category,
        "slug":slug,
    }
    return render(request, "article/list.html", context)


def list_article(request):
    articles = CbArticle.objects.filter(is_visible=True).order_by("-created_at")
    page = request.GET.get("page", 1)
    paginator = Paginator(articles, settings.REST_FRAMEWORK.get("PAGE_SIZE"))
    category = CbCategory.objects.filter(is_visible=True)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {
        "articles": articles,
        "category": category,
    }
    return render(request,"article/list.html",context)


def search_article(request):
    articles = CbArticle.objects.filter(title__icontains=request.GET.get("q"))
    page = request.GET.get("page", 1)
    paginator = Paginator(articles, settings.REST_FRAMEWORK.get("PAGE_SIZE"))
    category = CbCategory.objects.filter(is_visible = True)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {
        "articles": articles,
        "category": category,
    }
    return render(request, "article/list.html", context)
