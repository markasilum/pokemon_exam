
# Django Project Setup

This README provides the steps to set up a Django project with an app called `pokemons`.

## Initial Setup

### 1. Create a Virtual Environment

First, create a virtual environment using the following command:
```bash
uv venv
```

### 2. Initialize the Project

Run the following command to initialize the project:
```bash
uv init
```

### 3. Install Django

Add Django to the virtual environment by running:
```bash
uv add django
```

### 4. Create a Directory for Your App

Create and navigate to the directory for your project:
```bash
mkdir pokedex
cd pokedex
```

### 5. Start the Django Project

Run the command below to start the Django project within the `pokedex` directory:
```bash
uv run django-admin startproject pokedex .
```
This will generate the necessary files for the Django project.

## Create an App Inside the Project

### 1. Create the App

Use the following command to create an app called `pokemons` inside the project:
```bash
python manage.py startapp pokemons
```

This will create a new directory `pokemons` with all the necessary files for the app.

### 2. Add the App to Installed Apps

Next, open `settings.py` in the `pokedex` directory and add `'pokemons'` to the `INSTALLED_APPS` list:
```python
INSTALLED_APPS = [
    # Other installed apps...
    'pokemons',
]
```

## Adding Templates

### 1. Update `settings.py` for Template Directory

In the `TEMPLATES` setting of `settings.py`, update the `DIRS` list to include the templates directory:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

This will allow you to store your templates in the `templates` folder in your project's root directory.

## Running the Django Server
To run the development server, use the following command:
```bash
python manage.py runserver
```

## Create Models

### 1. Define Models for Your App

In the `models.py` file inside the `pokemons` app, define the models for your app.

### 2. Create and Apply Migrations

Once you have defined your models, run the following commands to create and apply migrations for your models:
```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the necessary database tables based on the models you defined.

---

Feel free to extend this README as your project evolves, adding more sections as needed for your app’s functionality, deployment, etc.
