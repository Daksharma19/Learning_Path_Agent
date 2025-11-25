# AI-Powered Personalized Learning Path Agent

An intelligent system that automatically generates structured, step-by-step learning paths for any user-specified topic. The system organizes scattered web resources into a cohesive curriculum and tracks user progress.

## Features

- 🎯 **Topic Structuring**: Uses NLP to break down topics into logical learning modules
- 📚 **Resource Curation**: Automatically gathers Wikipedia summaries and YouTube videos
- 👤 **User Authentication**: Secure signup/login system
- 📊 **Progress Tracking**: Visual progress indicators with percentage completion
- 💾 **MongoDB Database**: Persistent storage for users and learning paths

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Web Scraping**: BeautifulSoup4, Wikipedia API, YouTube Search API
- **NLP**: NLTK for text processing
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5 with custom styling

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd OS_project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB**
   - Install MongoDB on your system
   - Start MongoDB service
   - Default connection: `mongodb://localhost:27017/learning_path_agent`

5. **Configure environment variables** (optional)
   - Copy `.env.example` to `.env`
   - Update with your configuration

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and go to `http://localhost:5000`

## Usage

1. **Sign Up**: Create a new account
2. **Generate Path**: Enter any topic (e.g., "Machine Learning", "Python Programming")
3. **View Path**: Browse through modules and resources
4. **Track Progress**: Mark resources as complete to track your learning
5. **Dashboard**: View all your learning paths with progress percentages

## Project Structure

```
OS_project/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.py                 # MongoDB database operations
├── auth.py                     # User authentication
├── nlp_service.py             # NLP for topic structuring
├── web_scraper.py             # Web scraping for resources
├── learning_path_generator.py # Main path generation logic
├── requirements.txt           # Python dependencies
├── templates/                 # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   ├── generate.html
│   └── path_view.html
└── static/                    # Static files (CSS, JS)
```

## How It Works

1. **User Input**: User enters a topic they want to learn
2. **NLP Processing**: System breaks down the topic into logical sub-topics
3. **Resource Curation**: 
   - Fetches Wikipedia summaries for each module
   - Searches for relevant YouTube videos
4. **Path Generation**: Structures resources into a multi-step learning path
5. **Database Storage**: Saves path to MongoDB
6. **Progress Tracking**: Users can mark resources as complete

## Notes

- The system uses web scraping to gather resources, so internet connection is required
- Some topics may have limited resources available
- YouTube search results are fetched using the `youtube-search-python` library
- Wikipedia articles are fetched using the `wikipedia` library

## License

This project is for educational purposes.

