from backend import vault_serializers
from vault_backend.models import Vault
from django.contrib.auth.models import User, AnonymousUser
from rest_framework import viewsets
from rest_framework.response import Response
import os

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        if not request.successful_authenticator or request.user is AnonymousUser:
            return Response({
                'user': request.user.get_username(),
                'Result': 'Failed',
                'Message': 'Please register a new user. Anon not allowed',
            })
        user = User.objects.get(username=request.user.get_username());
        return Response({
            'user': user.username,
            'Result': 'Success',
            'Message': 'None',
        })

    def create(self, request):
        user_serializer = vault_serializers.UserSerializer(data=request.data)
        try:
            if (user_serializer.is_valid()):
                print(user_serializer.validated_data)
                user_object = user_serializer.save()
                if (user_object == 2):
                    return Response ({
                        'username': user_serializer.validated_data.get('username'),
                        'Result': 'Failed',
                        'Message': 'Already Exists'
                    })

                return Response({
                    'username': user_serializer.validated_data.get('username'),
                    'Result': 'Success (Created)',
                    'Code': '0'
                })
            else:
                return Response({
                    'Result': 'Failed (Not Created)',
                    'Errors': user_serializer.errors,
                })
        except:
            User.objects.get(username=user_serializer.validated_data.get('username')).delete()
            return Response({
               'Result': 'Failed',
               'Message': 'Some Error occurred',
            }) 

class VaultViewSet(viewsets.ViewSet):
    
    def list(self, request):
        if request.successful_authenticator is None or request.user is AnonymousUser:
            return Response({
                'username': 'Anonymous',
                'Result': 'Failed',
                'Message': 'NotAuthenticated'
            })
        username = request.user
        user_object = User.objects.get(username=username)
        queryset = user_object.vault_set.all()
        serializer_class = vault_serializers.VaultSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        if request.successful_authenticator is None or request.user is AnonymousUser:
            return Response({
                'username': request.user,
                'Result': 'Failed',
                'Message': 'NotAuthenticated',
            })
        vault_obj = Vault.objects.get(pk=pk)
        serializer_class = vault_serializers.VaultSerializer(vault_obj)
        return Response(serializer_class.data)

    def create(self, request):
        if request.user:
            request.data['username'] = request.user.get_username()
            print(request.data)
            vault_data = vault_serializers.VaultSerializer(data=request.data)
            try:
                if (vault_data.is_valid()):
                    vault_data.save()
                    return Response({
                      'vault_name': vault_data.validated_data.get('vault_name'),
                      'Result': 'Success',
                      'Messaage': 'None'
                    })
            except: 
                request.user.vault_set.get(vault_name=request.data.get('vault_name')).delete()
                path = vault_data.validated_data.get('directory') + '/' + vault_data.validated_data.get('filename')
                if os.path.exists(path):
                    os.remove(path)
                return Response({
                  'vault_name': request.data['vault_name'],
                  'Result': 'Failed',
                  'Message': 'Some Error occurred. Please check the data passed'
                })
        else:
            return Response({
                'username': request.user.get_username(),
                'Result': 'Failed',
                'Message': "NotAuthenticated",
            })

    def partial_update(self, request, pk=None):
        if request.successful_authenticator is None or request.user is AnonymousUser:
            return Response({
                'username': request.user.get_username(),
                'Result': 'Failed',
                'Message': 'NotAuthenticated',
            })
        vault_obj = Vault.objects.get(pk=pk)
        name = request.data.get('vault_name')
        if not name:
            return Response({
              'Result': 'Failed',
              'Message': 'Only vault_name attribute can be updated'
            })
        vault_obj.vault_name = name
        vault_obj.save()
        return Response ({
          'Result':'Success'
        })

class VaultRecordViewSet(viewsets.ViewSet):
    def list(self, request):
        if not request.successful_authenticator or request.user is AnonymousUser:
            return Response({
                'username': request.user.get_username(),
                'Result': 'Failed',
                'Message': 'NotAuthenticated',
            })
        vaults = User.objects.get(username=request.user.get_username()).vault_set.all()
        return Response([{
            'vault_name': vault.vault_name,
            'number': str(vault.number)
        } for vault in vaults])

    def create(self, request):
        if not request.successful_authenticator or request.user is AnonymousUser:
            return Response({
                'username': request.user.get_username,
                'Result': 'Failed',
                'Message': 'NotAuthenticated',
            })
        sitename = request.data.get('sitename')
        password = request.data.get('password')
        vault = User.objects.get(username=request.user.get_username()).vault_set.get(vault_name=request.data.get('vault_name'))

        try:
            print(vault)
            vault.add_data(sitename, password)
            return Response({
                'vault_name': request.data.get('vault_name'),
                'sitename': sitename,
                'Result': 'Success',
                'Message': 'None',
            })
        except:
            return Response({
                'vault_name': request.data.get('vault_name'),
                'sitename': sitename,
                'Result': 'Failed',
                'Message': 'Error occurred',
            })
    
    def retrieve(self, request, pk=None):
        if not request.successful_authenticator or request.user is AnonymousUser:
            return Response({
                'username': request.user.get_username(),
                'Result': 'Failed',
                'Message': 'NotAuthenticated',
            })
        vault = User.objects.get(username=request.user.get_username()).vault_set.get(number=pk)
        data = vault.get_data() or None
        return Response({
            'vault_name': vault.vault_name,
            'passwords': data,
            'Result': 'Success',
            'Message': 'None',
        })
        

        

        


    
