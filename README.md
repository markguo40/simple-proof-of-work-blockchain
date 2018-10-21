# simple-proof-of-work-blockchain
Assignment 1 in Blockchain Tutorial: Building a simple proof of work blockchain

Python 3.7

## installation:

Install all the libraries
```
pip install -r requirements.txt 
```

Start Django Migration in blockchain directory
```
./manage.py migrate
```

Creating Genesis Block:
```
./manage.py shell < server/scripts/generate_genesis_block.py
```

Greate a superuser so you can log into the admin:
```
./manage.py createsuperuser
```

Run server
```
./manage.py runserver
```

Go to http://127.0.0.1:8000/admin/ and Using your username and password for superuser to login to the admin page:

Open another terminal tab

Start Mining:
```
./manage.py shell < server/scripts/start_mining.py
```
