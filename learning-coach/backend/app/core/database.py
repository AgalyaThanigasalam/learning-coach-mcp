# Database module — using in-memory storage (no MongoDB required)
db = None

async def connect_db():
    print("Using in-memory storage (no MongoDB required)")

async def disconnect_db():
    pass

def get_db():
    return db
