import os
from typing import Annotated
from passlib.handlers.bcrypt import bcrypt
import bcrypt
from model.shemas import User
from config.security import oauth2_scheme,guardar_log, SSH_USERNAME_RES, SSH_PASSWORD_RES, SSH_HOST_RES, get_current_active_user, get_current_user
from config.db import users_collection
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, Depends, status, APIRouter
import paramiko

router = APIRouter()




@router.post("/register")
async def register(user: User):
    # Check if the username is already taken
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password before saving it
    password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_dict = user.dict()
    user_dict['password'] = password_hash
    result = await users_collection.insert_one(user_dict)
    user_id = result.inserted_id
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=SSH_HOST_RES, username=SSH_USERNAME_RES, password=SSH_PASSWORD_RES)

        username = user_dict['username']
        directory_commands = f"sudo mkdir -p /var/www/html/beatnow/{username}/photo_profile /var/www/html/beatnow/{username}/posts"
        stdin, stdout, stderr = ssh.exec_command(directory_commands)

        exit_status = stderr.channel.recv_exit_status()

        if exit_status != 0:
            raise HTTPException(status_code=500, detail="Error al crear la carpeta en el servidor remoto")
    return {"_id": str(user_id), **user_dict}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users")
async def get_all_users(token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token)  # Espera el resultado de la corutina
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.username == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized",
        )

    all_users = await users_collection.find({}, {"username": 1, "_id": 0}).to_list(length=None)
    usernames = [user["username"] for user in all_users]
    return {"usernames": usernames}
