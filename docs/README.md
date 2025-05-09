# Python Project - 3D Print Store

## Backend Development Install

1. It is recommended to first create a virtual environment to contain python dependencies:
`python -m venv .venv`

2. And activate it:
`source .venv/bin/activate`

3. Install requirements into root of the repo:
`pip install -r requirements.txt`

4. Spin up a database in MySQL or MariaDB named `print_shop`

5. Create a copy of the `.env.example` file with the name `.env`

6. Update the `DATABASE_URL` variable with your username and password for MySQL/ MariaDB

7. Change directory into project root:
`cd src/print_shop` 

8. Install tailwind dependencies:
`python manage.py tailwind install`

9. Run migrations:
`python manage.py migrate`

## Start up the project

1. Run server:

`python manage.py runserver`

2. Run tailwind:
`python manage.py tailwind start`


## Front End Testing

1. Frontend testing requires Selenium. On Linux, you will need to install the following dependencies:
`sudo apt-get install -y libasound2-dev`

2. Then install requirements.txt:
`pip install -r requirements.txt`


## Credits

### Environment Variables
- [Environment Variables](https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f)

### Extend User Model OneToOneField
- [Extend User Model OneToOneField](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#extending-the-existing-user-model)
- [Example of Extending User Model](https://www.crunchydata.com/blog/extending-djangos-user-model-with-onetoonefield)

### Tailwind in Django
- [Tailwind in Django](https://django-tailwind.readthedocs.io/en/latest/installation.html)

### Admin Custom Display
- [Admin Custom Display](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#customizing-the-admin-interface)
- [Display Fields](https://www.w3schools.com/django/django_admin_set_list_display.php)

### Model Manager
- [Django Docs on Model Manager](https://docs.djangoproject.com/en/5.2/topics/db/managers/)

### Forms Logic Resources
- [Django ModelForms Create and Update with kwargs](https://stackoverflow.com/questions/21119494/django-modelforms-init-kwargs-create-and-update)

