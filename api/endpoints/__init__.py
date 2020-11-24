from api.endpoints import users

def register(app):
    """Register all the endpoints in app."""
    app.include_router(users.router, prefix='/users', tags=['users'])
