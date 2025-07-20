import uuid
import os

def generate_session_id(filename):
    name = os.path.splitext(filename)[0]
    return f"{uuid.uuid4().hex[:10]}"