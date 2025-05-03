# Python Project - 3D Print Store

## Backend Development Setup

It is recommended to first create a virtual environment to contain python dependencies:
`python -m venv .venv`

And activate it:
`source .venv/bin/activate`

Install requirements into root of the repo:
`pip install requirements.txt`

Spin up a database in MySQL or MariaDB named `print_shop`

Create a copy of the `.env.example` file with the name `.env`

- Update the `DATABASE_URL` variable with your username and password for MySQL/ MariaDB

Run migrations:
`python manage.py migrate`

## Credits

[Environment Variables](https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f)

[Extend User Model OneToOneField](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#extending-the-existing-user-model)
[Example of Extending User Model](https://www.crunchydata.com/blog/extending-djangos-user-model-with-onetoonefield)
