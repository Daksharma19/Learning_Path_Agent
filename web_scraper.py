import requests
from bs4 import BeautifulSoup
import wikipedia
from youtubesearchpython import VideosSearch
import re

class WebScraper:
    @staticmethod
    def get_wikipedia_summary(topic, sentences=5):
        """Fetch Wikipedia summary for a topic"""
        try:
            # Set language to English
            wikipedia.set_lang("en")
            
            # Search for the topic
            search_results = wikipedia.search(topic, results=1)
            if not search_results:
                return None
            
            page_title = search_results[0]
            page = wikipedia.page(page_title, auto_suggest=False)
            
            # Get summary
            summary = page.summary
            # Limit to specified number of sentences
            sentences_list = summary.split('. ')
            summary = '. '.join(sentences_list[:sentences])
            
            return {
                'title': page_title,
                'summary': summary,
                'url': page.url,
                'type': 'wikipedia'
            }
        except wikipedia.exceptions.DisambiguationError as e:
            # If disambiguation, try the first option
            try:
                page = wikipedia.page(e.options[0], auto_suggest=False)
                summary = page.summary
                sentences_list = summary.split('. ')
                summary = '. '.join(sentences_list[:sentences])
                return {
                    'title': page.title,
                    'summary': summary,
                    'url': page.url,
                    'type': 'wikipedia'
                }
            except:
                return None
        except Exception as e:
            print(f"Error fetching Wikipedia: {e}")
            return None
    
    @staticmethod
    def search_youtube_videos(query, max_results=3):
        """Search for YouTube videos related to a topic"""
        try:
            videos_search = VideosSearch(query, limit=max_results)
            results = videos_search.result()
            
            videos = []
            for item in results.get('result', [])[:max_results]:
                video = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'duration': item.get('duration', ''),
                    'thumbnail': item.get('thumbnails', [{}])[0].get('url', '') if item.get('thumbnails') else '',
                    'channel': item.get('channel', {}).get('name', ''),
                    'type': 'youtube'
                }
                videos.append(video)
            
            return videos
        except Exception as e:
            print(f"Error fetching YouTube videos: {e}")
            return []
    
    @staticmethod
    def scrape_article_content(url):
        """Scrape content from a web article URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit to first 1000 characters
            text = text[:1000] + '...' if len(text) > 1000 else text
            
            return text
        except Exception as e:
            print(f"Error scraping article: {e}")
            return None

