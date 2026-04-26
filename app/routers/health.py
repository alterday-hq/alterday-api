from fastapi import APIRouter, HTTPException
from app.database import supabase

# Create router for health checks
router = APIRouter(
    tags=["Health & Diagnostics"]
)

@router.get("/")
async def root():
    """Base endpoint to verify that the API is running."""
    return {"status": "ok", "message": "AlterDay API is up and running."}

@router.get("/test-db")
async def test_db_connection():
    """
    Test connection to Supabase by attempting to fetch a single row 
    from the 'activities' table.
    """
    try:
        # Attempt to fetch 1 record to verify read access
        response = supabase.table("activities").select("*").limit(1).execute()
        
        return {
            "status": "success",
            "message": "Successfully connected to Supabase DB.",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))