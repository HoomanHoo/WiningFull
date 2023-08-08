from rest_framework import serializers

from user.models import WinUserAccount


class AccountPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinUserAccount
        fields = ["user_account_default", "user_account_id"]

    def create(self, validated_data):
        return WinUserAccount.objects.create(validated_data)

    def update(self, instance, validated_data):
        # instance.user_account_id = validated_data.get("user_account_id", instance.user_account_id)
        instance.user_account_default = validated_data.get(
            "user_account_default", instance.user_account_default
        )
        instance.save()
        return super().update(instance, validated_data)


class AccountSerializer(serializers.Serializer):
    user_account1 = serializers.CharField()
    user_account2 = serializers.CharField()
    user_account3 = serializers.CharField()


class WinUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinUserAccount
        fields = "__all__"


class SelectAccountSerializer(serializers.Serializer):
    user_account = serializers.CharField()
    user_account_id = serializers.CharField()
