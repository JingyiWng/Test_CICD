from fastapi import APIRouter
from app.config import VERSION

#TODO
# This creates a circular import risk because app.main imports this health module (to include its router). 
# When app.main is being imported, trying to import VERSION back from app.main can fail (module present but VERSION not yet set). 
router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": VERSION,
        "service": "todo-api"
    }