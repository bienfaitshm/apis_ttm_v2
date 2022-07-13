from rest_framework import serializers
from .models import Client, Employe, Users, Company

from rest_framework_simplejwt.tokens import AccessToken
from djoser import serializers as DjoserSerializer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = "__all__"


class UserSerializer(DjoserSerializer.UserSerializer):
    info = serializers.SerializerMethodField(method_name="get_profile")

    class Meta(DjoserSerializer.UserSerializer.Meta):
        fields = DjoserSerializer.UserSerializer.Meta.fields + ("info",)

    def get_profile(self, user):
        # user = obj.select_related("employe", "client")
        return self.get_profile_user(user)

    def get_profile_user(self, user: Users):
        if user.type_user == Users.EMPLOYE and hasattr(user, "employe"):
            employe = user.employe
            return {
                "profile": EmployeSerializer(employe).data,
                "company": CompanySerializer(employe.company).data
            }
        if user.type_user == Users.CLIENT and hasattr(user, "client"):
            client = user.client
            return {
                "profile": ClientSerializer(client).data,
                "company": None
            }
