===============
PassMan-Backend
===============

PassMan-backend is a backend REST API written in Django REST Framework as an implementation for a password manager. Each password record is stored in a vault which is tied to a single user instance.
The vault file is stored in local system and is not sent to any third party. For this reason, it is very important to remember the master password which unlocks the vault. Fortunately, this has been
combined with the sign in process so as soon as you sign in, you will have access to all your stored passwords. 

Detailed Documentation in the "docs" directory

Quick Start
------------
1. Add PassMan-backend to your installed apps setting in your application's settings.py file
    INSTALLED_APPS = [
        ....,
        'backend',
        ....,
    ]

2. Include the backend in the URLConf like this
    path('passman/',include(backend.urls)

3. Run `python manage.py migrate` to construct the database tables
4. Start the development server
    `python manage.py runserver`

5. Navigate to "http://127.0.0.1:8000/backend/<endpoint>" to invoke functionality provided by each endpoint ("users/","vaults/", "records/")



