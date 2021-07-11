PassMan - The password manager for the paranoid. 
This repository represents the backend logic of the password manager. The logic is defined as a REST API using Django and Django REST Framework.
The API is used by accessing several endpoints and invoking the functionality abstracted from that endpoint.

Please note that this is under testing and has not finished development. The code must be cleaned and neatly documented.

Also, this is intended to be run in a localhost environment or a limited client environment. The fact being that the password vaults are created in your system and only you have access to it.
This part of behavior can be changed of course if you would like.

If you would only like to test this and not do any development, You can use the docker container instead of manually building the repo.
You can find my docker container [here](https://hub.docker.com/repository/docker/sharanvarma0/passman-backend).

The PassMan password manager backend is intended to be consumed by a frontend framework implementation written in any language. The backend has the following features:
    
    1. Create/Manage Users: The users have their username and password which are used as master credentials to access password vaults.
    2. Create/Manage vaults for passwords: The vault is just a simple text file as a container of encrypted passwords. Each user has one or more vaults which store encrypted passwords. 
    3. Create/Manage records: A record is an entry in the vault like a website mapped to its set password. These records are put inside vaults and encrypted.
    4. Create/Manage API Tokens: As a backend service, the token service has been implemented. By reaching out to a certain endpoint, get the API token. This API token must be included in subsequent requests.

Programming Language: Python 3.9
Frameworks: Django, Django REST Framework
Intended users: Developers, users.

Reason for the API based architecture
-------------------------------------
One question I would have if I was going through this is why would someone need an API based architecture for this. I have pointed out my reasons below.
    
    - As you may be aware, I am still a newbie in backend design and development. I am a junior programmer and I wanted to experiment with APIs and how my own API could be made.
    - An API is a very good emphasis on the DRY principle, I would only need to write or change the API defination in one place. The multiple frontends that are using this API will all reflect this change.
    - The API is very portable and such architecture often produces code that is easy to maintain and manage. 
    - All the scaling and loadbalancing logic need to be defined only once at the API side. Furthermore, no changes would be needed on the frontend.
    - A user can decide if the provided frontend is not upto their mark or standard and if necessary, create their own frontend which interfaces with this API. They would only need knowledge of the working.

FAQs
----
1. Will you continue to develop this project?
A. Yes, I shall continue to develop this project. From my personal opinion, the actual working logic is working of now. There are only some other functions which are needed to be added. I shall keep the
github repo updated as I make any changes to the code or doc.

2. Is this code free to use?
A. Yes, This code is fully free to use. I have licensed it under the BSD 3 clause license. While not actually necessary, I would be glad if you had a different approach for anything and would inform me of it.
I will try to either merge it or integrate it into this project.

3. Is this project on par with enterprise password managers?
A. ABSOLUTELY NOT! This by no means is a full password manager as of now. Perhaps it could be once the trivial but important functionality has been added. Please do note that I am just one guy who came up
with this idea. There are full multi person teams in big companies/enterprises/corporations working on the problem of password managing day in and day out. This project would never hold a candle to those
projects. That being said, I assume this project does present a good entrypoint into learning how a simple password manager could be created.
