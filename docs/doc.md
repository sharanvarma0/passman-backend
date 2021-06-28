PassMan - The password manager for the paranoid
===============================================
This repository contains code and routines for the backend of the password manager. The PassMan password manager has been developed in Django and Django REST Framework. It has an API like architecture.
Each API endpoint undertakes an action anywhere from creating a user, creating a password vault or adding records to the vault. Further description follows.

There are 3 endpoints for PassMan. 

1. Users (/users/)
------------------
The users endpoint handles creation and listing of users. These users are represented as django.contrib.auth.User module instances underneath. Several functioning components of PassMan require a user.
As of now, anonymous login is not allowed. Unless a user is created, no other functions would become available. The following methods are supported for the /users/ endpoint.
    
    GET: if authenticated, get the information of the user authenticated. 
    POST: Create a new user. The parameters required are username and password. POSTing these values as JSON data would set off the routine to create the user. Any failure in the process will be visible
          as an API error. If successful, the response message should say 'Success'.

   This authentication is handled by the UserViewSet which uses the UserSerializer to save users into the system.

2. Vaults (/vaults/)
--------------------
A vault is just a file where the encrypted passwords are stored. The file itself is not encrypted but the content is encrypted. The following REST methods are supported.
    
    GET: if authenticated, get a list of vaults created by the user. If none, return the empty message.
    POST: Create a new vault. Specify the three following parameters.
        - vault_name: (The name of the vault to be created)
        - directory: (The directory in the local system where passman should create the encrypted vault file)
        - filename: (The filename to create and use as the vault)
        eg. POST Request {'vault_name':"vault", 'directory':"/home/<user>/.vaults",'filename':"my_vault"} creates a vault "vault" in directory /home/<user>/.vaults/my_vault.

3. Records (/records/)
----------------------
The records endpoint is used to add password records to the vault. These records are later encrypted and stored in the created vault. 
The following methods are supported.
    
    GET (/pk): The primary key of the vault must be supplied in the request. If yes, the passwords stored in the vault are listed to you. Ofcourse, you must be authenticated.
    POST: Create a new record in the selected vault and save it. The request takes the following parameters.
        - vault_name: (The vault in which to save the password)
        - sitename: (The purpose or the website for which the password is being saved)
        - password: (The password to store)

        Please note that as of now, the backend does not have auto password generation as that can be accomplished in the frontend using JS frameworks.
        eg POST Request: {'vault_name':"vault",'sitename':"gmail.com",'password':"<some_password>"} would store the password for gmail in the vault and then encrypt it.

This is as of now, still a work in progress. The code is messy and very ugly. Over time, I plan to clean the code, document it very well and add trivial functionalities to it.
This prototype is however use able for now and does whatever mentioned above with no problems. Further testing is required however.

