from django.db import models
from django.contrib.postgres.fields import JSONField
from main.models import CbCategory,CbTag

# Create your models here.


def upload_article_image(instance,filename):
    return "".join(["%s%s" % ("articles/", "/"), filename])
    # return "".join(["%s%s%s" % ("category/", str(instance.name), "/"), filename])


class CbArticle(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(CbCategory,on_delete=models.SET_NULL,null=True,related_name="category_article")
    content = models.TextField()
    image = models.ImageField(default="article_image.png",upload_to=upload_article_image)
    user = models.ForeignKey("accounts.User",related_name="user_articles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_data = JSONField()
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "cb_article"


class CbArticleTags(models.Model):
    article = models.ForeignKey(CbArticle, on_delete=models.CASCADE,related_name="article_tags")
    tag = models.ForeignKey(CbTag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cb_article_tags"


class CbArticleComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey("accounts.User",related_name="user_article_comments")
    article = models.ForeignKey(CbArticle,related_name="article_comments")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cb_article_comment"


class CbArticleCommentReply(models.Model):
    comment = models.ForeignKey(CbArticleComment,related_name="comment_replies")
    content = models.TextField()
    user = models.ForeignKey("accounts.User", related_name="user_article_cr")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cb_article_comment_reply"


class CbArticleLike(models.Model):
    article = models.ForeignKey(CbArticle, on_delete=models.CASCADE,related_name="article_likes")
    user = models.ForeignKey("accounts.User",related_name="user_article_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cb_article_like"


class CbArticleCommentLike(models.Model):
    comment = models.ForeignKey(CbArticleComment, on_delete=models.CASCADE,related_name="article_comment_likes")
    user = models.ForeignKey("accounts.User",related_name="user_article_comment_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cb_article_comment_like"


class CbArticleCommentReplyLikes(models.Model):
    comment_reply = models.ForeignKey(CbArticleCommentReply, on_delete=models.CASCADE,related_name="article_cr_likes")
    user = models.ForeignKey("accounts.User", related_name="user_article_cr_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cb_article_comment_reply_like"
