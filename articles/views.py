from django.shortcuts import render
from articles.models import CbArticle
from django.shortcuts import get_object_or_404,redirect,redirect
from django.db.models import Q
# Create your views here.


def view_article(request,id):
    article = get_object_or_404(CbArticle,pk=id)
    similar_articles = CbArticle.objects.filter(~Q(id=id),category=article.category).order_by("-created_at")[:3]
    context = {
        "article": article,
        "more_article":similar_articles
    }
    return render(request,"article/view.html",context)