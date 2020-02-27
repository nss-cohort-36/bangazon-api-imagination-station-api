## Steps to get the Bangazon API started:

- Clone the repo and `cd` into it

- Create your OSX virtual environment in Terminal:

  - `python -m venv bangazonenv`
  - `source ./bangazonenv/bin/activate`

- Or create your Windows virtual environment in Command Line:

  - `python -m venv bangazonenv`
  - `source ./bangazonenv/Scripts/activate`

- Install the app's dependencies:

  - `pip install -r requirements.txt`

- Build your database from the existing models:

  - `python manage.py makemigrations bangazonapi`
  - `python manage.py migrate`

- Create a superuser for your local version of the app:

  - `python manage.py createsuperuser`

- Populate your database with initial data from fixtures files: (_NOTE: every time you run this it will remove existing data and repopulate the tables_)

  - `python manage.py loaddata orders`
  - `python manage.py loaddata product`
  - `python manage.py loaddata producttype`

- Fire up your dev server and get to work!

  - `python manage.py runserver`

- This API is dependent on the front-end client. You can find it here:
https://github.com/nss-cohort-36/bangazon-client-imagination-station-react