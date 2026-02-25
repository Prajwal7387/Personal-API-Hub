import matplotlib.pyplot as plt
import seaborn as sns
import os
from django.conf import settings
from typing import Dict, Any

# Set style for premium look
plt.style.use('dark_background')
sns.set_palette("viridis")

class GitHubVisualizer:
    """
    Generates visual charts from processed GitHub analytics data.
    """
    
    BASE_DIR = os.path.join(settings.MEDIA_ROOT, 'analytics')

    @classmethod
    def generate_charts(cls, user_id: int, analytics_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates and saves charts to the media directory.
        Returns a dictionary of chart types and their relative URLs.
        """
        if not os.path.exists(cls.BASE_DIR):
            os.makedirs(cls.BASE_DIR, exist_ok=True)
            
        results = {}
        
        # 1. Language Distribution (Pie Chart)
        if analytics_data.get('language_distribution'):
            plt.figure(figsize=(8, 8))
            data = analytics_data['language_distribution']
            plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=140, colors=sns.color_palette("magma"))
            plt.title("Language Distribution", color='white', pad=20)
            
            filename = f"user_{user_id}_languages.png"
            filepath = os.path.join(cls.BASE_DIR, filename)
            plt.savefig(filepath, transparent=True, dpi=300)
            plt.close()
            results['languages_pie'] = os.path.join(settings.MEDIA_URL, 'analytics', filename).replace('\\', '/')

        # 2. Activity Trends (Bar Chart)
        if analytics_data.get('activity_trends'):
            plt.figure(figsize=(10, 6))
            trends = analytics_data['activity_trends']
            periods = [t['period'] for t in trends]
            counts = [t['count'] for t in trends]
            
            sns.barplot(x=periods, y=counts, hue=periods, palette="rocket", legend=False)
            plt.title("Repository Growth Trend", color='white', pad=20)
            plt.ylabel("Total Repositories")
            
            filename = f"user_{user_id}_trends.png"
            filepath = os.path.join(cls.BASE_DIR, filename)
            plt.savefig(filepath, transparent=True, dpi=300)
            plt.close()
            results['trends_bar'] = os.path.join(settings.MEDIA_URL, 'analytics', filename).replace('\\', '/')
            
        return results
