from api.endpoints import users, login, companies

def register(app):
    """Register all the endpoints in app."""
    app.include_router(users.router, prefix='/users', tags=['users'])
    app.include_router(login.router, prefix='/login', tags=['login'])
    app.include_router(companies.router, prefix='/companies', tags=['companies'])
