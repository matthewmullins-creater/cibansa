from rest_framework import serializers
from courses.models import CbCourses
from accounts.serializers import CbUserSerializer


class CbCoursesSerializer(serializers.ModelSerializer):
    user = CbUserSerializer()
    user_full_name = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    def get_user_full_name(self,obj):
        return obj.user.get_full_name();

    def get_has_liked(self, obj):
        request = self.context.get("request")
        return True


    class Meta:
        model = CbCourses
        fields = ("category","image","created_at","meta_data","is_visible","content","user","user_full_name","id")