import os

from libs.database import create_uri

origins = os.environ.get("ALLOWED_ORIGINS", "").split(",")
port = int(os.environ.get("API_PORT", 8000))

database_uri = create_uri()
