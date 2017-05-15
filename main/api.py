from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from main.models import CbCategory,CbTopic,CbQuestion,CbAnswerLike,CbAnswerReplyLike
from main.serializers import CbCategorySerializer,CbTopicSerializer,CbQuestionSerializer,CbAnswersSerializer,\
                                CbAnswerReplySerializer,CbAnswerLikeSerializer,CbAnswerReplyLikeSerializer
from rest_framework.decorators import list_route,detail_route
from rest_framework.response import Response
from main.core.pagination import LinkHeaderPagination


class CbCategoryViewset(viewsets.ModelViewSet):
    queryset = CbCategory.objects.all()
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CbCategorySerializer

    @detail_route(methods=["get"])
    def get_topics(self,request,pk):
        queryset = CbTopic.objects.filter(category=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CbTopicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CbTopicSerializer(queryset, many=True)
        return Response(serializer.data)


        # return Response(serializer.data)


class CbTopicViewset(viewsets.ModelViewSet):
    queryset = CbTopic.objects.all()
    permissions_class = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CbTopicSerializer
    # paginate_by = 2
    # pagination_class = LinkHeaderPagination
    # paginate_by_param = 'page_size'
    # max_paginate_by = 2

    @list_route(methods=["get"])
    def get_category_topics(self, request):
        queryset = CbTopic.objects.filter(category=1)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CbQuestionViewset(viewsets.ModelViewSet):
    queryset = CbQuestion.objects.all()
    serializer_class = CbQuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @list_route(methods=["post"])
    def post_answer(self,request):
        serializer = CbAnswersSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=403)

    @list_route(methods=["post"])
    def post_answer_reply(self,request):
        serializer = CbAnswerReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=403)

    # @detail_route(methods=["post"])
    # def like_answer(self,request,pk=None):
    #     serializer = CbAnswerLikeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors,status=403)


class CbAnswerLikeViewset(viewsets.ModelViewSet):
    queryset = CbAnswerLike.objects.all()
    serializer_class = CbAnswerLikeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @list_route(methods=["post"])
    def un_like(self,request):
        try:
            c=CbAnswerLike.objects.get(answer=request.data.get("answer"),user=request.user.id)
            c.delete()
            return Response({})
        except:
            return Response({},status=403)


class CbAnswerReplyLikeViewset(viewsets.ModelViewSet):
    queryset = CbAnswerReplyLike.objects.all()
    serializer_class = CbAnswerReplyLikeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @list_route(methods=["post"])
    def un_like(self, request):
        try:
            c = CbAnswerReplyLike.objects.get(answer_reply=request.data.get("answer_reply"), user=request.user.id)
            c.delete()
            return Response({})
        except:
            return Response({}, status=403)
    # def list(self,request):
    #
    #     print(request.data)
