from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from database import db
from auth import User
from learning_path_generator import LearningPathGenerator
import json
from bson import ObjectId

app = Flask(__name__)
app.config.from_object('config.Config')

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)

# Initialize learning path generator
path_generator = LearningPathGenerator()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not email or not password:
            flash('Please fill in all fields', 'error')
            return render_template('signup.html')
        
        user = User.create_user(username, email, password)
        if user:
            login_user(user)
            flash('Account created successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username or email already exists', 'error')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.verify_password(username, password)
        if user:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get all learning paths for the user
    paths = db.get_user_learning_paths(current_user.id)
    
    # Calculate progress for each path and convert ObjectId to string
    paths_with_progress = []
    for path in paths:
        path['_id'] = str(path['_id'])  # Convert ObjectId to string for template
        progress_percent = db.calculate_progress_percentage(path)
        paths_with_progress.append({
            'path': path,
            'progress': progress_percent
        })
    
    return render_template('dashboard.html', paths=paths_with_progress)

@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        topic = request.form.get('topic')
        if not topic:
            flash('Please enter a topic', 'error')
            return render_template('generate.html')
        
        # Generate learning path
        modules = path_generator.generate_path(topic)
        
        # Save to database
        path_id = db.save_learning_path(current_user.id, topic, modules)
        
        flash('Learning path generated successfully!', 'success')
        return redirect(url_for('view_path', path_id=path_id))
    
    return render_template('generate.html')

@app.route('/path/<path_id>')
@login_required
def view_path(path_id):
    path = db.get_learning_path(path_id)
    
    if not path or path['user_id'] != current_user.id:
        flash('Path not found', 'error')
        return redirect(url_for('dashboard'))
    
    # Convert ObjectId to string for template
    path['_id'] = str(path['_id'])
    
    progress_percent = db.calculate_progress_percentage(path)
    progress = path.get('progress', {})
    
    return render_template('path_view.html', path=path, progress=progress, progress_percent=progress_percent)

@app.route('/complete_resource', methods=['POST'])
@login_required
def complete_resource():
    data = request.get_json()
    path_id = data.get('path_id')
    module_index = data.get('module_index')
    resource_id = data.get('resource_id')
    
    # Verify path belongs to user
    path = db.get_learning_path(path_id)
    if not path or path['user_id'] != current_user.id:
        return jsonify({'success': False, 'error': 'Path not found'}), 404
    
    # Toggle progress (mark/unmark)
    success = db.update_progress(path_id, module_index, resource_id, toggle=True)
    
    if success:
        # Recalculate progress
        updated_path = db.get_learning_path(path_id)
        progress_percent = db.calculate_progress_percentage(updated_path)
        
        # Check if resource is now completed
        progress = updated_path.get('progress', {})
        is_completed = resource_id in progress.get(str(module_index), [])
        
        return jsonify({
            'success': True, 
            'progress': progress_percent,
            'is_completed': is_completed
        })
    
    return jsonify({'success': False}), 400

if __name__ == '__main__':
    app.run(debug=True)

