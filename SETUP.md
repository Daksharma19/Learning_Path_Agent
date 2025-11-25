# Setup Guide

## Prerequisites

1. **Python 3.8+** installed on your system
2. **MongoDB** installed and running

## Step-by-Step Setup

### 1. Install MongoDB

**Windows:**
- Download MongoDB Community Server from https://www.mongodb.com/try/download/community
- Install and start the MongoDB service
- MongoDB will run on `mongodb://localhost:27017` by default

**Alternative - MongoDB Atlas (Cloud):**
- Create a free account at https://www.mongodb.com/cloud/atlas
- Create a cluster and get your connection string
- Update `MONGO_URI` in `.env` file

### 2. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb://localhost:27017/learning_path_agent
```

If you don't create a `.env` file, the application will use default values.

### 4. Run the Application

```bash
# Option 1: Using the run script
python run.py

# Option 2: Using app.py directly
python app.py
```

The application will start on `http://localhost:5000`

### 5. Access the Application

1. Open your browser and go to `http://localhost:5000`
2. Create an account (Sign Up)
3. Login with your credentials
4. Start generating learning paths!

## Troubleshooting

### MongoDB Connection Issues

- Ensure MongoDB is running: `mongod` (or check Windows Services)
- Check if MongoDB is listening on port 27017
- Verify the `MONGO_URI` in your `.env` file

### Python Package Issues

- Make sure you're using Python 3.8 or higher
- Try upgrading pip: `python -m pip install --upgrade pip`
- If NLTK data download fails, it will download automatically on first run

### Port Already in Use

- Change the port in `run.py` or `app.py`: `app.run(port=5001)`

## Testing the Application

1. **Sign Up**: Create a new account
2. **Generate Path**: Enter a topic like "Machine Learning" or "Python Programming"
3. **View Resources**: Browse through the generated modules
4. **Track Progress**: Click on resource checkboxes to mark them as complete
5. **Dashboard**: View all your learning paths with progress percentages

## Features to Try

- Generate paths for various topics (Machine Learning, Web Development, etc.)
- Mark resources as complete to see progress updates
- View historical learning paths on the dashboard
- Explore Wikipedia summaries and YouTube videos

