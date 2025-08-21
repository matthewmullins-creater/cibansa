from rest_framework import  viewsets
from articles.serializers import CbArticleSerializer, CbArticleLikesSerializer,CbArticleCommentSerializer,\
    CbArticleCommentReplySerializer, CbArticleCommentReplyLikesSerializer,CbArticleCommentLikesSerializer
from articles.models import CbArticle,CbArticleComment,CbArticleLike,CbArticleCommentLike,CbArticleCommentReply,\
    CbArticleCommentReplyLikes

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response


class CbArticleViewset(viewsets.ModelViewSet):
    queryset = CbArticle.objects.all()
    serializer_class = CbArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False, methods=["post"])
    def post_comment(self,request):
        serializer = CbArticleCommentSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=403)

    @action(detail=False, methods=["post"])
    def post_comment_reply(self,request):
        serializer = CbArticleCommentReplySerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=403)


class CbArticleLikeViewset(viewsets.ModelViewSet):
    queryset = CbArticleLike.objects.all()
    serializer_class = CbArticleLikesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False, methods=["post"])
    def un_like(self,request):
        try:
            c=CbArticleLike.objects.get(article=request.data.get("article"),user=request.user.id)
            c.delete()
            return Response({})
        except:
            return Response({},status=403)


class CbArticleCommentLikeViewset(viewsets.ModelViewSet):
    queryset = CbArticleCommentLike.objects.all()
    serializer_class = CbArticleCommentLikesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False, methods=["post"])
    def un_like(self, request):
        try:
            c = CbArticleCommentLike.objects.get(comment=request.data.get("comment"), user=request.user.id)
            c.delete()
            return Response({})
        except:
            return Response({}, status=403)


class CbArticleCommentReplyLikeViewset(viewsets.ModelViewSet):
    queryset = CbArticleCommentReplyLikes.objects.all()
    serializer_class = CbArticleCommentReplyLikesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False, methods=["post"])
    def un_like(self, request):
        try:
            c = CbArticleCommentReplyLikes.objects.get(comment_reply=request.data.get("comment_reply"), user=request.user.id)
            c.delete()
            return Response({})
        except:
            return Response({}, status=403)