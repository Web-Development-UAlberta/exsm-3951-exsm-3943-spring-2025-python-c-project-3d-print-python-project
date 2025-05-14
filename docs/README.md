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

## Seed the Database:
1. Download [3DBenchy.stl](https://github.com/CreativeTools/3DBenchy)
2. Download [3DBenchy Image](http://www.3dbenchy.com/wp-content/uploads/2018/01/3DBenchy-LowPoly-Wireframe-Dark-Side-view-3DBenchy.com_.png) and rename it `benchy.png`
3. Download [Infinity_cube_2.stl](https://www.thingiverse.com/thing:6589139/files)
4. Download [Infinity Cube Image](https://cdn.thingiverse.com/assets/0a/75/b0/f6/7c/large_display_1b212582-9c97-4080-9d24-5190f5188e01.png) and rename it `infinity_cube.png`
5. Put models in `src/print_shop/store/models`
6. Put thumbnails in `src/print_shop/store/thumbnails`
7. **Flush** your database if you have existing dummy data `python manage.py flush`
8. Run `python manage.py initial_seed`
9. Run `python manage.py order_seed`

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

### Management Commands and Fixtures
- [Django Management Commands](https://docs.djangoproject.com/en/5.2/howto/custom-management-commands/)
- [Django Fixtures](https://docs.djangoproject.com/en/5.2/topics/db/fixtures/#fixtures-explanation)

### Media Files
- [Benchy](https://github.com/CreativeTools/3DBenchy/)
- [Infinity Cube](https://www.thingiverse.com/thing:6589139)
