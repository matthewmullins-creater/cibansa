from rest_framework import serializers
from main.models import CbCategory,CbQuestion,CbTopic,CbAnswer,CbAnswerReply,CbAnswerLike,CbAnswerReplyLike
from accounts.serializers import CbUserSerializer


class CbCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CbCategory
        fields = ("name","image","description","created_at","slug","meta_data")


class CbTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = CbTopic
        fields = ("category","title","image","description","created_at","owner","slug","meta_data")


class CbAnswerReplyLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CbAnswerReplyLike
        fields = ("answer_reply","user","created_at")


class CbAnswerReplySerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()
    answer_reply_likes = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    def get_user_data(self,obj):
        user = CbUserSerializer(obj.user).data
        return user

    def get_has_liked(self,obj):
        request = self.context.get("request")
        if CbAnswerReplyLike.objects.filter(answer_reply=obj.id,user=request.user.id).exists():
            return True
        else:
            return False

    def get_answer_reply_likes(self,obj):
        return obj.answer_reply_likes.count()

    class Meta:
        model=CbAnswerReply
        fields = ("id","answer","user","comment","created_at","answer_reply_likes","user_data","has_liked")


class CbAnswerLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CbAnswerLike
        fields = ("answer","user","created_at")


class CbAnswersSerializer(serializers.ModelSerializer):
    answer_replies = CbAnswerReplySerializer(many=True,required=False)
    answer_likes = serializers.SerializerMethodField()
    user_data = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    def get_user_data(self,obj):
        user = CbUserSerializer(obj.user).data
        return user

    def get_has_liked(self,obj):
        request = self.context.get("request")
        if CbAnswerLike.objects.filter(answer=obj.id,user=request.user.id).exists():
            return True
        else:
            return False

    def get_answer_likes(self,obj):
        return obj.answer_likes.count()

    class Meta:
        model = CbAnswer
        fields = ("user","id","question","comment","created_at","answer_replies","answer_likes","user_data","has_liked")


class CbQuestionSerializer(serializers.ModelSerializer):
    owner = CbUserSerializer()
    question_answers = CbAnswersSerializer(many=True)
    user_full_name = serializers.SerializerMethodField()

    def get_user_full_name(self,obj):
        return obj.owner.get_full_name();

    class Meta:
        model = CbQuestion
        fields = ("topic","title","description","owner","created_at","status","slug","question_answers","user_full_name")
