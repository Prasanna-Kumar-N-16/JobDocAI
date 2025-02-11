from fastapi import APIRouter, HTTPException
from app.models.user_profile import UserProfile

router = APIRouter()

# Temporary in-memory storage (Replace with DB later)
profiles_db: Dict[str, UserProfile] = {}

# Create a new profile
@router.post("/", response_model=dict)
async def create_profile(profile: UserProfile):
    if profile.email in profiles_db:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    profiles_db[profile.email] = profile.dict()
    return {"message": "Profile created successfully!"}

# Get profile by email
@router.get("/{email}", response_model=UserProfile)
async def get_profile(email: str):
    if email not in profiles_db:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profiles_db[email]

# Get profiles
@router.get("/", response_model=Dict[str, UserProfile]) 
async def get_profiles():
    return profiles_db

# Update profile
@router.put("/{email}", response_model=dict)
async def update_profile(email: str, profile: UserProfile):
    if email not in profiles_db:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profiles_db[email] = profile.dict()
    return {"message": "Profile updated successfully!"}

# Delete profile
@router.delete("/{email}", response_model=dict)
async def delete_profile(email: str):
    if email not in profiles_db:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    del profiles_db[email]
    return {"message": "Profile deleted successfully!"}
