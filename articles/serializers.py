from rest_framework import serializers
from articles.models import CbArticle,CbArticleComment,CbArticleCommentLike,CbArticleCommentReply,\
                        CbArticleCommentReplyLikes,CbArticleLike
from accounts.serializers import CbUserSerializer


class CbArticleCommentReplySerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()
    comment_reply_likes = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    def get_user_data(self,obj):
        user = CbUserSerializer(obj.user).data
        return user

    def get_has_liked(self,obj):
        request = self.context.get("request")
        if CbArticleCommentReplyLikes.objects.filter(comment_reply=obj.id,user=request.user.id).exists():
            return True
        else:
            return False

    def get_comment_reply_likes(self,obj):
        return obj.article_cr_likes.count()

    class Meta:
        model = CbArticleCommentReply
        fields = "__all__"


class CbArticleCommentReplyLikesSerializer(serializers.ModelSerializer):

     class Meta:
        model = CbArticleCommentReplyLikes
        fields = "__all__"


class CbArticleCommentLikesSerializer(serializers.ModelSerializer):

     class Meta:
        model = CbArticleCommentLike
        fields = "__all__"


class CbArticleCommentSerializer(serializers.ModelSerializer):
    comment_replies = CbArticleCommentReplySerializer(many=True, required=False)
    comment_likes = serializers.SerializerMethodField()
    user_data = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    def get_user_data(self, obj):
        user = CbUserSerializer(obj.user).data
        return user

    def get_has_liked(self, obj):
        request = self.context.get("request")
        if CbArticleCommentLike.objects.filter(comment=obj.id, user=request.user.id).exists():
            return True
        else:
            return False

    def get_comment_likes(self, obj):
        return obj.article_comment_likes.count()

    class Meta:
        model = CbArticleComment
        fields = (
        "user", "id", "article", "comment", "created_at", "comment_replies", "comment_likes", "user_data", "has_liked")


class CbArticleLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CbArticleLike
        fields = "__all__"


class CbArticleSerializer(serializers.ModelSerializer):
    user = CbUserSerializer()
    user_full_name = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    article_likes = serializers.SerializerMethodField()
    article_comments = CbArticleCommentSerializer(many=True)

    def get_user_full_name(self,obj):
        return obj.user.get_full_name();

    def get_has_liked(self, obj):
        request = self.context.get("request")
        if CbArticleLike.objects.filter(article=obj.id, user=request.user.id).exists():
            return True
        else:
            return False

    def get_article_likes(self, obj):
        return obj.article_likes.count()

    class Meta:
        model = CbArticle
        fields = ("category","image","created_at","meta_data","is_visible","content","user","user_full_name",
                  "has_liked","article_likes","id","article_comments")