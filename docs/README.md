# Python Project - 3D Print Store

## Backend Development Setup
It is recommended to first create a virtual envinroment to contain python dependencies:
`python -m venv .venv`

And activate it:
`source .venv/bin/activate`

Install requirements into root of the repo:
`pip install requiremnets.txt`

Spin up a database in MySQL or MariaDB named `print_shop`

Create a copy of the `.env.example` file with the name `.env`
- Update the `DATABASE_URL` variable with your username and password for MySQL/ MariaDB

## Credits
[Environment Variables](https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f)