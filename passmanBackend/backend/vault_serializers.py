''' This module defines all the serializers. The serializers are required to convert Django models and objects to primitive types and render them as JSON,XML,etc for easy transfer.
3 seralizers:

User Serializer: Handles serialization/Deserialization of the User model for authentication. User is an inbuilt model in django.contrib.auth.models. Very useful for authentication purposes

Vault Serializer: Seriliazation/Deserialization for vault. It takes parameters from request to create a vault or update an existing vault if required.

Vault Record Serializer: Seriliazation/Deserialization for a record in the vault. Creates a new record in the vault if required.
'''


from rest_framework import serializers
from django.contrib.auth.models import User
from vault_backend import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# This code allows automatic creation of an authtoken whenever a user is created. 
# Helpful as we do not need a seperate routine and trigger that when a new user is created for creating an API auth token.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# User serializer only creates new users. A new creation triggers the receiver dispatch above that binds a Token model instance to this user. This token can be used for API authentication

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
    
    # The following code is for updating user or password. This is still under testing. Need to test some corner cases but I suppose it will suffice for now.
    def update(self, instance, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        try:
            if not User.objects.get(username=username):
                print("User %s does not exist. Creating user" %(username))
                self.create(validated_data)
                return 0
            instance.username = username
            instance.set_password(password)
            instance.save()
            print("User %s updated" % (username))
            return instance
        except:
            User.objects.delete(username=username)
            return None
              


# Vault Serializer creates or updates a new vault based on method (POST, UPDATE) executed. You can see vault documentation in vault_backend/models.py module

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

# Each vault record represents a record stored in the vault. This serializer stringifies them. Some methods used here is in the Vault model defined. Please refer that module for more info.

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
