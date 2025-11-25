from nlp_service import NLPService
from web_scraper import WebScraper

class LearningPathGenerator:
    def __init__(self):
        self.nlp_service = NLPService()
        self.web_scraper = WebScraper()
    
    def generate_path(self, topic):
        """
        Generate a complete learning path for a topic.
        Returns a list of modules, each containing resources.
        """
        # Step 1: Break down topic into modules using NLP
        module_titles = self.nlp_service.structure_topic(topic)
        
        # Step 2: For each module, gather resources
        modules = []
        for index, module_title in enumerate(module_titles):
            module = {
                'index': index,
                'title': module_title,
                'resources': []
            }
            
            # Get Wikipedia summary for the module topic
            wiki_resource = self.web_scraper.get_wikipedia_summary(
                f"{topic} {module_title}", sentences=5
            )
            if wiki_resource:
                wiki_resource['id'] = f"wiki_{index}_0"
                module['resources'].append(wiki_resource)
            
            # Search for YouTube videos
            video_query = f"{topic} {module_title} tutorial"
            videos = self.web_scraper.search_youtube_videos(video_query, max_results=2)
            
            for vid_index, video in enumerate(videos):
                video['id'] = f"youtube_{index}_{vid_index + 1}"
                module['resources'].append(video)
            
            # If no Wikipedia found for module, try main topic
            if not wiki_resource and index == 0:
                wiki_resource = self.web_scraper.get_wikipedia_summary(topic, sentences=7)
                if wiki_resource:
                    wiki_resource['id'] = f"wiki_{index}_0"
                    module['resources'].insert(0, wiki_resource)
            
            modules.append(module)
        
        return modules

