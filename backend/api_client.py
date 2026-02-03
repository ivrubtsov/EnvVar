import os
import requests
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class ExternalAPIClient:
    """Client for external API integrations"""
    
    def __init__(self):
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        self.openai_org_id = os.getenv('OPENAI_ORG_ID')
        self.openai_base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        
        self.weather_api_key = os.environ.get('WEATHER_API_KEY')
        self.weather_api_url = os.getenv('WEATHER_API_URL', 'https://api.weatherapi.com/v1')
        
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github_api_url = os.getenv('GITHUB_API_URL', 'https://api.github.com')
        
        # Timeout settings
        self.request_timeout = int(os.getenv('API_REQUEST_TIMEOUT', '30'))
        self.max_retries = int(os.getenv('API_MAX_RETRIES', '3'))
        
        # Feature flags
        self.enable_caching = os.getenv('ENABLE_API_CACHING', 'true').lower() == 'true'
        self.enable_rate_limiting = os.getenv('ENABLE_RATE_LIMITING', 'true').lower() == 'true'
    
    def query_openai(self, prompt: str, model: Optional[str] = None) -> Dict[str, Any]:
        """Query OpenAI API"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }
        
        if self.openai_org_id:
            headers['OpenAI-Organization'] = self.openai_org_id
        
        model = model or os.getenv('OPENAI_MODEL', 'gpt-4')
        temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
        max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '1000'))
        
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        response = requests.post(
            f'{self.openai_base_url}/chat/completions',
            headers=headers,
            json=payload,
            timeout=self.request_timeout
        )
        
        return response.json()
    
    def get_weather(self, location: str) -> Dict[str, Any]:
        """Get weather data"""
        if not self.weather_api_key:
            raise ValueError("WEATHER_API_KEY not set")
        
        params = {
            'key': self.weather_api_key,
            'q': location,
            'aqi': os.getenv('WEATHER_INCLUDE_AQI', 'no')
        }
        
        response = requests.get(
            f'{self.weather_api_url}/current.json',
            params=params,
            timeout=self.request_timeout
        )
        
        return response.json()
    
    def get_github_repo(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get GitHub repository information"""
        if not self.github_token:
            logger.warning("GITHUB_TOKEN not set, API rate limits will apply")
        
        headers = {}
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
        
        response = requests.get(
            f'{self.github_api_url}/repos/{owner}/{repo}',
            headers=headers,
            timeout=self.request_timeout
        )
        
        return response.json()


# Email service configuration
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@example.com')
SENDGRID_TEMPLATE_ID = os.getenv('SENDGRID_TEMPLATE_ID')

def send_email(to_email: str, subject: str, content: str) -> bool:
    """Send email via SendGrid"""
    if not SENDGRID_API_KEY:
        logger.error("SENDGRID_API_KEY not configured")
        return False
    
    # Email sending logic here
    logger.info(f"Sending email to {to_email}")
    return True
