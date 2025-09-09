# Django Blogging Website

A full-featured blogging platform built with Django, allowing users to create, manage, and interact with blog posts.

## Features

- **User Authentication**
  - User registration
  - User login/logout functionality
  - Secure authentication system

- **Blog Post Management**
  - Create, read, update, and delete blog posts
  - Rich text editing for post content
  - Featured image support
  - Post excerpts
  - Category-based organization
  - Bookmark favorite posts

- **User Interface**
  - Clean and responsive design
  - Category-based post filtering
  - Detailed post view
  - Custom CSS styling

## Tech Stack

- Python 3.13
- Django
- SQLite3 (Database)
- HTML/CSS
- Bootstrap (for styling)

## Project Structure

```
blogging_website/
├── blogs/                  # Main blog application
│   ├── migrations/        # Database migrations
│   ├── static/           # Static files (CSS)
│   ├── templates/        # HTML templates
│   ├── forms.py         # Form definitions
│   ├── models.py        # Database models
│   ├── urls.py          # URL configurations
│   └── views.py         # View functions
├── my_blog/              # Project configuration
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
├── manage.py            # Django management script
└── db.sqlite3          # SQLite database
```

## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd blogging_website
```

2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install django
```

4. Apply database migrations
```bash
python manage.py migrate
```

5. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

7. Access the website at `http://127.0.0.1:8000`

## Usage

1. Register a new account or login with existing credentials
2. Create new blog posts through the post creation form
3. Add featured images and categorize your posts
4. Browse posts by category
5. Bookmark interesting posts for later reading
6. Manage your posts through the user interface

## Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin` to:
- Manage users
- Moderate blog posts
- Handle categories
- Monitor user activity

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
