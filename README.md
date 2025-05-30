# Inkwell - AI Summarizing Blog App 

Inkwell is a modern Flask-based blog application enhanced with AI-powered summarization. Users can write, manage, and read blog posts, while the app uses natural language processing to summarize content intelligently.

##  Features

-  Full blog post creation, editing, and deletion
-  User registration, login, logout
-  Profile picture upload
-  Post image support
-  Search functionality
-  Comments and likes (under development)
-  AI-powered blog summarization
-  User dashboard and post statistics
-  CSRF protection, input validation, and Flask best practices

##  AI Integration

- Uses HuggingFace Transformers or custom summarizer model
- Automatically summarizes long blog content
- Designed for easy AI module replacement

## Tech Stack

- **Backend:** Flask, SQLAlchemy, Jinja2
- **Frontend:** HTML, Bootstrap,css
- **Database:** SQLite (development) / PostgreSQL (production-ready)
- **AI:** Custom NLP summarizer (transformers-based or textrank)
- **Deployment:** Render / GitHub

##  Project Structure

gingerblog/
│
├── static/ # Images, CSS
├── templates/ # Jinja2 HTML templates
├── users/ # User forms, routes, utils
├── posts/ # Post-related views and logic
├── main/ # Homepage & general routes
├── utils/ # Summarization logic
├── errors/ # Custom error pages
├── config.py # App configuration
├── run.py # App entry point


##  Installation

```bash
git clone https://github.com/Chievu/Inkwell-AI-summerizing-Blog-App.git
cd Inkwell-AI-summerizing-Blog-App
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

Create a .env file (or set environment variables):
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///site.db

Then run the app:
python run.py
