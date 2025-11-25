from pymongo import MongoClient
from config import Config
import datetime
from urllib.parse import urlparse

class Database:
    def __init__(self):
        mongo_uri = Config.MONGO_URI
        self.client = MongoClient(mongo_uri)
        # Extract database name from URI or use default
        # Handle both mongodb:// and mongodb+srv:// formats
        if '/learning_path_agent' in mongo_uri:
            db_name = 'learning_path_agent'
        else:
            parsed_uri = urlparse(mongo_uri)
            db_name = parsed_uri.path[1:] if parsed_uri.path and len(parsed_uri.path) > 1 else 'learning_path_agent'
            if not db_name or db_name == '/':
                db_name = 'learning_path_agent'
        self.db = self.client[db_name]
        
    def get_collection(self, name):
        return self.db[name]
    
    def create_user(self, username, email, password_hash):
        """Create a new user in the database"""
        users = self.get_collection('users')
        if users.find_one({'$or': [{'username': username}, {'email': email}]}):
            return None
        user = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'created_at': datetime.datetime.utcnow()
        }
        result = users.insert_one(user)
        return str(result.inserted_id)
    
    def get_user_by_username(self, username):
        """Get user by username"""
        users = self.get_collection('users')
        return users.find_one({'username': username})
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        users = self.get_collection('users')
        from bson import ObjectId
        return users.find_one({'_id': ObjectId(user_id)})
    
    def save_learning_path(self, user_id, topic, modules):
        """Save a learning path to the database"""
        paths = self.get_collection('learning_paths')
        path = {
            'user_id': user_id,
            'topic': topic,
            'modules': modules,
            'created_at': datetime.datetime.utcnow(),
            'progress': {}  # {module_index: [completed_resource_ids]}
        }
        result = paths.insert_one(path)
        return str(result.inserted_id)
    
    def get_user_learning_paths(self, user_id):
        """Get all learning paths for a user"""
        paths = self.get_collection('learning_paths')
        return list(paths.find({'user_id': user_id}).sort('created_at', -1))
    
    def get_learning_path(self, path_id):
        """Get a specific learning path"""
        paths = self.get_collection('learning_paths')
        from bson import ObjectId
        return paths.find_one({'_id': ObjectId(path_id)})
    
    def update_progress(self, path_id, module_index, resource_id, toggle=False):
        """Mark or unmark a resource as completed"""
        paths = self.get_collection('learning_paths')
        from bson import ObjectId
        path = paths.find_one({'_id': ObjectId(path_id)})
        if not path:
            return False
        
        if 'progress' not in path:
            path['progress'] = {}
        
        module_str = str(module_index)
        if module_str not in path['progress']:
            path['progress'][module_str] = []
        
        # Toggle: remove if exists, add if not
        if toggle:
            if resource_id in path['progress'][module_str]:
                path['progress'][module_str].remove(resource_id)
            else:
                path['progress'][module_str].append(resource_id)
        else:
            # Just add if not exists
            if resource_id not in path['progress'][module_str]:
                path['progress'][module_str].append(resource_id)
        
        paths.update_one(
            {'_id': ObjectId(path_id)},
            {'$set': {'progress': path['progress']}}
        )
        return True
    
    def calculate_progress_percentage(self, path):
        """Calculate completion percentage for a learning path"""
        if not path or 'modules' not in path:
            return 0
        
        total_resources = 0
        completed_resources = 0
        progress = path.get('progress', {})
        
        for module_index, module in enumerate(path['modules']):
            resources = module.get('resources', [])
            total_resources += len(resources)
            
            completed = progress.get(str(module_index), [])
            completed_resources += len(completed)
        
        if total_resources == 0:
            return 0
        
        return round((completed_resources / total_resources) * 100, 2)

# Global database instance
db = Database()

