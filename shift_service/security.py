import bcrypt


def create_hash_pass(password: bytes):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password: bytes, hashed_password: bytes):
    return bcrypt.checkpw(password, hashed_password)
