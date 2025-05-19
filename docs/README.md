
# 🖨️ Python Project - 3D Print Store

## ⚙️ Backend Development Setup

1. 🛠️  It is recommended to first create a virtual environment to contain python dependencies:
         `python -m venv .venv`
   

2. 🔌 Activate the virtual environment:  
       `source .venv/bin/activate`

3. 📦 Install requirements into root of the repo:
      `pip install -r requirements.txt`

4. 🗄️ Create a MySQL or MariaDB database named `print_shop`.

5. 📁 Create a copy of the `.env.example` file with the name `.env`


6. 🔐 Update the `DATABASE_URL` variable with your username and password for MySQL/ MariaDB

7. 📂 Navigate into the Django project root:  
      `cd src/print_shop`

8. 🌈 Install Tailwind CSS dependencies:  
       `python manage.py tailwind install`

9.  🧱 Run migrations:
         `python manage.py migrate`

## 🚀 Start the Project

1. ▶️ Run the Django development server:  
      `python manage.py runserver`

2. 🎨 Start Tailwind in watch mode:  
      `python manage.py tailwind start`

## 🧪 Frontend Testing

1. 🐧 Frontend testing requires Selenium. On Linux, you will need to install the following dependencies:
      `sudo apt-get install -y libasound2-dev`

2. 🧰 Install required Python packages (again, if needed for testing):  
      `pip install -r requirements.txt`

## 🌱 Seed the Database

1. 📥 Download [3DBenchy.stl](https://github.com/CreativeTools/3DBenchy)

2. 🖼️ Download and rename the image to `benchy.png`:  
   [3DBenchy Image](http://www.3dbenchy.com/wp-content/uploads/2018/01/3DBenchy-LowPoly-Wireframe-Dark-Side-view-3DBenchy.com_.png)

3. 📥 Download [Infinity_cube_2.stl](https://www.thingiverse.com/thing:6589139/files)

4. 🖼️ Download and rename the image to `infinity_cube.png`:  
   [Infinity Cube Image](https://cdn.thingiverse.com/assets/0a/75/b0/f6/7c/large_display_1b212582-9c97-4080-9d24-5190f5188e01.png)

5. 📂 Put models in `src/print_shop/media/models`

6. 📂  Put thumbnails in `src/print_shop/media/thumbnails`

7. 🧹 **Flush** your database if you have existing dummy data `python manage.py flush`

8. 🌱 Seed initial 3D models:  
      `python manage.py initial_seed`

9. 🧾 Seed order data:  
      `python manage.py order_seed`

## 🙌 Credits & Resources

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
- [Create/Update with kwargs](https://stackoverflow.com/questions/21119494/django-modelforms-init-kwargs-create-and-update)

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
