import bcrypt
import db

def register_user(username, password, is_tutor):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # hashed is already a string in bcrypt 4.x, no need to decode
    return db.add_user(username, hashed, 1 if is_tutor else 0)

def authenticate_user(username, password):
    user = db.get_user_by_username(username)

    if user:
        stored_hash = user['password']  # this is already a str
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return user
    return None
