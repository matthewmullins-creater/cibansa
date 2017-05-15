from rest_framework import serializers
from accounts.models import CbUserProfile, User


class CbUserProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = CbUserProfile
        fields = ("first_name","last_name","phone","dob","country","city","gender","has_photo","avatar")


class CbUserSerializer(serializers.ModelSerializer):
    profile = CbUserProfileSerializer()
    profile_pix = serializers.SerializerMethodField()

    def get_profile_pix(self, obj):
        return obj.get_profile_pix()

    class Meta:
        model = User
        fields = ("profile","username","profile_pix")