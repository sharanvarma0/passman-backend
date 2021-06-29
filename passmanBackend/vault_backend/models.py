''' 
Mostly these are internal imports related to django and rest_framework.
The os and io imports are for creating files, paths and parsing bytes objects respectively 
'''

from django.db import models
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from vault_backend.extra_functions import *
import os
import io


''' 
The Vault model represents the basic password vault in passman. This model will store the directory path, filename and vault_name specified. This is linked to the User model for only displaying vaults belonging
to the authenticated user. The Vault model is later referenced in different places for creating and updating records stored in it. 
'''

class Vault(models.Model):
    number = models.IntegerField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    vault_name = models.CharField(max_length=200, unique=True)
    directory = models.CharField(max_length=200, default='/home/sharan/.vaults')
    filename = models.CharField(max_length=200, default="vault")

    # Create a new vault as a file in specified directory for future use and store of encrypted passwords.
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

    # adding passwords to the vault file after encrypting them
    def add_data(self, sitename, password):
        try:
            user = self.username
            key = generate_key(user)

            default_directory = self.directory 
            default_filename = self.filename  
            arr_of_passwords = self.get_data()
            print(arr_of_passwords)
            if arr_of_passwords == '':
                arr_of_passwords = []                # passwords stored as a JSON array for easy future retrieval and storage

            write_descriptor = open(default_directory + '/' + default_filename, 'w')
            write_data = {'site_name': sitename, 'password': password}
            if self.check_data(write_data, arr_of_passwords):
                return 2
            arr_of_passwords.append(write_data)
            write_data = JSONRenderer().render(arr_of_passwords)
            encrypted_data = encrypt_data(key, write_data)      # this encrypt_data function is defined in extra_functions module. It takes some data and encrypts it using cryptography.fernet (refer cryptography.fernet module).
            write_descriptor.write(encrypted_data)
            write_descriptor.close()
            return 0
        except:
            if (write_descriptor):
                write_descriptor.close()
            return 1

    # read data from the vault file and decrypt them before dispatch
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
            read_data = io.BytesIO(decrypt_data(key, data))   # the decrypt_data function is defined in extra_functions module. It decrypts data given by generating a fernet key from PBKDF2 using user creds.
            json_read_data = JSONParser().parse(read_data)
            read_descriptor.close()
            return json_read_data
        except:
            read_descriptor.close()
            return 1
 
# Delete Record functionality in vault.Not tested delete functionality yet. Might implement in future.

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
            

        
