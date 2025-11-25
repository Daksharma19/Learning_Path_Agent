"""
Simple script to run the Flask application
"""
from app import app

if __name__ == '__main__':
    print("Starting Learning Path Agent...")
    print("Make sure MongoDB is running on your system")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

