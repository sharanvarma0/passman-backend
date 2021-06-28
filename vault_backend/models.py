from django.db import models
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from vault_backend.extra_functions import *
import os
import io

class Vault(models.Model):
    number = models.IntegerField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    vault_name = models.CharField(max_length=200, unique=True)
    directory = models.CharField(max_length=200, default='/home/sharan/.vaults')
    filename = models.CharField(max_length=200, default="vault")


    def create_vault(self):
        default_directory = self.directory
        default_filename = self.filename 
        if not os.path.exists(default_directory):
            os.mkdir(default_directory)
        file = open(default_directory + '/' + default_filename, 'w').close()

    def check_data(self, term, data):
        if term in data:
            return True
        return False

    def add_data(self, sitename, password):
        try:
            user = self.username
            key = generate_key(user)

            default_directory = self.directory 
            default_filename = self.filename  
            arr_of_passwords = self.get_data()
            print(arr_of_passwords)
            if arr_of_passwords == '':
                arr_of_passwords = []

            write_descriptor = open(default_directory + '/' + default_filename, 'w')
            write_data = {'site_name': sitename, 'password': password}
            if self.check_data(write_data, arr_of_passwords):
                return 2
            arr_of_passwords.append(write_data)
            write_data = JSONRenderer().render(arr_of_passwords)
            encrypted_data = encrypt_data(key, write_data)
            write_descriptor.write(encrypted_data)
            write_descriptor.close()
            return 0
        except:
            if (write_descriptor):
                write_descriptor.close()
            return 1

    def get_data(self):
        try:
            user = self.username
            key = generate_key(user)
            default_directory = self.directory 
            default_filename = self.filename 
            read_descriptor = open(default_directory + '/' + default_filename, 'r')
            data = read_descriptor.read()
            if data == '':
               read_descriptor.close()
               return data
            read_data = io.BytesIO(decrypt_data(key, data))
            json_read_data = JSONParser().parse(read_data)
            read_descriptor.close()
            return json_read_data
        except:
            read_descriptor.close()
            return 1
 
# Not tested delete functionality yet. Might implement in future.

'''    def delete_data(self, sitename, password):
        try:
            delete_data = {'site_name':sitename, 'password':password}
            data = self.get_data()
            if self.check_data(delete_data, data):
                data.remove(delete_data)
            if data:
                for dictionary_data in data:
                    self.add_data(dictionary_data['site_name'], dictionary_data['password'])
                return 0
            else:
                self.create_vault()
                return 0
        except ValueError:
            return 'No Such Value'

'''
            

        
