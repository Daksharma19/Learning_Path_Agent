import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://appUser:9uJbu25iqzNE0O5t@cluster0.cmbopgj.mongodb.net/learning_path_agent'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or ''
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') or 'AIzaSyC75WjYNELo0PczCOkL0Y1TNPOb0z97o1E'

