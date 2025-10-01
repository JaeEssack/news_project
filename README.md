# 📰 News Application

A Django-based news application that allows readers to view articles published by publishers and independent journalists.  
The project includes generated documentation (Sphinx) and supports multiple setup methods: local virtual environment or Docker.


## 📖 Features
- User authentication (readers, publishers, journalists).
- Create, read, update, and delete articles.
- REST API endpoints powered by Django REST Framework.
- Documentation generated with **Sphinx**.
- Ready-to-use Docker setup (with SQLite by default, extensible for other databases).


## ⚙️ Installation (Option 1: Virtual Environment)

Follow these steps if you want to run the project locally without Docker:

# Clone the repository
git clone https://github.com/JaeEssack/news_project.git
cd news_project

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start the server
python manage.py runserver

🐳 Installation (Option 2: Docker)

This method runs the app inside a container.

# Clone the repository
git clone https://github.com/JaeEssack/news_project.git
cd news_project

# Build the Docker image
docker build -t news_app .


📚 Documentation

This project uses Sphinx for documentation.
The generated HTML docs are located in:
# Run the container
docker run -d -p 8000:8000 news_app

  - news_project/docs/_build/html/
To view them locally, open:
  - news_project/docs/_build/html/index.html
Or rebuild them with:
  - cd news_project/docs
  - make html


🗄️ Database Notes

Default database: SQLite (works out of the box).

For MariaDB/PostgreSQL: update DATABASES in news_project/settings.py and adjust Docker/Docker Compose setup.

mysqlclient is included in requirements.txt for MySQL/MariaDB support, but additional dependencies may be needed in Docker.


🤝 Contributing

- Fork the repo
- Create a new branch (git checkout -b feature-name)
- Commit changes (git commit -m "Add new feature")
- Push to branch (git push origin feature-name)
- Open a Pull Request
