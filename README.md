# Educational Content Management API

An API built with Django REST framework for managing educational content. The project allows authenticated users to create, organize, search, and manage learning resources using categories and tags.

This project was built to strengthen my backend development skills while learning how to design scalable APIs using Django.

## Features

* JWT Authentication
* CRUD operations for content
* Categories and tags management
* Search, filtering, and ordering
* Pagination
* Reading time estimation
* Tracking individual content views

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* JWT Authentication
* Git

## How to install

Clone the repository:

```bash
git clone https://github.com/BillyMko/django-content-management-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start server:

```bash
python manage.py runserver
```

## Main API Endpoints

Authentication

* POST /api/register/
* POST /api/login/
* POST /api/token/refresh/

Content

* GET     /api/content/
* POST    /api/content/
* PUT     /api/content/{id}/
* DELETE  /api/content/{id}/
* GET     /api/content/{id}/
* PATCH   /api/content/{id}/


Categories

* GET     /api/categories/
* POST    /api/categories/

Tags

* GET     /api/tags/
* POST    /api/tags/

## Future Improvements

* PostgreSQL migration
* Bulk content creation
* JSON import
* Query optimization

## What I Learned

This project helped me gain new knowledge in:

* Serializers and ViewSets
* Model relationships
* Custom Permissions
* Filtering and pagination

## Author

Believe Mukomberanwa
