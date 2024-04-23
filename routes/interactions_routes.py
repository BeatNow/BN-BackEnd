from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from config.db import get_database, post_collection, users_collection, interactions_collection
from config.security import get_current_user, get_user_id, check_post_exists
from model.shemas import User


router = APIRouter()
@router.post("/like/{post_id}")
async def add_like(post_id: str, current_user: User = Depends(get_current_user), db=Depends(get_database)):
    await check_post_exists(post_id, db)
    user_id = await get_user_id(current_user.username)
    result = await interactions_collection.update_one(
        {"user_id": user_id, "post_id": post_id},
        {"$set": {"like_date": datetime.now()}},
        upsert=True
    )
    if result.modified_count == 0 and result.upserted_id is None:
        raise HTTPException(status_code=500, detail="Failed to add like")
    return {"message": "Like added successfully"}

@router.post("/save/{post_id}")
async def save_publication(post_id: str, current_user: User = Depends(get_current_user), db=Depends(get_database)):
    await check_post_exists(post_id, db)
    user_id = await get_user_id(current_user.username)
    result = await interactions_collection.update_one(
        {"user_id": user_id, "post_id": post_id},
        {"$set": {"saved_date": datetime.now()}},
        upsert=True
    )
    if result.modified_count == 0 and result.upserted_id is None:
        raise HTTPException(status_code=500, detail="Failed to save publication")
    return {"message": "Publication saved successfully"}

@router.post("/dislike/{post_id}")
async def add_dislike(post_id: str, current_user: User = Depends(get_current_user), db=Depends(get_database)):
    await check_post_exists(post_id, db)
    user_id = await get_user_id(current_user.username)
    result = await interactions_collection.update_one(
        {"user_id": user_id, "post_id": post_id},
        {"$set": {"dislike_date": datetime.now()}},
        upsert=True
    )
    if result.modified_count == 0 and result.upserted_id is None:
        raise HTTPException(status_code=500, detail="Failed to add dislike")
    return {"message": "Dislike added successfully"}

@router.post("/unlike/{post_id}")
async def remove_like(post_id: str, current_user: User = Depends(get_current_user), db=Depends(get_database)):
    await check_post_exists(post_id, db)
    user_id = await get_user_id(current_user.username)
    result = await interactions_collection.update_one(
        {"user_id": user_id, "post_id": post_id},
        {"$unset": {"like_date": ""}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to remove like")
    return {"message": "Like removed successfully"}

@router.post("/unsave/{post_id}")
async def remove_saved(post_id: str, current_user: User = Depends(get_current_user), db=Depends(get_database)):
    await check_post_exists(post_id, db)
    user_id = await get_user_id(current_user.username)
    result = await interactions_collection.update_one(
        {"user_id": user_id, "post_id": post_id},
        {"$unset": {"saved_date": ""}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to remove saved publication")
    return {"message": "Saved publication removed successfully"}

@router.post("/undislike/{post_id}")
async def remove_dislike(post_id: str, current_user: User = Depends(get_current_user), db=Depends(get_database)):
    await check_post_exists(post_id, db)
    user_id = await get_user_id(current_user.username)
    result = await interactions_collection.update_one(
        {"user_id": user_id, "post_id": post_id},
        {"$unset": {"dislike_date": ""}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to remove dislike")
    return {"message": "Dislike removed successfully"}