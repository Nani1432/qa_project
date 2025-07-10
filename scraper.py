import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import socket

def get_website_content(url):
    """Robust scraper with multiple fallback options"""
    # Configure session with advanced retry
    session = requests.Session()
    retry_strategy = Retry(
        total=5,  # Increased from 3
        backoff_factor=2,  # Longer wait between retries
        status_forcelist=[408, 429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # Set socket timeout
    socket.setdefaulttimeout(30)  # System-level timeout

    try:
        # Attempt with multiple user-agents
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'MedicasApp-Scraper/1.0 (+https://yourdomain.com)'
        ]

        for attempt in range(3):  # Additional attempt loop
            try:
                response = session.get(
                    url,
                    headers={
                        'User-Agent': user_agents[attempt % len(user_agents)],
                        'Accept-Language': 'en-US,en;q=0.9'
                    },
                    timeout=(10, 30),  # Connect timeout 10s, read timeout 30s
                    verify=False  # Bypass SSL verification if needed
                )
                response.raise_for_status()
                
                # Parse content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove unwanted elements
                for tag in ["script", "style", "noscript", "svg"]:
                    for element in soup.find_all(tag):
                        element.decompose()
                
                return soup.get_text(separator='\n', strip=True)

            except requests.exceptions.SSLError:
                # Retry with SSL verification disabled
                response = session.get(url, verify=False)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser').get_text()

    except Exception as e:
        raise Exception(
            f"Final scraping failure after all attempts. "
            f"Possible solutions:\n"
            f"1. Check if medicasapp.com is blocking scrapers\n"
            f"2. Try from a different network connection\n"
            f"3. Contact MedicasApp for API access\n"
            f"Technical details: {str(e)}"
        )