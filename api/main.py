from fastapi import FastAPI

from braveminer import database
from braveminer import endpoints
from braveminer import settings


app = FastAPI()

# Register endpoints
endpoints.register(app)

@app.on_event('startup')
async def startup():
    #await database.connect()
    pass

@app.on_event('shutdown')
async def shutdown():
    #await database.disconnect()
    pass
