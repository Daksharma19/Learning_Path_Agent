import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import requests
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

class NLPService:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def extract_key_concepts(self, topic):
        """Extract key concepts and break down topic into sub-topics"""
        # Simple keyword extraction
        words = word_tokenize(topic.lower())
        words = [w for w in words if w not in self.stop_words and w.isalnum()]
        
        return words
    
    def generate_learning_modules(self, topic):
        """
        Generate structured learning modules for a topic.
        This uses a rule-based approach with some heuristics for common topics.
        """
        topic_lower = topic.lower()
        
        # Common learning path templates
        templates = {
            'machine learning': [
                'Introduction to Machine Learning',
                'Supervised Learning Basics',
                'Unsupervised Learning',
                'Deep Learning Fundamentals',
                'Neural Networks',
                'Model Evaluation and Validation',
                'Practical Applications'
            ],
            'python': [
                'Python Basics and Syntax',
                'Data Structures in Python',
                'Functions and Modules',
                'Object-Oriented Programming',
                'File Handling and I/O',
                'Libraries and Packages',
                'Advanced Topics and Best Practices'
            ],
            'web development': [
                'HTML Fundamentals',
                'CSS Styling',
                'JavaScript Basics',
                'Frontend Frameworks',
                'Backend Development',
                'Database Integration',
                'Deployment and DevOps'
            ]
        }
        
        # Check if we have a template
        for key, modules in templates.items():
            if key in topic_lower:
                return modules
        
        # Generic fallback: create modules based on topic analysis
        return self._generate_generic_modules(topic)
    
    def _generate_generic_modules(self, topic):
        """Generate generic learning modules when no template matches"""
        # Extract main keywords
        words = word_tokenize(topic)
        words = [w.lower() for w in words if w.isalnum() and w.lower() not in self.stop_words]
        
        base_modules = [
            f'Introduction to {topic}',
            f'Fundamentals of {topic}',
            f'Core Concepts',
            f'Intermediate Topics',
            f'Advanced Applications',
            f'Best Practices',
            f'Real-World Examples'
        ]
        
        return base_modules
    
    def structure_topic(self, topic):
        """
        Main method to structure a topic into learning modules.
        Returns a list of module titles.
        """
        modules = self.generate_learning_modules(topic)
        return modules

