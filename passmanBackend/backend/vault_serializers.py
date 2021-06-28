from rest_framework import serializers
from django.contrib.auth.models import User
from vault_backend import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=500)

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        try:
            if len(User.objects.filter(username=username)):
                return 2
            user_obj = User(username=username)
            user_obj.set_password(password)
            if not user_obj.check_password(password):
                return 1
            user_obj.save()
            return user_obj
        except:
            User.objects.get(username=username).delete()
            return 1 


class VaultSerializer(serializers.Serializer):
    number = serializers.IntegerField(required=False)
    username = serializers.CharField(max_length=200)
    vault_name = serializers.CharField(max_length=200)
    directory = serializers.CharField(required=False)
    filename = serializers.CharField(required=False)

    def create(self, validated_data):
        username = User.objects.get(username=validated_data.get('username'))
        number = validated_data.get('number') or None
        vault_name = validated_data.get('vault_name')
        directory = validated_data.get('directory')
        filename = validated_data.get('filename') 
        vault_instance = models.Vault.objects.create(number=number, username=username, vault_name=vault_name, directory=directory, filename=filename)
        vault_instance.create_vault()
        return vault_instance
        

    def update(self, instance, validated_data):
        instance.vault_name = validated_data.get('vault_name')
        instance.save()
        return instance

class VaultRecordSerializer(serializers.Serializer):
    vault_name = serializers.CharField(max_length=200)
    site_name = serializers.CharField(max_length=200)
    generated_password = serializers.CharField(max_length=200)

    def create(self, validated_data):
        vault_name = validated_data.get('vault_name')
        vault = models.Vault.objects.get(vault_name=vault_name)
        site_name = validated_data.get('site_name')
        password = validated_data.get('generated_password')
        return vault.add_data(site_name=site_name, password=password)

    def update(self, instance, validated_data):
        instance.vault_name = validated_data.get('vault-name')
        instance.site_name = validated_data.get('site-name')
        instance.password = validated_data.get('generated-password')
        instance.save()
        return instance
