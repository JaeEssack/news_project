## How to Run This Project

1.  **Clone the repository:**
    `git clone [your-repository-url]`

2.  **Navigate to the project directory:**
    `cd news_project`

3.  **Set up the virtual environment and install dependencies:**
    `python -m venv venv`
    `venv\Scripts\activate` (on Windows)
    `pip install -r requirements.txt`

4.  **Apply database migrations:**
    `python manage.py migrate`

5.  **Run the development server:**
    `python manage.py runserver`

6.  **Open in your browser:**
    Open `http://localhost:8000` to view the application.