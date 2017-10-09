from articles.models import CbArticle


def new_articles():
    articles = CbArticle.objects.filter(is_visible=True).order_by("-created_at")[:4]
    return articles
