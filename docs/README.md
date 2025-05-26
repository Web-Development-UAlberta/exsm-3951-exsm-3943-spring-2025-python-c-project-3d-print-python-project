# 🖨️ Python Project - 3D Print Store

A full-featured Django application built to power a customizable 3D printing storefront.
This platform enables seamless product management, dynamic order processing, and real-time customization for both customers and administrators. With a modern and responsive frontend styled using Tailwind CSS, and a robust backend architecture, this application delivers a smooth and intuitive user experience.

## ✨ Features

### 👤 Customer Features

- **Select 3D Models:** Create a customized 3D Model or choose from our extensive pre-made gallery.

- **Color & Material Options:** Customize your selection by picking colors and materials.

- **Instant Quote:** Receive an instant price quote calculated using a fixed formula based on selections.

- **User Registration & Login:** Securely register and log in to your account.

- **Order History & Status:** View your past orders with real-time status updates such as Ordered → Printing → Shipped.

### 🛠️ Admin & Backend Features

- **Filament Stock Tracking:** Monitor filament stock levels by color and material type.

- **Low-Stock Warnings:** Receive alerts when filament stock is low (restocking is manual).

- **User Dashboard:** Manage and review all user orders efficiently.

- **Fulfillment Updates:** Update order fulfillment statuses, including marking orders as "Shipped."

- **Quote Generation:** Generate quotes based on the selected 3D model and material.

- **Pseudo-Checkout:** Simulate checkout confirmation without real payment processing.

## 🖥️ Technologies Used

| Technology                                                                                       | Purpose                     |
| ------------------------------------------------------------------------------------------------ | --------------------------- |
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)               | Backend language            |
| ![Django](https://img.shields.io/badge/-Django-092E20?logo=django&logoColor=white)               | Web framework               |
| ![MySQL](https://img.shields.io/badge/-MySQL-4479A1?logo=mysql&logoColor=white)                  | Database management         |
| ![Tailwind](https://img.shields.io/badge/-Tailwind_CSS-06B6D4?logo=tailwind-css&logoColor=white) | Styling & responsive design |
| ![Selenium](https://img.shields.io/badge/-Selenium-43B02A?logo=selenium&logoColor=white)         | Frontend testing            |
| ![GitHub](https://img.shields.io/badge/-GitHub-181717?logo=github&logoColor=white)               | Version control             |

## ⚙️ Project Usage

### 1. Clone or Pull the Repository

To get a local copy of the project, run:

```bash
git clone https://github.com/Web-Development-UAlberta/exsm-3951-exsm-3943-spring-2025-python-c-project-3d-print-python-project.git

cd "exsm-3951-exsm-3943-spring-2025-python-c-project-3d-print-python-project"
```

If you already have the repo and want to update it, use:

```bash
git pull origin main
```

### 2. Create & Activate Virtual Environment (Optional)

```bash
python -m venv .venv
```

#### ▶️ Activate the Environment

**Windows (Git Bash):**

```bash
source .venv/Scripts/activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Navigate to the project root and run:

```bash
pip install -r requirements.txt
```

### 4. Create Database

Setup a local MySQL or MariaDB database named `print_shop`.

### 5. Configure Environment Variables

Copy the `.env.example` file into `.env` and update the `DATABASE_URL` variable with your recently created database credentials.

```bash
DATABASE_URL=mysql://myuser:mypassword@localhost:3306/print_shop
```

### 6. Navigate to the Django Project Root

```bash
cd src/print_shop
```

### 7. Install Tailwind CSS Dependencies

```bash
python manage.py tailwind install
```

## 🌱 Seed the Database

<!-- Add Seed data instructions here -->

## 🧪 Testing

To run the test suite and ensure everything is working correctly, navigate to the Django project root:

```bash
cd src/print_shop
```

Then run:

```bash
python manage.py test
```

This command will automatically discover and execute all unit tests across your Django app.

Make sure your dependencies are installed before running tests.

## ▶️ Running the Application

### 🚀 Start Django Development Server

To launch the server locally, run these commands in your terminal:

```bash
cd src/print_shop
```

```bash
python manage.py runserver
```

Once the server starts, you’ll see a message like this in your terminal:

```bash
Starting development server at http://127.0.0.1:8000/
```

👉 To open the site, press Ctrl + Click on the URL or paste it into your browser.

🛑 To stop the server, use CTRL + BREAK (or CTRL + C on macOS/Linux).

## 🙌 Credits & Resources

Helpful documentation, examples, and third-party resources that made this project possible.

---

### 🔧 Environment Variables

- [How to Set Up Environment Variables in Django](https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f)

### 👤 Extending User Model

- [Django OneToOneField Extension](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#extending-the-existing-user-model)
- [Example of Extending User Model](https://www.crunchydata.com/blog/extending-djangos-user-model-with-onetoonefield)

### 🎨 Tailwind Setup

- [Tailwind in Django Docs](https://django-tailwind.readthedocs.io/en/latest/installation.html)

### 🛠️ Admin Custom Display

- [Django Admin Interface](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#customizing-the-admin-interface)
- [Display Fields Guide](https://www.w3schools.com/django/django_admin_set_list_display.php)

### 🧙 Model Managers

- [Django Custom Managers](https://docs.djangoproject.com/en/5.2/topics/db/managers/)

### 📝 Forms Logic

- [Create/Update with `kwargs`](https://stackoverflow.com/questions/21119494/django-modelforms-init-kwargs-create-and-update)

### ⚙️ Management Commands & Fixtures

- [Django Management Commands](https://docs.djangoproject.com/en/5.2/howto/custom-management-commands/)
- [Django Fixtures](https://docs.djangoproject.com/en/5.2/topics/db/fixtures/#fixtures-explanation)

### 🧾 API & JSON Responses

- [HTTP Method Decorators](https://docs.djangoproject.com/en/5.2/topics/http/decorators/#allowed-http-methods)
- [Create JSON Response](https://www.geeksforgeeks.org/creating-a-json-response-using-django-and-python/)
- [JsonResponse Docs](https://docs.djangoproject.com/en/5.2/ref/request-response/#jsonresponse-objects)

### 📂 Media Files

- [Benchy STL + Info](https://github.com/CreativeTools/3DBenchy/)

- [Infinity Cube STL + Info](https://www.thingiverse.com/thing:6589139)

- [3D Print Site Logo](https://images.unsplash.com/photo-1518732714860-b62714ce0c59?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)

- [3D Print Site Homepage](https://unsplash.com/photos/brown-cardboard-box-with-yellow-light-d2w-_1LJioQ)
