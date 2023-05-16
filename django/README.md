This Django app is the future home of the user-facing Metro2 results app.

How to run this app locally, for now:
1. Prepare a python environment. I used pyenv-virtualenv.
2. From the metro2 project root, pip install 4.2.1
3. `./django/manage.py migrate`
4. `./django/manage.py runserver`
5. `./django/manage.py createsuperuser --username=admin`
6. Visit localhost:8000/admin to log in to the admin site
