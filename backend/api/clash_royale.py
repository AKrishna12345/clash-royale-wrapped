import os
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Use RoyaleAPI proxy to avoid IP whitelist issues
# Set USE_PROXY=false to use direct API (requires static IP whitelist)
USE_PROXY = os.getenv("USE_PROXY", "true").lower() == "true"

if USE_PROXY:
    CLASH_ROYALE_API_BASE = "https://proxy.royaleapi.dev/v1"
else:
    CLASH_ROYALE_API_BASE = "https://api.clashroyale.com/v1"

API_TOKEN = os.getenv("CLASH_ROYALE_API_TOKEN")


class ClashRoyaleAPIError(Exception):
    """Custom exception for Clash Royale API errors"""
    pass


def validate_tag_format(tag: str) -> bool:
    """
    Validate that the tag follows Clash Royale format.
    Tags should start with # and contain only uppercase letters and numbers.
    """
    if not tag:
        return False
    
    # Remove # if present
    clean_tag = tag.replace("#", "")
    
    # Check length (typically 3-15 characters)
    if len(clean_tag) < 3 or len(clean_tag) > 15:
        return False
    
    # Check if it contains only uppercase letters and numbers
    if not clean_tag.isalnum() or not clean_tag.isupper():
        return False
    
    return True


def encode_tag(tag: str) -> str:
    """
    Encode the player tag for URL usage.
    Removes # and URL encodes it.
    """
    clean_tag = tag.replace("#", "")
    return f"%23{clean_tag}"


async def get_player_info(player_tag: str) -> Dict[str, Any]:
    """
    Fetch player information from Clash Royale API.
    
    Args:
        player_tag: Player tag (with or without #)
    
    Returns:
        Dictionary containing player information
    
    Raises:
        ClashRoyaleAPIError: If API call fails or player not found
    """
    if not API_TOKEN:
        raise ClashRoyaleAPIError("Clash Royale API token not configured. Please set CLASH_ROYALE_API_TOKEN environment variable.")
    
    # Validate tag format
    if not validate_tag_format(player_tag):
        raise ClashRoyaleAPIError("Invalid tag format. Tag must start with # and contain only uppercase letters and numbers.")
    
    # Encode tag for URL
    encoded_tag = encode_tag(player_tag)
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }
    
    # Make API request
    url = f"{CLASH_ROYALE_API_BASE}/players/{encoded_tag}"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
            
            # Handle different status codes
            if response.status_code == 404:
                raise ClashRoyaleAPIError("Player not found. Please check your tag and try again.")
            elif response.status_code == 403:
                raise ClashRoyaleAPIError("API access forbidden. Please check your API token.")
            elif response.status_code == 429:
                raise ClashRoyaleAPIError("Rate limit exceeded. Please try again later.")
            elif response.status_code != 200:
                raise ClashRoyaleAPIError(f"API error: {response.status_code} - {response.text}")
            
            return response.json()
            
    except httpx.TimeoutException:
        raise ClashRoyaleAPIError("Request timed out. Please try again.")
    except httpx.RequestError as e:
        raise ClashRoyaleAPIError(f"Network error: {str(e)}")
    except Exception as e:
        if isinstance(e, ClashRoyaleAPIError):
            raise
        raise ClashRoyaleAPIError(f"Unexpected error: {str(e)}")


async def get_player_battlelog(player_tag: str) -> list:
    """
    Fetch player battle log from Clash Royale API.
    
    Args:
        player_tag: Player tag (with or without #)
    
    Returns:
        List of battle log entries
    
    Raises:
        ClashRoyaleAPIError: If API call fails
    """
    if not API_TOKEN:
        raise ClashRoyaleAPIError("Clash Royale API token not configured.")
    
    # Encode tag for URL
    encoded_tag = encode_tag(player_tag)
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }
    
    # Make API request
    url = f"{CLASH_ROYALE_API_BASE}/players/{encoded_tag}/battlelog"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 404:
                return []  # Return empty list if battle log not available
            elif response.status_code != 200:
                return []  # Return empty list on other errors (battle log might be private)
            
            return response.json()
            
    except Exception:
        return []  # Return empty list on any error
