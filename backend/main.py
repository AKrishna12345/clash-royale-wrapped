import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.clash_royale import get_player_info, get_player_battlelog, ClashRoyaleAPIError, validate_tag_format
from api.analysis import analyze_player
from models.schemas import PlayerTagRequest, PlayerInfoResponse, ErrorResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Clash Royale Wrapped API")

# Configure CORS - allow origins from environment variable or default to localhost
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Clash Royale Wrapped API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/test")
async def test():
    """Test endpoint to verify API is working"""
    return {
        "status": "ok",
        "proxy_enabled": os.getenv("USE_PROXY", "true"),
        "api_base": "https://proxy.royaleapi.dev/v1" if os.getenv("USE_PROXY", "true").lower() == "true" else "https://api.clashroyale.com/v1",
        "has_token": bool(os.getenv("CLASH_ROYALE_API_TOKEN"))
    }

@app.post("/api/player", response_model=PlayerInfoResponse)
async def get_player(player_request: PlayerTagRequest):
    """
    Get player information from Clash Royale API and generate insights.
    
    Validates the tag format and fetches player data.
    Returns error if tag is invalid or player not found.
    """
    try:
        # Validate tag format first
        if not validate_tag_format(player_request.tag):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid tag format. Tag must start with # and contain only uppercase letters and numbers."
            )
        
        # Fetch player info and battle log from Clash Royale API
        player_data = await get_player_info(player_request.tag)
        battle_log = await get_player_battlelog(player_request.tag)
        
        # Generate insights
        insights = analyze_player(player_data, battle_log)
        
        # Combine player data with insights
        response_data = {
            "player": player_data,
            "insights": insights
        }
        
        return PlayerInfoResponse(
            success=True,
            data=response_data
        )
        
    except ClashRoyaleAPIError as e:
        # Handle API-specific errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
