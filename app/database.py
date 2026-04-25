import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """
    Initialize and return the Supabase client.
    Uses the service role key for backend-level administrative access.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError("Supabase credentials (URL or KEY) are missing in .env file.")
        
    return create_client(url, key)

# Global database instance
supabase = get_supabase_client()